#!/usr/bin/env python3
"""
跨模型验证脚本 - plan 技能阶段4第一层验证使用

用不同的 AI 模型审查交付物，实现模型隔离验证。
主 agent（glm-5.2）执行任务后，用此脚本调另一个模型审查结果。

用法:
  from hermes_tools import execute_code  # 或直接在 execute_code 中 import
  
  # 方法1：直接调用（推荐在 execute_code 中使用）
  result = cross_model_verify(
      prompt="验证以下交付物是否完整...",
      content="交付物内容...",
      api="dashscope",      # 可选: dashscope/moonshot/deepseek
      model="qwen3.7-flash" # 可选，默认按 API 自动选择
  )

  # 方法2：命令行
  # python cross-model-verify.py --api dashscope --model qwen3.7-flash \
  #   --prompt-file prompt.txt --content-file deliverable.md

环境变量要求（已在 ~/AppData/Local/hermes/.env 中配置）:
  DASHSCOPE_API_KEY / DASHSCOPE_BASE_URL
  MOONSHOT_API_KEY
  DEEPSEEK_API_KEY / DEEPSEEK_BASE_URL

可用 API 和模型（2026.7.28 验证通过）:
  dashscope:  qwen3.7-flash (默认, 快/便宜), qwen3.7-max (更强)
  moonshot:   moonshot-v1-8k
  deepseek:   deepseek-chat (actual: deepseek-v4-flash)
"""

import os
import sys
import json
import urllib.request
import argparse
from pathlib import Path

# ============================================================
# API 配置
# ============================================================

APIS = {
    # 火山方舟 Coding Plan（主力，零成本，9个模型）
    # 2026.8.3 验证：qwen3.7-flash/max免费额度耗尽(403)，改用火山方舟
    "volcano": {
        "key_env": "ARK_API_KEY",
        "base_url_env": "VOLCANO_BASE_URL",
        "default_base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
        "default_model": "deepseek-v4-flash",
        "available_models": [
            "deepseek-v4-flash",      # L级快速响应
            "doubao-seed-2.0-lite",   # L级超轻量
            "glm-5.2",                # M级旗舰通用
            "deepseek-v4-pro",        # H级深度推理
            "minimax-m3",             # 通用均衡
            "minimax-m2.7",           # 推理增强
        ],
        # 需要关闭thinking模式的模型
        "thinking_disabled_models": ["glm-5.2", "deepseek-v4-pro", "kimi-k2.6"],
        # extra_body 参数注入
        "extra_body": {"thinking": {"type": "disabled"}},
    },
    # DashScope 千问（备用，免费额度已耗尽，仅qwen3.7-max可用）
    "dashscope": {
        "key_env": "DASHSCOPE_API_KEY",
        "base_url_env": "DASHSCOPE_BASE_URL",
        "default_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen3.7-max",
        "available_models": ["qwen3.7-max"],
    },
    # Moonshot（按量付费）
    "moonshot": {
        "key_env": "MOONSHOT_API_KEY",
        "base_url_env": None,
        "default_base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
        "available_models": ["moonshot-v1-8k"],
    },
    # DeepSeek（按量付费）
    "deepseek": {
        "key_env": "DEEPSEEK_API_KEY",
        "base_url_env": "DEEPSEEK_BASE_URL",
        "default_base_url": "https://api.deepseek.com",
        "default_model": "deepseek-chat",
        "available_models": ["deepseek-chat"],
    },
}

# ============================================================
# 环境变量加载（从 Hermes .env 文件）
# ============================================================

def _load_env():
    """从 ~/AppData/Local/hermes/.env 加载环境变量"""
    env_path = Path.home() / "AppData" / "Local" / "hermes" / ".env"
    if not env_path.exists():
        # 尝试其他路径
        for p in [Path.home() / ".hermes" / ".env", Path("/etc/hermes/.env")]:
            if p.exists():
                env_path = p
                break
        else:
            return  # 环境变量可能已在 shell 中

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if key and key not in os.environ:
                    os.environ[key] = val


def _get_api_config(api_name: str, model: str = None):
    """获取 API 配置"""
    if api_name not in APIS:
        raise ValueError(
            f"Unknown API: {api_name}. Available: {list(APIS.keys())}"
        )

    cfg = APIS[api_name]

    api_key = os.environ.get(cfg["key_env"], "")
    if not api_key:
        raise ValueError(
            f"Environment variable {cfg['key_env']} not set. "
            f"Check ~/AppData/Local/hermes/.env"
        )

    if cfg["base_url_env"]:
        base_url = os.environ.get(cfg["base_url_env"], cfg["default_base_url"])
    else:
        base_url = cfg["default_base_url"]

    if not model:
        model = cfg["default_model"]

    return api_key, base_url, model


# ============================================================
# API 调用
# ============================================================

