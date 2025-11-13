#!/usr/bin/env python3
"""
测试新增的Restart-Tool和max_elements功能
"""

from src.mobile import Mobile
import sys

def test_max_elements():
    """测试max_elements参数"""
    print("=" * 50)
    print("测试 max_elements 功能")
    print("=" * 50)
    
    try:
        # 连接设备
        print("\n1. 连接设备...")
        mobile = Mobile(device=None)
        device = mobile.get_device()
        print(f"✓ 已连接到: {device.info.get('productName', 'Unknown')}")
        
        # 测试不同的max_elements值
        test_values = [10, 20, 50]
        
        for max_elem in test_values:
            print(f"\n2. 获取设备状态 (max_elements={max_elem})...")
            state = mobile.get_state(use_vision=False, max_elements=max_elem)
            element_count = len(state.tree_state.interactive_elements)
            print(f"✓ 返回了 {element_count} 个交互元素")
            
            if element_count > max_elem:
                print(f"✗ 错误: 返回元素数量 ({element_count}) 超过限制 ({max_elem})")
                return False
            else:
                print(f"✓ 元素数量符合限制")
        
        print("\n" + "=" * 50)
        print("✓ max_elements 功能测试通过")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_restart():
    """测试重启功能"""
    print("\n" + "=" * 50)
    print("测试 Restart 功能")
    print("=" * 50)
    
    try:
        # 第一次连接
        print("\n1. 首次连接设备...")
        mobile1 = Mobile(device=None)
        device1 = mobile1.get_device()
        print(f"✓ 已连接到: {device1.info.get('productName', 'Unknown')}")
        
        # 获取状态
        print("\n2. 获取设备状态...")
        state1 = mobile1.get_state(use_vision=False, max_elements=10)
        print(f"✓ 获取到 {len(state1.tree_state.interactive_elements)} 个元素")
        
        # 模拟重启
        print("\n3. 模拟重启连接...")
        mobile2 = Mobile(device=None)
        device2 = mobile2.get_device()
        print(f"✓ 重新连接到: {device2.info.get('productName', 'Unknown')}")
        
        # 再次获取状态
        print("\n4. 重启后获取设备状态...")
        state2 = mobile2.get_state(use_vision=False, max_elements=10)
        print(f"✓ 获取到 {len(state2.tree_state.interactive_elements)} 个元素")
        
        print("\n" + "=" * 50)
        print("✓ Restart 功能测试通过")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n开始测试 Android-MCP 新功能...\n")
    
    # 测试max_elements
    test1_passed = test_max_elements()
    
    # 测试restart
    test2_passed = test_restart()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"max_elements 功能: {'✓ 通过' if test1_passed else '✗ 失败'}")
    print(f"Restart 功能: {'✓ 通过' if test2_passed else '✗ 失败'}")
    print("=" * 50)
    
    sys.exit(0 if (test1_passed and test2_passed) else 1)
