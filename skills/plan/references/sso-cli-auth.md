# SSO CLI 认证（非交互式终端模式）

适用于所有需要 SSO 浏览器登录的 CLI 工具在非交互式终端中的认证流程。
以火山方舟 `arkcli` 为例（2026.7.29 验证通过）。

## 通用流程

```
步骤1: 生成授权URL     CLI tool auth login --no-browser
步骤2: 用户浏览器打开   URL → 登录 → 获取授权码
步骤3: 完成登录        CLI tool auth login --code <auth_code>
步骤4: 创建/验证profile  CLI tool profile create --no-interactive
```

## 详细步骤

### 步骤1：生成授权 URL

```bash
# 输出一个链接，让用户在浏览器中打开
arkcli auth login volc-sso --no-browser --format json
```

输出示例：
```json
{
  "authorize_url": "https://signin.volcengine.com/authorize/oauth/authorize?...",
  "expires_in_sec": 600,
  "next_command": "arkcli auth login --no-browser --code <authorization_code>"
}
```

### 步骤2：用户操作

用户打开授权 URL → 登录 → 浏览器显示 base64 授权码 → 复制发给 agent。

**注意**：授权码通常 10 分钟内有效。

### 步骤3：完成登录

```bash
arkcli auth login --no-browser --code "<base64_code>"
```

**常见失败**：授权码消费成功（显示"火山 SSO 认证成功!"）但 project 选择失败，报错：
```
激活火山身份失败: sso.ActivateIdentity ... 选择项目 (Project) cancelled: 非交互式终端
```

**原因**：auth login 成功后自动触发首次 profile 创建，但需要交互式选择 project。`--project-name` 全局标志不被 `auth login` 命令传递。

**修复**：auth 完成后手动创建 profile（步骤4）。

### 步骤4：创建 profile

```bash
# 需要提前知道 region 和 project 名称
arkcli profile create --type platform --project default --region cn-beijing \
  --set-default --no-interactive --format json
```

输出：
```json
{
  "created": "platform_cn-beijing_default",
  "is_default": true
}
```

## 验证

```bash
# 验证 SSO 状态
arkcli auth status --format json
# 关键字段: auth_method: sso, control_plane_auth.status: ok, logged_in: true

# 验证控制面命令
arkcli usage plan --format json    # 套餐用量查询
arkcli models list --format json   # 模型列表
arkcli billing list --start YYYY-MM --format json  # 账单
```

## 注意事项

1. **授权码一次有效** -- 消费后重复使用会报 "没有待完成的无浏览器登录会话"
2. **profile 创建后的凭证持久化** -- 凭证保存在 `~/.arkcli/` 目录（`.env` 含 STS token + refresh token），重启后仍有效，除非 STS 过期
3. **STS 过期处理** -- STS 过期后控制面命令自动用 refresh token 续期；如果 refresh token 也过期，需重新 SSO 登录
4. **控制面 vs 数据面** -- 控制面命令（usage/billing/models/plans）需要 SSO；数据面命令（+chat/+gen/+understand）只需要 API Key
