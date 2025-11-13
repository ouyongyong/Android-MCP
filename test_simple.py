#!/usr/bin/env python3
"""
简单的设备连接和操作测试
"""
import sys
import time

def test_basic_connection():
    print("=" * 60)
    print("测试1: 基本设备连接")
    print("=" * 60)
    
    try:
        import uiautomator2 as u2
        print("✓ uiautomator2 导入成功")
        
        print("\n连接设备...")
        start = time.time()
        device = u2.connect()
        elapsed = time.time() - start
        print(f"✓ 设备连接成功 (耗时: {elapsed:.2f}秒)")
        
        print("\n获取设备信息...")
        start = time.time()
        info = device.info
        elapsed = time.time() - start
        print(f"✓ 设备信息获取成功 (耗时: {elapsed:.2f}秒)")
        print(f"  - 产品名: {info.get('productName', 'Unknown')}")
        print(f"  - 型号: {info.get('model', 'Unknown')}")
        print(f"  - 屏幕: {info.get('displayWidth')}x{info.get('displayHeight')}")
        
        return device
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return None

def test_dump_hierarchy(device):
    print("\n" + "=" * 60)
    print("测试2: dump_hierarchy (这是最可能超时的操作)")
    print("=" * 60)
    
    try:
        print("\n调用 dump_hierarchy()...")
        start = time.time()
        xml = device.dump_hierarchy(compressed=False, pretty=False)
        elapsed = time.time() - start
        print(f"✓ dump_hierarchy 成功 (耗时: {elapsed:.2f}秒)")
        print(f"  - XML长度: {len(xml)} 字符")
        print(f"  - 前100字符: {xml[:100]}...")
        return True
    except Exception as e:
        print(f"✗ dump_hierarchy 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mobile_class():
    print("\n" + "=" * 60)
    print("测试3: Mobile类初始化")
    print("=" * 60)
    
    try:
        from src.mobile import Mobile
        print("✓ Mobile类导入成功")
        
        print("\n创建Mobile实例...")
        start = time.time()
        mobile = Mobile(device=None)
        elapsed = time.time() - start
        print(f"✓ Mobile实例创建成功 (耗时: {elapsed:.2f}秒)")
        
        print("\n调用 get_state()...")
        start = time.time()
        state = mobile.get_state(use_vision=False)
        elapsed = time.time() - start
        print(f"✓ get_state 成功 (耗时: {elapsed:.2f}秒)")
        print(f"  - 可交互元素数量: {len(state.tree_state.interactive_elements)}")
        
        return True
    except Exception as e:
        print(f"✗ Mobile类测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n🔍 Android MCP 诊断测试")
    print("此测试将帮助定位超时问题的根源\n")
    
    # 测试1: 基本连接
    device = test_basic_connection()
    if not device:
        print("\n❌ 设备连接失败，无法继续测试")
        return 1
    
    # 测试2: dump_hierarchy
    if not test_dump_hierarchy(device):
        print("\n❌ dump_hierarchy 失败 - 这很可能是MCP超时的原因！")
        print("\n💡 建议:")
        print("1. 检查设备是否响应缓慢")
        print("2. 尝试重启设备/模拟器")
        print("3. 检查ADB连接是否稳定")
        return 1
    
    # 测试3: Mobile类
    if not test_mobile_class():
        print("\n❌ Mobile类测试失败")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)
    print("\n如果MCP仍然超时，问题可能在于:")
    print("1. MCP通信协议层面")
    print("2. Claude Desktop的超时设置太短")
    print("3. 需要查看Claude Desktop的日志文件")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
