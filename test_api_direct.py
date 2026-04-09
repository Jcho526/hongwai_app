#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试 API 的脚本
测试 base64 上传和 PDF 生成功能
"""

import requests
import base64
import json
import time
from pathlib import Path

# API 配置
API_URL = "http://localhost:5000"
API_ENDPOINT = f"{API_URL}/api/v1/generate-pdf"

def test_api_health():
    """测试 API 健康状态"""
    print("=" * 60)
    print("1️⃣  测试 API 健康检查")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"✅ API 健康检查: {response.status_code}")
        print(f"   响应: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API 健康检查失败: {e}")
        return False

def test_api_with_base64():
    """测试使用 base64 上传图片的 API"""
    print("\n" + "=" * 60)
    print("2️⃣  测试 API 的 Base64 上传功能")
    print("=" * 60)
    
    # 寻找示例图片
    sample_images = list(Path("C:\\Users\\1\\Desktop\\新\\static\\icons").glob("*.png"))
    
    if not sample_images:
        print("❌ 未找到示例图片")
        return False
    
    sample_image = sample_images[0]
    print(f"📷 使用示例图片: {sample_image.name}")
    
    try:
        # 读取图片并转换为 base64
        with open(sample_image, "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
        
        print(f"📊 图片大小: {len(image_data)} 字节")
        print(f"🔐 Base64 编码长度: {len(image_base64)} 字符")
        
        # 准备请求数据
        request_data = {
            "image_base64": image_base64,
            "person_name": "测试用户",
            "person_id": "TEST_001",
            "age": 35,
            "gender": "男",
            "diagnosis": "测试诊断",
            "template": "universal"
        }
        
        print("\n📤 发送请求到 API...")
        print(f"   URL: {API_ENDPOINT}")
        print(f"   方法: POST")
        print(f"   Content-Type: application/json")
        
        # 发送请求
        start_time = time.time()
        response = requests.post(
            API_ENDPOINT,
            json=request_data,
            timeout=300,
            headers={"Content-Type": "application/json"}
        )
        elapsed_time = time.time() - start_time
        
        print(f"\n📥 收到响应 (耗时: {elapsed_time:.2f} 秒)")
        print(f"   状态码: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            # 检查是否是 PDF 文件
            if 'application/pdf' in response.headers.get('Content-Type', ''):
                print(f"\n✅ PDF 生成成功!")
                print(f"   响应大小: {len(response.content)} 字节")
                
                # 保存 PDF 文件用于验证
                pdf_save_path = "test_output.pdf"
                with open(pdf_save_path, 'wb') as f:
                    f.write(response.content)
                print(f"   📁 PDF 已保存到: {pdf_save_path}")
                return True
            else:
                # 尝试解析为 JSON
                try:
                    result = response.json()
                    print(f"   响应: {result}")
                    if result.get('success'):
                        print(f"\n✅ PDF 生成成功!")
                        return True
                    else:
                        print(f"\n❌ PDF 生成失败: {result.get('error', 'Unknown error')}")
                        return False
                except:
                    print(f"❌ 无法解析响应")
                    print(f"   响应内容: {response.text[:200]}")
                    return False
        else:
            print(f"❌ API 返回错误: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_status():
    """测试 API 状态端点"""
    print("\n" + "=" * 60)
    print("3️⃣  测试 API 状态")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/api/v1/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ API 状态: {json.dumps(status, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ 获取状态失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取状态失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n")
    print("🚀 热成像 API 端到端测试")
    print("=" * 60)
    
    results = []
    
    # 1. 测试 API 健康
    results.append(("API 健康检查", test_api_health()))
    
    # 2. 测试 base64 上传和 PDF 生成
    results.append(("Base64 上传和 PDF 生成", test_api_with_base64()))
    
    # 3. 测试 API 状态
    results.append(("API 状态", test_api_status()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print(f"\n总体: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过! API 可以正常使用。")
    else:
        print("\n⚠️  部分测试失败，请检查 API 配置和日志。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
