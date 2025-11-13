# 🔧 Android MCP 超时问题修复

## 问题诊断

客户端能够连接到MCP服务器，但调用工具时出现超时错误。

## 根本原因

**主要问题**：在 `src/tree/__init__.py` 第18行有一个 `print(tree_string)` 语句，它会将整个XML树输出到标准输出（stdout）。

由于MCP协议通过stdio（标准输入/输出）进行通信，任何意外的stdout输出都会干扰MCP协议消息，导致：
- 客户端无法正确解析响应
- 工具调用超时
- 通信失败

## 已实施的修复

### 1. 移除干扰性的print语句 ✅
**文件**: `src/tree/__init__.py`
- 移除了 `print(tree_string)` 语句
- 添加了注释说明原因

### 2. 优化启动时间 ✅
**文件**: `main.py`
- 移除了 `lifespan` 函数中不必要的 `await asyncio.sleep(1)`
- 减少了服务器启动延迟

### 3. 改进错误处理 ✅
**文件**: `main.py`
- 为所有工具函数添加了try-except错误处理
- 提供更详细的错误信息
- 在设备连接失败时提供有用的诊断信息

### 4. 添加诊断日志 ✅
**文件**: `main.py`
- 使用 `sys.stderr` 输出日志（不干扰MCP通信）
- 在设备连接时显示连接状态
- 连接失败时提供故障排除步骤

### 5. 修复Type-Tool功能 ✅
**文件**: `main.py`
- 修复了坐标参数未使用的问题
- 现在会在输入文本前点击指定坐标以聚焦输入框

## 测试步骤

1. **重启Claude Desktop**
   ```bash
   # 完全退出并重新启动Claude Desktop应用
   ```

2. **验证连接**
   - 打开Claude Desktop
   - 检查是否能看到 "android-mcp" 集成
   - 查看日志确认设备连接成功

3. **测试工具调用**
   尝试以下命令：
   ```
   - "获取设备状态" (State-Tool)
   - "点击坐标 (100, 200)" (Click-Tool)
   - "按返回键" (Press-Tool)
   ```

## 日志位置

如果仍有问题，检查Claude Desktop日志：
- **macOS**: `~/Library/Logs/Claude/mcp*.log`
- **Windows**: `%APPDATA%\Claude\logs\mcp*.log`

## 常见问题排查

### 如果仍然超时：

1. **检查设备连接**
   ```bash
   adb devices
   ```
   应该显示你的设备

2. **检查uiautomator2**
   ```bash
   python -c "import uiautomator2 as u2; d = u2.connect(); print(d.info)"
   ```

3. **查看stderr日志**
   Claude Desktop的MCP日志会包含stderr输出，检查是否有连接错误

4. **验证uv路径**
   确保Claude Desktop配置中的uv路径正确：
   ```bash
   which uv
   ```

## 性能优化建议

- 首次调用 `State-Tool` 时可能较慢（需要dump整个UI树）
- 建议在不需要视觉信息时设置 `use_vision=False`
- 避免频繁调用 `State-Tool`，尽量缓存状态信息

## 修复总结

✅ 移除了干扰MCP通信的print语句  
✅ 添加了完整的错误处理  
✅ 改进了日志记录（使用stderr）  
✅ 优化了启动时间  
✅ 修复了Type-Tool的坐标功能  

现在MCP服务器应该能够正常响应工具调用，不再出现超时问题。