def _call_chat_api(base_url: str, api_key: str, model: str,
                   messages: list, temperature: float = 0.3,
                   max_tokens: int = 4096, timeout: int = 120,
                   extra_body: dict = None) -> dict:
    """调用 OpenAI 兼容的 chat/completions API

    Args:
        extra_body: 额外参数注入到请求体（如 thinking: {type: disabled}）
    """

    payload_dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    # 火山方舟 Coding Plan 需要注入 extra_body 关闭 thinking 模式
    if extra_body:
        payload_dict.update(extra_body)

    payload = json.dumps(payload_dict).encode("utf-8")

    url = f"{base_url.rstrip('/')}/chat/completions"

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    resp = urllib.request.urlopen(req, timeout=timeout)
    data = json.loads(resp.read())

    return {
        "content": data["choices"][0]["message"]["content"],
        "model": data.get("model", model),
        "usage": data.get("usage", {}),
        "finish_reason": data["choices"][0].get("finish_reason", ""),
    }


# ============================================================
# 核心函数：跨模型验证
# ============================================================

def cross_model_verify(
    prompt: str,
    content: str,
    api: str = "volcano",
    model: str = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
    timeout: int = 120,
) -> dict:
    """
    用不同的模型验证交付物。

    参数:
        prompt: 验证指令（告诉验证模型该检查什么）
        content: 交付物内容（被验证的文本）
        api: API 名称 (volcano/dashscope/moonshot/deepseek)
        model: 模型名（None 则用 API 默认模型）
        temperature: 温度，越低越确定
        max_tokens: 最大输出 tokens
        timeout: 超时秒数

    返回:
        dict: {
            "success": bool,
            "content": str,       # 验证报告内容
            "model": str,         # 实际使用的模型
            "usage": dict,        # token 用量
            "error": str or None, # 错误信息
        }
    """
    _load_env()

    api_key, base_url, model = _get_api_config(api, model)

    messages = [
        {
            "role": "system",
            "content": (
                "你是独立验证员。你的任务是审查交付物的质量和完整性。"
                "你只负责验证，不负责执行。"
                "请按验证指令逐项检查，给出具体的问题和改进建议。"
                "如果交付物没有问题，明确说明'验证通过'。"
                "格式要求：用清晰的分点列表输出验证结果。"
            ),
        },
        {
            "role": "user",
            "content": f"## 验证指令\n\n{prompt}\n\n## 交付物内容\n\n{content}",
        },
    ]

    # 获取该 API 的 extra_body 配置（火山方舟需关闭 thinking）
    cfg = APIS.get(api, {})
    extra_body = cfg.get("extra_body")

    try:
        result = _call_chat_api(
            base_url, api_key, model, messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            extra_body=extra_body,
        )
        return {
            "success": True,
            "content": result["content"],
            "model": result["model"],
            "usage": result["usage"],
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "model": model,
            "usage": {},
            "error": str(e),
        }


# ============================================================
# 批量验证：对同一内容用多个模型交叉验证
# ============================================================

def cross_model_verify_multi(
    prompt: str,
    content: str,
    apis: list = None,
    model: str = None,
) -> list:
    """
    用多个模型对同一内容进行交叉验证。

    参数:
        prompt: 验证指令
        content: 交付物内容
        apis: API 名称列表（None 则用全部可用 API）
        model: 指定模型（None 则各 API 用默认模型）

    返回:
        list[dict]: 每个 API 的验证结果
    """
    _load_env()

    if apis is None:
        apis = list(APIS.keys())

    results = []
    for api_name in apis:
        if api_name not in APIS:
            results.append({
                "api": api_name,
                "success": False,
                "error": f"Unknown API: {api_name}",
            })
            continue

        print(f"  [{api_name}] 正在验证...", file=sys.stderr)
        result = cross_model_verify(prompt, content, api=api_name, model=model)
        result["api"] = api_name
        results.append(result)

    return results


# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="跨模型验证工具 - 用不同模型审查交付物"
    )
    parser.add_argument(
        "--api", default="dashscope",
        choices=list(APIS.keys()),
        help="使用的 API (默认: dashscope)",
    )
    parser.add_argument(
        "--model", default=None,
        help="模型名 (默认按 API 自动选择)",
    )
    parser.add_argument(
        "--prompt-file", "-p", required=True,
        help="验证指令文件路径",
    )
    parser.add_argument(
        "--content-file", "-c", required=True,
        help="交付物内容文件路径",
    )
    parser.add_argument(
        "--output-file", "-o", default=None,
        help="输出文件路径 (默认输出到 stdout)",
    )
    parser.add_argument(
        "--multi", action="store_true",
        help="用所有可用 API 交叉验证",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=4096,
        help="最大输出 tokens (默认 4096)",
    )
    parser.add_argument(
        "--timeout", type=int, default=120,
        help="超时秒数 (默认 120)",
    )

    args = parser.parse_args()

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    content = Path(args.content_file).read_text(encoding="utf-8")

    if args.multi:
        results = cross_model_verify_multi(
            prompt, content,
        )
        output = []
        for r in results:
            api_name = r.get("api", "unknown")
            if r["success"]:
                output.append(f"=== {api_name} ({r['model']}) ===\n{r['content']}\n")
            else:
                output.append(f"=== {api_name} ===\nFAILED: {r['error']}\n")
        report = "\n".join(output)
    else:
        result = cross_model_verify(
            prompt, content,
            api=args.api,
            model=args.model,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        if result["success"]:
            report = f"[验证模型: {result['model']}]\n\n{result['content']}"
        else:
            report = f"验证失败: {result['error']}"
            sys.exit(1)

    if args.output_file:
        Path(args.output_file).write_text(report, encoding="utf-8")
        print(f"验证报告已保存到: {args.output_file}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
