#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热成像 API 集成测试脚本
用于验证 API 的各项功能
"""

import subprocess
import json
import time
import sys
from pathlib import Path


class APITester:
    """API 集成测试类"""
    
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.test_results = []
    
    def log(self, message, level='info'):
        """输出日志"""
        colors = {
            'info': '\033[94m',      # 蓝色
            'success': '\033[92m',    # 绿色
            'warning': '\033[93m',    # 黄色
            'error': '\033[91m',      # 红色
            'reset': '\033[0m'
        }
        
        color = colors.get(level, colors['info'])
        emoji = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }[level]
        
        print(f"{emoji} {color}{message}{colors['reset']}")
    
    def test_health_check(self):
        """测试健康检查"""
        self.log("测试: 健康检查", 'info')
        
        try:
            result = subprocess.run(
                ['curl', '-s', f'{self.base_url}/health'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('status') == 'healthy':
                    self.log("✓ 服务健康检查通过", 'success')
                    self.test_results.append(('health_check', True))
                    return True
                else:
                    self.log(f"✗ 意外响应: {data}", 'error')
                    self.test_results.append(('health_check', False))
                    return False
            else:
                self.log(f"✗ 请求失败: {result.stderr}", 'error')
                self.test_results.append(('health_check', False))
                return False
        
        except Exception as e:
            self.log(f"✗ 错误: {str(e)}", 'error')
            self.test_results.append(('health_check', False))
            return False
    
    def test_status_api(self):
        """测试服务状态 API"""
        self.log("测试: 服务状态 API", 'info')
        
        try:
            result = subprocess.run(
                ['curl', '-s', f'{self.base_url}/api/v1/status'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('status') == 'success':
                    version = data.get('version', 'unknown')
                    formats = data.get('supported_formats', [])
                    self.log(f"✓ 版本: {version}, 支持格式: {', '.join(formats)}", 'success')
                    self.test_results.append(('status_api', True))
                    return True
                else:
                    self.log(f"✗ 意外响应: {data}", 'error')
                    self.test_results.append(('status_api', False))
                    return False
            else:
                self.log(f"✗ 请求失败", 'error')
                self.test_results.append(('status_api', False))
                return False
        
        except Exception as e:
            self.log(f"✗ 错误: {str(e)}", 'error')
            self.test_results.append(('status_api', False))
            return False
    
    def test_generate_pdf(self, image_path='Snipaste_2026-03-22_11-27-51.png'):
        """测试单个 PDF 生成"""
        self.log(f"测试: 单个 PDF 生成 (文件: {image_path})", 'info')
        
        if not Path(image_path).exists():
            self.log(f"✗ 文件不存在: {image_path}", 'warning')
            self.log(f"  你可以使用任何 PNG/JPG 文件进行测试", 'info')
            self.test_results.append(('generate_pdf', False))
            return False
        
        try:
            # 准备 curl 命令
            cmd = [
                'curl', '-s', '-X', 'POST',
                f'{self.base_url}/api/v1/generate-pdf',
                '-F', f'file=@{image_path}',
                '-F', 'patient_name=测试患者',
                '-F', 'patient_age=30',
                '-F', 'patient_gender=男',
                '-F', 'patient_id=TEST001',
                '-o', 'test_output.pdf'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                if Path('test_output.pdf').exists():
                    size_kb = Path('test_output.pdf').stat().st_size / 1024
                    self.log(f"✓ PDF 生成成功 (大小: {size_kb:.1f}KB)", 'success')
                    self.test_results.append(('generate_pdf', True))
                    return True
                else:
                    self.log("✗ PDF 文件生成失败", 'error')
                    self.test_results.append(('generate_pdf', False))
                    return False
            else:
                self.log(f"✗ 请求失败: {result.stderr}", 'error')
                self.test_results.append(('generate_pdf', False))
                return False
        
        except Exception as e:
            self.log(f"✗ 错误: {str(e)}", 'error')
            self.test_results.append(('generate_pdf', False))
            return False
    
    def test_batch_generate(self, image_path='Snipaste_2026-03-22_11-27-51.png'):
        """测试批量 PDF 生成"""
        self.log("测试: 批量 PDF 生成", 'info')
        
        if not Path(image_path).exists():
            self.log(f"✗ 文件不存在: {image_path}", 'warning')
            self.test_results.append(('batch_generate', False))
            return False
        
        try:
            # 准备批量请求数据
            payload = {
                'patients': [
                    {
                        'image_path': image_path,
                        'patient_name': '患者1',
                        'patient_age': 30,
                        'patient_gender': '男'
                    },
                    {
                        'image_path': image_path,
                        'patient_name': '患者2',
                        'patient_age': 28,
                        'patient_gender': '女'
                    }
                ]
            }
            
            # 保存到临时文件
            batch_file = 'batch_request.json'
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False)
            
            # 执行 curl 请求
            cmd = [
                'curl', '-s', '-X', 'POST',
                f'{self.base_url}/api/v1/batch-generate',
                '-H', 'Content-Type: application/json',
                '-d', f'@{batch_file}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('status') == 'success':
                    total = data.get('total', 0)
                    success = data.get('success_count', 0)
                    failed = data.get('failed_count', 0)
                    self.log(f"✓ 批量生成完成 (总数: {total}, 成功: {success}, 失败: {failed})", 'success')
                    self.test_results.append(('batch_generate', True))
                    return True
                else:
                    self.log(f"✗ API 返回错误: {data.get('error')}", 'error')
                    self.test_results.append(('batch_generate', False))
                    return False
            else:
                self.log(f"✗ 请求失败: {result.stderr}", 'error')
                self.test_results.append(('batch_generate', False))
                return False
        
        except Exception as e:
            self.log(f"✗ 错误: {str(e)}", 'error')
            self.test_results.append(('batch_generate', False))
            return False
        
        finally:
            if Path(batch_file).exists():
                Path(batch_file).unlink()
    
    def run_all_tests(self, with_pdf=True):
        """运行所有测试"""
        self.log("开始运行集成测试...", 'info')
        self.log("=" * 60, 'info')
        
        # 检查服务
        self.log("检查 API 服务连接...", 'info')
        try:
            result = subprocess.run(
                ['curl', '-s', '-I', f'{self.base_url}/health'],
                capture_output=True,
                timeout=3
            )
            if result.returncode != 0:
                raise Exception("无法连接到 API 服务")
        except Exception as e:
            self.log(f"❌ 无法连接到 {self.base_url}", 'error')
            self.log(f"   请确保 API 服务已启动: python thermal_api.py", 'warning')
            sys.exit(1)
        
        self.log("")
        
        # 运行测试
        self.test_health_check()
        time.sleep(0.5)
        
        self.test_status_api()
        time.sleep(0.5)
        
        if with_pdf:
            self.test_generate_pdf()
            time.sleep(0.5)
            
            self.test_batch_generate()
            time.sleep(0.5)
        
        # 输出总结
        self.print_summary()
    
    def print_summary(self):
        """输出测试总结"""
        self.log("")
        self.log("=" * 60, 'info')
        self.log("测试总结", 'info')
        self.log("=" * 60, 'info')
        
        total = len(self.test_results)
        passed = sum(1 for _, result in self.test_results if result)
        failed = total - passed
        
        for test_name, result in self.test_results:
            status = "PASS" if result else "FAIL"
            level = 'success' if result else 'error'
            self.log(f"  {test_name}: {status}", level)
        
        self.log("")
        self.log(f"总计: {total} | 通过: {passed} | 失败: {failed}", 
                 'success' if failed == 0 else 'warning')
        
        if failed == 0:
            self.log("✨ 所有测试通过！API 已准备就绪。", 'success')
        else:
            self.log("⚠️ 部分测试失败，请检查错误信息。", 'warning')
        
        self.log("=" * 60, 'info')


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='热成像 API 集成测试')
    parser.add_argument('--url', default='http://localhost:5000', 
                        help='API 服务地址 (默认: http://localhost:5000)')
    parser.add_argument('--skip-pdf', action='store_true', 
                        help='跳过 PDF 生成测试')
    parser.add_argument('--image', default='Snipaste_2026-03-22_11-27-51.png',
                        help='用于测试的图片路径')
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    tester.run_all_tests(with_pdf=not args.skip_pdf)
    
    sys.exit(0 if all(result for _, result in tester.test_results) else 1)
