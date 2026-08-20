# 限速规则详解（写死，不可绕过）

> 来源：文献云平台限制（2026.8.6 确认）
> 目的：防止平台封号或限流

## 规则总览

| 规则 | 值 | 实现方式 |
|------|-----|---------|
| 每篇最小间隔 | ≥ 3 秒 | `time.sleep(3)` |
| 1分钟最多 | ≤ 20 篇 | 计数器+时间窗口 |
| 3分钟最多 | ≤ 50 篇 | 计数器+时间窗口 |
| 每5篇额外休息 | 10 秒 | `if len(downloaded) % 5 == 0: time.sleep(10)` |
| 下载超时重试等待 | 60 秒 | 等待后重试1次 |
| 错误重试间隔 | 5 秒 | 下载失败后等待 |

## 为什么这些规则是写死的

1. **平台有每日下载额度**：约30-50篇/天，超过后显示"您今天的下载次数已用尽"
2. **快速请求会触发限流**：点击后20秒无响应
3. **非CSSCI跳过也要等**：防止快速跳过导致实际间隔过短

## 实现代码

### 限速器类

```python
import time, threading

class RateLimiter:
    def __init__(self):
        self.timestamps = []
        self.lock = threading.Lock()

    def wait(self):
        """在下载前调用，确保符合限速规则"""
        with self.lock:
            now = time.time()
            # 清理超过3分钟的记录
            self.timestamps = [t for t in self.timestamps if now - t < 180]
            # 检查3分钟窗口
            if len(self.timestamps) >= 50:
                sleep_time = 180 - (now - self.timestamps[0]) + 1
                print(f"⏳ 3分钟窗口已达50篇，等待{sleep_time:.0f}秒...")
            else:
                # 检查1分钟窗口
                last_60s = [t for t in self.timestamps if now - t < 60]
                if len(last_60s) >= 20:
                    sleep_time = 60 - (now - last_60s[0]) + 1
                    print(f"⏳ 1分钟窗口已达20篇，等待{sleep_time:.0f}秒...")
                else:
                    # 最小间隔
                    if self.timestamps:
                        sleep_time = 3 - (now - self.timestamps[-1])
                        if sleep_time > 0:
                            print(f"⏳ 间隔等待{sleep_time:.1f}秒...")
                            time.sleep(sleep_time)
                            return
                    sleep_time = 0
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.timestamps.append(time.time())
```

### 使用方式

```python
rate = RateLimiter()

for row in rows:
    # CSSCI过滤
    if not is_cssci(journal):
        time.sleep(3)  # ⭐ 跳过也要等3秒！
        continue

    # 限速等待
    rate.wait()

    # 每5篇额外休息
    if len(downloaded) > 0 and len(downloaded) % 5 == 0:
        print(f"💤 每5篇防限流休息10秒...")
        time.sleep(10)

    # 下载
    with page.expect_download(timeout=30000) as dl_info:
        dl_btn.click()
    download = dl_info.value
    download.save_as(save_path)
    downloaded.append(...)

    time.sleep(1)  # 下载后额外防抖
```

### 错误重试

```python
for attempt in range(2):
    try:
        with page.expect_download(timeout=30000) as dl_info:
            dl_btn.click()
        download = dl_info.value
        break
    except Exception as e:
        if attempt == 0:
            print(f"⚠️ 下载超时，等待60秒后重试...")
            time.sleep(60)
        else:
            raise e
```

## 违反规则的后果

| 违反行为 | 后果 |
|---------|------|
| 间隔<3秒 | 平台开始对下载请求限速，点击后20秒无响应 |
| 1分钟>20篇 | 平台临时封禁下载功能（10-30分钟） |
| 3分钟>50篇 | 平台永久封禁当日下载额度 |
| 不加间隔跳过非CSSCI | 实际间隔过短，触发限流 |

## 调试技巧

1. **打印时间戳**：每篇下载后打印 `time.time()`，验证间隔
2. **日志分析**：检查日志中时间戳间隔是否≥3秒
3. **渐进测试**：先测试单篇下载，确认成功后再批量
4. **监控额度**：每10篇检查一次是否触发"下载次数已用尽"

## 参考

- `references/cssci_journals.py` - CSSCI过滤名单
- `references/kns8_queryjson.md` - QueryJson结构
- `scripts/pw_download.py` - 完整下载脚本（含限速+CSSCI过滤）
