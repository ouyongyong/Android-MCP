#!/usr/bin/env python3
"""
专门测试截图功能的脚本
用于验证优化后的截图是否会触发 input length too long 错误
"""
import sys
import time
from src.mobile import Mobile

def test_screenshot_without_vision():
    """测试不带vision的截图"""
    print("=" * 60)
    print("测试1: 不带Vision的截图 (仅获取树状结构)")
    print("=" * 60)
    
    try:
        mobile = Mobile(device=None)
        print("✓ Mobile连接成功")
        
        print("\n调用 get_state(use_vision=False)...")
        start = time.time()
        state = mobile.get_state(use_vision=False, max_elements=30)
        elapsed = time.time() - start
        
        print(f"✓ 成功 (耗时: {elapsed:.2f}秒)")
        print(f"  - 可交互元素数: {len(state.tree_state.interactive_elements)}")
        print(f"  - 是否包含截图: {state.screenshot is not None}")
        
        if state.screenshot:
            print(f"  - 截图大小: {len(state.screenshot)/1024:.1f}KB")
        
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_screenshot_with_vision():
    """测试带vision的截图（这是触发错误的操作）"""
    print("\n" + "=" * 60)
    print("测试2: 带Vision的截图 (包含注释的可视化截图)")
    print("=" * 60)
    
    try:
        mobile = Mobile(device=None)
        print("✓ Mobile连接成功")
        
        print("\n调用 get_state(use_vision=True, max_elements=15)...")
        print("  (这个操作最容易触发 'input length too long' 错误)")
        start = time.time()
        state = mobile.get_state(use_vision=True, max_elements=15)
        elapsed = time.time() - start
        
        print(f"✓ 成功 (耗时: {elapsed:.2f}秒)")
        print(f"  - 可交互元素数: {len(state.tree_state.interactive_elements)}")
        print(f"  - 是否包含截图: {state.screenshot is not None}")
        
        if state.screenshot:
            size_kb = len(state.screenshot) / 1024
            print(f"  - 截图大小: {size_kb:.1f}KB")
            if size_kb > 500:
                print(f"  ⚠️  警告: 截图超过500KB，可能导致MCP限制错误")
            else:
                print(f"  ✓ 截图大小在安全范围内 (<500KB)")
        
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_screenshot_with_different_elements():
    """测试不同元素数量的截图"""
    print("\n" + "=" * 60)
    print("测试3: 不同元素数量的Vision截图")
    print("=" * 60)
    
    for max_elem in [5, 10, 15, 20]:
        try:
            mobile = Mobile(device=None)
            
            print(f"\n测试 max_elements={max_elem}...")
            start = time.time()
            state = mobile.get_state(use_vision=True, max_elements=max_elem)
            elapsed = time.time() - start
            
            if state.screenshot:
                size_kb = len(state.screenshot) / 1024
                print(f"  ✓ 成功 (耗时: {elapsed:.2f}秒, 大小: {size_kb:.1f}KB)")
            else:
                print(f"  ✓ 成功 (耗时: {elapsed:.2f}秒, 无截图)")
        except Exception as e:
            print(f"  ✗ 失败: {e}")
            return False
    
    return True

def main():
    print("\n📸 Android MCP 截图功能测试")
    print("此测试用于验证优化后的截图是否解决了 'input length too long' 问题\n")
    
    # 测试1: 不带vision
    if not test_screenshot_without_vision():
        print("\n❌ 基础截图测试失败")
        return 1
    
    # 测试2: 带vision（关键测试）
    if not test_screenshot_with_vision():
        print("\n❌ Vision截图测试失败")
        print("这可能仍然会在MCP层触发错误")
        return 1
    
    # 测试3: 不同元素数量
    if not test_screenshot_with_different_elements():
        print("\n❌ 不同元素数量的测试失败")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ 所有截图测试通过！")
    print("=" * 60)
    print("\n优化效果:")
    print("✓ 图像缩放从0.5改为0.4")
    print("✓ JPEG质量从75%降低到60%")
    print("✓ 添加了自适应压缩（超过500KB会继续降低质量）")
    print("✓ Vision模式最大元素数从20降低到15")
    print("\n现在可以尝试在MCP中使用截图功能了！")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
