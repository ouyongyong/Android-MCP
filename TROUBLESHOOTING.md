# 🔍 Android MCP 超时问题诊断指南

## 当前状态
✅ 已修复代码中的print语句干扰问题  
✅ 已添加详细的stderr日志  
❌ MCP工具调用仍然超时  

## 诊断步骤

### 步骤1: 运行诊断测试脚本

```bash
cd /Users/kilaou/Documents/UGit/Android-MCP
uv run test_simple.py
```

这个脚本会测试:
1. 设备连接是否正常
2. `dump_hierarchy()` 是否超时（最可能的原因）
3. Mobile类是否工作正常

**预期结果**: 所有测试应该在几秒内完成

**如果测试失败**: 记录哪一步失败以及耗时

### 步骤2: 检查Claude Desktop日志

查看MCP服务器的stderr输出:

```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp-server-android-mcp.log

# 或者查看所有MCP日志
ls -lt ~/Library/Logs/Claude/mcp*.log | head -5
```

**查找内容**:
- `[Android-MCP] Connecting to device...` - 设备连接开始
- `[Android-MCP] Successfully connected to...` - 设备连接成功
- `[State-Tool] Starting...` - 工具调用开始
- `[Mobile.get_state] Getting tree state...` - 获取UI树
- 任何错误信息

### 步骤3: 检查设备响应速度

```bash
# 测试ADB连接速度
time adb shell dumpsys window windows | grep -E 'mCurrentFocus'

# 测试uiautomator2
time python3 -c "import uiautomator2 as u2; d=u2.connect(); print(len(d.dump_hierarchy()))"
```

**正常耗时**: 应该在1-3秒内完成  
**如果超过5秒**: 设备响应太慢，这会导致MCP超时

## 可能的原因和解决方案

### 原因1: dump_hierarchy() 太慢 ⭐ 最可能

**症状**: test_simple.py 在测试2卡住或超时

**解决方案**:
1. 重启Android设备/模拟器
2. 清理设备上的后台应用
3. 使用更快的设备/模拟器
4. 增加MCP超时时间（见下文）

### 原因2: 设备连接不稳定

**症状**: test_simple.py 在测试1失败或很慢

**解决方案**:
```bash
# 重启ADB服务
adb kill-server
adb start-server
adb devices

# 重新安装uiautomator2
python3 -m uiautomator2 init
```

### 原因3: MCP超时设置太短

**症状**: 本地测试都通过，但MCP调用超时

**解决方案**: 修改 `main.py` 添加超时配置

```python
# 在 mcp.run() 之前添加
import os
os.environ['MCP_TIMEOUT'] = '30000'  # 30秒超时
```

### 原因4: UI树太大

**症状**: dump_hierarchy 返回非常大的XML（>1MB）

**解决方案**: 优化get_state方法，只返回必要信息

## 临时解决方案：简化State-Tool

如果问题持续，可以创建一个简化版本的State-Tool:

```python
@mcp.tool('State-Tool-Simple',description='Get basic device state without full UI tree')
def state_tool_simple():
    try:
        # 只返回当前应用信息，不获取完整UI树
        current_app = device.app_current()
        return f"Current app: {current_app['package']}"
    except Exception as e:
        raise RuntimeError(f'Failed: {str(e)}')
```

## 下一步行动

1. **立即执行**: 运行 `uv run test_simple.py`
2. **查看日志**: 检查Claude Desktop的MCP日志
3. **报告结果**: 记录哪个测试失败以及具体耗时
4. **尝试简化**: 如果dump_hierarchy太慢，使用简化版工具

## 性能基准

正常情况下的耗时应该是:
- 设备连接: < 1秒
- dump_hierarchy: 1-3秒
- get_state: 2-4秒
- MCP工具调用总耗时: < 10秒

如果任何步骤超过这些时间，就需要优化或更换设备。

## 联系信息

如果问题仍未解决，请提供:
1. `test_simple.py` 的完整输出
2. Claude Desktop MCP日志的相关部分
3. 设备型号和Android版本
4. `adb devices` 的输出
