# Android-MCP 使用指南

## 新增功能

### 1. Restart-Tool - 重启设备连接

当MCP服务出现超时或设备无响应时，使用此工具重新建立连接。

**使用场景：**
- 返回"mcp工具查询结果返回过长，请修改参数尝试缩小查询范围"后出现超时
- 设备连接不稳定
- 长时间运行后设备无响应

**使用方法：**
```python
# 通过MCP调用
Restart-Tool()
```

**返回示例：**
```
Device connection restarted successfully. Connected to Pixel 6
```

---

### 2. State-Tool 优化 - 限制返回元素数量

为了防止返回数据过大导致超时，State-Tool现在支持`max_elements`参数。

**参数说明：**
- `use_vision` (bool): 是否包含截图，默认False
- `max_elements` (int): 最大返回元素数量，默认50，最大200

**使用方法：**

```python
# 只返回前20个交互元素（快速查看）
State-Tool(use_vision=False, max_elements=20)

# 返回前50个元素并包含截图（默认）
State-Tool(use_vision=True, max_elements=50)

# 返回更多元素（最多200个）
State-Tool(use_vision=False, max_elements=100)
```

**最佳实践：**

1. **首次查看页面**：使用较小的`max_elements`值（20-30）快速了解页面结构
2. **详细分析**：根据需要逐步增加`max_elements`值
3. **遇到超时**：
   - 减小`max_elements`值
   - 如果仍然超时，使用`Restart-Tool`重启连接
   - 重启后再次尝试，使用更小的`max_elements`值

---

## 典型使用流程

### 场景1：正常使用
```python
# 1. 获取设备状态（默认50个元素）
State-Tool(use_vision=True)

# 2. 点击某个元素
Click-Tool(x=540, y=326)

# 3. 输入文本
Type-Tool(text="王者荣耀", x=540, y=326)
```

### 场景2：遇到超时问题
```python
# 1. 尝试获取状态，但返回过长导致超时
State-Tool(use_vision=True)  # 超时！

# 2. 重启设备连接
Restart-Tool()

# 3. 使用更小的max_elements重试
State-Tool(use_vision=True, max_elements=20)

# 4. 如果需要更多信息，逐步增加
State-Tool(use_vision=False, max_elements=50)
```

### 场景3：复杂页面分析
```python
# 1. 先快速查看页面顶部元素
State-Tool(use_vision=True, max_elements=15)

# 2. 如果需要，滚动页面
Swipe-Tool(x1=540, y1=1500, x2=540, y2=500)

# 3. 再次查看新显示的元素
State-Tool(use_vision=True, max_elements=15)
```

---

## 性能优化建议

1. **优先使用小的max_elements值**：从20开始，根据需要增加
2. **避免频繁使用use_vision=True**：截图会增加数据传输量
3. **遇到超时立即重启**：不要反复尝试相同的操作
4. **分批获取信息**：通过滚动+小批量查询的方式获取完整页面信息

---

## 故障排除

### 问题：State-Tool一直超时
**解决方案：**
1. 使用`Restart-Tool`重启连接
2. 将`max_elements`设置为10-20
3. 暂时不使用`use_vision=True`

### 问题：重启后仍然超时
**解决方案：**
1. 检查设备连接：`adb devices`
2. 检查设备是否卡死，手动操作设备
3. 重启ADB服务：`adb kill-server && adb start-server`
4. 重启MCP服务器

### 问题：找不到想要的元素
**解决方案：**
1. 增加`max_elements`值
2. 滚动页面后再次查询
3. 使用`use_vision=True`查看截图确认元素位置

---

## 技术细节

### max_elements的工作原理
- 限制从UI树中提取的交互元素数量
- 按照UI树的遍历顺序返回前N个元素
- 通常前面的元素是页面顶部和主要交互区域

### Restart-Tool的工作原理
- 重新初始化uiautomator2连接
- 清除可能的缓存和挂起状态
- 重新获取设备信息

---

## 更新日志

### v1.1.0 (2025-11-12)
- ✨ 新增 `Restart-Tool` 用于重启设备连接
- ✨ `State-Tool` 新增 `max_elements` 参数限制返回数据量
- 🐛 修复长时间运行后超时问题
- ⚡ 优化性能，减少大数据传输导致的超时
