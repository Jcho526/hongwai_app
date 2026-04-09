#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热成像报告生成 API 客户端示例
"""

import requests
import json
from pathlib import Path


class ThermalAPIClient:
    """热成像 API 客户端"""
    
    def __init__(self, base_url='http://localhost:5000'):
        """
        初始化客户端
        
        Args:
            base_url: API 服务地址，默认 http://localhost:5000
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """健康检查"""
        response = self.session.get(f'{self.base_url}/health')
        return response.json()
    
    def get_status(self):
        """获取服务状态"""
        response = self.session.get(f'{self.base_url}/api/v1/status')
        return response.json()
    
    def generate_pdf(self, image_path, patient_name=None, patient_age=None, 
                     patient_gender=None, patient_id=None, output_path=None):
        """
        生成单个 PDF 报告
        
        Args:
            image_path: 热成像图片路径
            patient_name: 患者名
            patient_age: 患者年龄
            patient_gender: 患者性别
            patient_id: 患者 ID
            output_path: 输出 PDF 路径（可选，不指定则为默认路径）
        
        Returns:
            PDF 文件内容（二进制）或错误信息
        """
        
        # 检查文件是否存在
        if not Path(image_path).exists():
            return {'success': False, 'error': f'文件不存在: {image_path}'}
        
        # 准备请求数据
        files = {'file': open(image_path, 'rb')}
        data = {}
        
        if patient_name:
            data['patient_name'] = patient_name
        if patient_age:
            data['patient_age'] = str(patient_age)
        if patient_gender:
            data['patient_gender'] = patient_gender
        if patient_id:
            data['patient_id'] = patient_id
        
        # 发送请求
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/generate-pdf',
                files=files,
                data=data,
                timeout=300  # 5分钟超时
            )
            
            files['file'].close()
            
            # 处理响应
            if response.status_code == 200:
                # 提取文件名
                content_disposition = response.headers.get('content-disposition', '')
                if 'filename=' in content_disposition:
                    pdf_filename = content_disposition.split('filename=')[1].strip('"')
                else:
                    pdf_filename = f"热图分析报告_{patient_name or 'unknown'}.pdf"
                
                # 保存文件
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ PDF 已保存: {output_path}")
                    return {'success': True, 'pdf_path': output_path}
                else:
                    return {
                        'success': True,
                        'content': response.content,
                        'filename': pdf_filename
                    }
            else:
                error_data = response.json()
                print(f"❌ 生成失败: {error_data.get('error')}")
                return {'success': False, 'error': error_data.get('error')}
        
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def batch_generate(self, patients_list):
        """
        批量生成 PDF 报告
        
        Args:
            patients_list: 患者列表，每个患者包含：
                - image_path: 图片路径（必需）
                - patient_name: 患者名（可选）
                - patient_age: 患者年龄（可选）
                - patient_gender: 患者性别（可选）
        
        Returns:
            API 响应字典
        """
        
        payload = {'patients': patients_list}
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/v1/batch-generate',
                json=payload,
                timeout=600  # 10分钟超时
            )
            
            return response.json()
        
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
            return {'success': False, 'error': str(e)}


# 使用示例
if __name__ == '__main__':
    # 初始化客户端
    client = ThermalAPIClient('http://localhost:5000')
    
    # 1. 健康检查
    print("=" * 60)
    print("🔥 热成像报告生成 API 客户端")
    print("=" * 60)
    
    print("\n1️⃣ 健康检查...")
    try:
        health = client.health_check()
        print(f"✅ 服务状态: {health.get('status')}")
        print(f"   消息: {health.get('message')}")
    except Exception as e:
        print(f"❌ 服务不可用: {e}")
        print("   请确保已启动 API 服务: python thermal_api.py")
        exit(1)
    
    # 2. 获取服务状态
    print("\n2️⃣ 获取服务状态...")
    status = client.get_status()
    print(f"✅ 服务版本: {status.get('version')}")
    print(f"   支持格式: {', '.join(status.get('supported_formats', []))}")
    print(f"   最大文件: {status.get('max_file_size_mb', 0):.0f}MB")
    
    # 3. 生成单个 PDF
    print("\n3️⃣ 生成单个 PDF 报告...")
    image_path = 'Snipaste_2026-03-22_11-27-51.png'
    
    if Path(image_path).exists():
        result = client.generate_pdf(
            image_path=image_path,
            patient_name='赵女士',
            patient_age=35,
            patient_gender='女',
            patient_id='PT001',
            output_path='report_sample.pdf'
        )
        
        if result.get('success'):
            print(f"✅ 报告生成成功")
            print(f"   路径: {result.get('pdf_path')}")
        else:
            print(f"❌ 生成失败: {result.get('error')}")
    else:
        print(f"⚠️ 文件不存在: {image_path}")
    
    # 4. 批量生成
    print("\n4️⃣ 批量生成 PDF 报告...")
    patients = [
        {
            'image_path': 'Snipaste_2026-03-22_11-27-51.png',
            'patient_name': '患者1',
            'patient_age': 30,
            'patient_gender': '男'
        },
        {
            'image_path': 'Snipaste_2026-03-22_11-27-51.png',
            'patient_name': '患者2',
            'patient_age': 28,
            'patient_gender': '女'
        }
    ]
    
    batch_result = client.batch_generate(patients)
    if batch_result.get('success'):
        print(f"✅ 批量生成完成")
        print(f"   总数: {batch_result.get('total')}")
        print(f"   成功: {batch_result.get('success_count')}")
        print(f"   失败: {batch_result.get('failed_count')}")
    else:
        print(f"❌ 批量生成失败: {batch_result.get('error')}")
    
    print("\n" + "=" * 60)
