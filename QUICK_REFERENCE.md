# Android-MCP 快速参考

## 🚀 新功能速查

### Restart-Tool
```python
# 当遇到超时或设备无响应时使用
Restart-Tool()
```

### State-Tool with max_elements
```python
# 快速查看（20个元素）
State-Tool(use_vision=True, max_elements=20)

# 标准查看（50个元素，默认）
State-Tool(use_vision=True, max_elements=50)

# 详细查看（100个元素）
State-Tool(use_vision=False, max_elements=100)

# 最大查看（200个元素）
State-Tool(use_vision=False, max_elements=200)
```

## 🔧 常见问题解决

| 问题 | 解决方案 |
|------|---------|
| 返回"查询结果过长" | 使用 `max_elements=20` 减小返回数据 |
| State-Tool超时 | 1. 使用 `Restart-Tool()` <br> 2. 减小 `max_elements` 值 |
| 找不到元素 | 1. 增加 `max_elements` 值 <br> 2. 滚动页面后重新查询 |
| 设备无响应 | 使用 `Restart-Tool()` 重启连接 |

## 📊 性能建议

| 场景 | 推荐配置 |
|------|---------|
| 首次查看页面 | `max_elements=20-30` |
| 正常使用 | `max_elements=50` (默认) |
| 详细分析 | `max_elements=100` |
| 复杂页面 | 分批查询，每次20-30个元素 |

## 🎯 最佳实践

1. **从小到大**：先用小的 `max_elements` 值，需要时再增加
2. **避免频繁截图**：`use_vision=True` 会增加数据量
3. **遇到超时立即重启**：不要反复尝试相同操作
4. **分批获取**：通过滚动+小批量查询获取完整信息

## 📝 典型工作流

```python
# 1. 快速查看页面
State-Tool(use_vision=True, max_elements=20)

# 2. 如果超时，重启并重试
Restart-Tool()
State-Tool(use_vision=True, max_elements=15)

# 3. 找到目标元素后操作
Click-Tool(x=540, y=326)

# 4. 输入文本
Type-Tool(text="王者荣耀", x=540, y=326)

# 5. 验证结果
State-Tool(use_vision=True, max_elements=20)
```

## 🔍 调试技巧

```python
# 1. 检查设备连接
# 在终端运行: adb devices

# 2. 重启ADB服务
# 在终端运行: adb kill-server && adb start-server

# 3. 使用小的max_elements测试
State-Tool(use_vision=False, max_elements=5)

# 4. 逐步增加直到找到合适的值
State-Tool(use_vision=False, max_elements=10)
State-Tool(use_vision=False, max_elements=20)
```

## 📚 更多信息

- 详细使用指南: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- 更新日志: [CHANGELOG.md](CHANGELOG.md)
- 故障排除: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
