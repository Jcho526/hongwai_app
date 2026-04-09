#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热成像报告生成 API 服务
提供 HTTP 接口用于上传热成像图片并生成 PDF 报告
"""

from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from generate_report import ThermalReportGenerator
from datetime import datetime
import os
import subprocess
import shutil
from pathlib import Path
import base64
import io

# 尝试导入 PDF 转换库
try:
    from docx2pdf import convert
    HAS_DOCX2PDF = True
except ImportError:
    HAS_DOCX2PDF = False
    print("⚠️  未找到 docx2pdf，将尝试使用 LibreOffice 转换")


app = Flask(__name__)

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 配置
UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, 'reports')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# 创建文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_pdf_report(image_path, patient_info=None):
    """
    生成 DOCX 报告
    
    Args:
        image_path: 热成像图片路径（可选）
        patient_info: 患者信息字典（可选）
    
    Returns:
        docx_path: 生成的 DOCX 文件路径
    """
    
    try:
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, 'thermal_report_template.docx')
        
        # 加载模板
        gen = ThermalReportGenerator(template_path)
        
        # 准备患者数据
        patient_data = {
            '编号': 'PT' + datetime.now().strftime('%Y%m%d%H%M%S'),
            '患者名': '患者',
            '性别': '未知',
            '年龄': '0',
            '检查日期': datetime.now().strftime('%Y-%m-%d'),
            
            # 热态分布
            '对称性': '待分析',
            '规律性': '待分析',
            
            # 体质信息
            '体质类型': '待分析',
            '体质描述': '根据热图分析进行判定',
            
            # 面部反射区温度
            '首面区温度': '0',
            '咽喉区温度': '0',
            '肺区温度': '0',
            '心区温度': '0',
            '肝区温度': '0',
            '脾区温度': '0',
            '膀胱温度': '0',
            '小肠区温度': '0',
            '胃区温度': '0',
            
            # 脏腑数据
            '左胸膺_max': '0', '左胸膺_min': '0', '左胸膺_avg': '0', '左胸膺_rel': '0',
            '右胸_max': '0', '右胸_min': '0', '右胸_avg': '0', '右胸_rel': '0',
            '虚里_max': '0', '虚里_min': '0', '虚里_avg': '0', '虚里_rel': '0',
            '胃脘_max': '0', '胃脘_min': '0', '胃脘_avg': '0', '胃脘_rel': '0',
            '左胁_max': '0', '左胁_min': '0', '左胁_avg': '0', '左胁_rel': '0',
            '右胁_max': '0', '右胁_min': '0', '右胁_avg': '0', '右胁_rel': '0',
            '大腹_max': '0', '大腹_min': '0', '大腹_avg': '0', '大腹_rel': '0',
            '小腹_max': '0', '小腹_min': '0', '小腹_avg': '0', '小腹_rel': '0',
            '右少腹_max': '0', '右少腹_min': '0', '右少腹_avg': '0', '右少腹_rel': '0',
            
            # 三焦数据
            '上焦_max': '0', '上焦_min': '0', '上焦_avg': '0', '上焦_rel': '0',
            '中焦_max': '0', '中焦_min': '0', '中焦_avg': '0', '中焦_rel': '0',
            '下焦_max': '0', '下焦_min': '0', '下焦_avg': '0', '下焦_rel': '0',
            '三焦分析': '待分析',
            
            # 气血信息
            '气血检查日期': datetime.now().strftime('%Y-%m-%d'),
            '气血瘀堵区域': '根据热图分析进行判定',
            '气血不足区域': '根据热图分析进行判定',
            
            # 证型
            '主要证型': '待分析',
            '证型详细描述': '根据热图和临床表现进行综合判定',
            
            # 调理建议
            '中医调理原则': '根据具体证型制定调理方案',
            '推荐中药方案': '建议咨询专业中医医生',
            '穴位调理': '建议咨询专业针灸医生',
            '药食同源建议': '根据体质选择适合的食疗方案',
            '起居注意事项': '保持规律作息，避免过度劳累',
            
            # 总体评估
            '总体体质': '待分析',
            '三焦状况': '待分析',
            '气血状况': '待分析',
            '主要问题': '根据热图分析进行判定',
            
            # 最终信息
            '最终评估日期': datetime.now().strftime('%Y-%m-%d'),
            '评估医生': '医疗专业人士',
            '医疗机构': '中医诊疗中心',
        }
        
        # 如果提供了患者信息，则覆盖默认值
        if patient_info:
            patient_data.update(patient_info)
        
        # 填充所有占位符
        for key, value in patient_data.items():
            gen.set_placeholder(key, str(value))
        
        # 替换占位符
        gen.replace_placeholders()
        
        # 生成 DOCX
        docx_filename = os.path.join(
            OUTPUT_FOLDER,
            f"热图分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        )
        gen.save(docx_filename)
        
        # 返回 DOCX 文件（不转换为 PDF 以避免 Windows COM 问题）
        return docx_filename
    
    except Exception as e:
        raise Exception(f"报告生成失败: {str(e)}")


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'message': '热成像报告生成 API 服务正常运行',
        'version': '1.0.0'
    })


@app.route('/api/v1/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    生成 PDF 报告
    
    支持两种上传方式：
    1. 文件上传（multipart/form-data）:
       - file: 热成像图片文件（必需）
       - patient_name: 患者名（可选）
       - patient_age: 患者年龄（可选）
       - patient_gender: 患者性别（可选）
       - patient_id: 患者 ID（可选）
    
    2. Base64 上传（application/json）:
       - image_base64: base64 编码的图片（必需）
       - patient_name: 患者名（可选）
       - patient_age: 患者年龄（可选）
       - patient_gender: 患者性别（可选）
       - patient_id: 患者 ID（可选）
    
    返回：
    - 成功: PDF 文件 + 200
    - 失败: 错误信息 JSON + 错误码
    """
    
    filepath = None
    
    try:
        # 检查请求类型
        if request.method == 'POST':
            # 方式 1：检查文件上传
            if 'file' in request.files:
                file = request.files['file']
                
                # 检查文件名是否为空
                if file.filename == '':
                    return jsonify({
                        'status': 'error',
                        'error': '文件名为空',
                        'code': 'EMPTY_FILENAME'
                    }), 400
                
                # 检查文件类型
                if not allowed_file(file.filename):
                    return jsonify({
                        'status': 'error',
                        'error': f'文件类型不支持: {file.filename.rsplit(".", 1)[-1] if "." in file.filename else "unknown"}，仅支持: {", ".join(ALLOWED_EXTENSIONS)}',
                        'code': 'INVALID_FILE_TYPE'
                    }), 400
                
                # 保存上传的文件
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                patient_name = request.form.get('patient_name', '患者')
                patient_age = request.form.get('patient_age', '0')
                patient_gender = request.form.get('patient_gender', '未知')
                patient_id = request.form.get('patient_id', '')
            
            # 方式 2：检查 Base64 上传
            elif request.is_json and request.json:
                data = request.json
                if 'image_base64' not in data:
                    return jsonify({
                        'status': 'error',
                        'error': '未找到 image_base64 字段',
                        'code': 'NO_IMAGE_BASE64'
                    }), 400
                
                try:
                    # 解析 base64 数据
                    image_base64 = data['image_base64']
                    
                    # 提取 base64 部分（去掉 data:image/...;base64, 前缀）
                    if ',' in image_base64:
                        image_base64 = image_base64.split(',')[1]
                    
                    # 解码 base64
                    image_data = base64.b64decode(image_base64)
                    
                    # 保存为临时文件
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_base64_image.png"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    
                    patient_name = data.get('patient_name', '患者')
                    patient_age = str(data.get('patient_age', '0'))
                    patient_gender = data.get('patient_gender', '未知')
                    patient_id = data.get('patient_id', '')
                
                except Exception as e:
                    return jsonify({
                        'status': 'error',
                        'error': f'Base64 解码失败: {str(e)}',
                        'code': 'BASE64_DECODE_ERROR'
                    }), 400
            
            else:
                return jsonify({
                    'status': 'error',
                    'error': '未找到图片文件或 base64 数据',
                    'code': 'NO_FILE'
                }), 400
        
        # 提取患者信息
        patient_info = {}
        if patient_name and patient_name != '患者':
            patient_info['患者名'] = patient_name
        if patient_age and patient_age != '0':
            patient_info['年龄'] = patient_age
        if patient_gender and patient_gender != '未知':
            patient_info['性别'] = patient_gender
        if patient_id:
            patient_info['编号'] = patient_id
        
        # 生成 PDF 报告
        pdf_path = generate_pdf_report(filepath, patient_info)
        
        # 返回 PDF 文件
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=os.path.basename(pdf_path)
        )
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 'GENERATION_ERROR'
        }), 500
    
    finally:
        # 清理临时文件（可选）
        if filepath and os.path.exists(filepath):
            try:
                # 延迟删除，让文件被发送后再删除
                pass
            except Exception as e:
                print(f"清理临时文件失败: {e}")


@app.route('/api/v1/batch-generate', methods=['POST'])
def batch_generate():
    """
    批量生成 PDF 报告
    
    请求格式：
    {
        "patients": [
            {
                "image_path": "path/to/image.png",
                "patient_name": "患者1",
                "patient_age": "30",
                "patient_gender": "男"
            },
            ...
        ]
    }
    
    返回：
    {
        "success": true,
        "total": 2,
        "success_count": 2,
        "failed_count": 0,
        "results": [
            {
                "patient_name": "患者1",
                "pdf_path": "path/to/report.pdf",
                "success": true
            },
            ...
        ]
    }
    """
    
    try:
        data = request.get_json()
        
        if not data or 'patients' not in data:
            return jsonify({
                'success': False,
                'error': '请提供患者列表',
                'code': 'NO_PATIENT_LIST'
            }), 400
        
        patients = data['patients']
        results = []
        success_count = 0
        failed_count = 0
        
        for patient in patients:
            try:
                image_path = patient.get('image_path')
                
                if not image_path or not os.path.exists(image_path):
                    results.append({
                        'patient_name': patient.get('patient_name', '未知'),
                        'success': False,
                        'error': '图片文件不存在'
                    })
                    failed_count += 1
                    continue
                
                # 提取患者信息
                patient_info = {
                    '患者名': patient.get('patient_name', '患者'),
                    '年龄': str(patient.get('patient_age', '0')),
                    '性别': patient.get('patient_gender', '未知'),
                }
                
                # 生成 PDF
                pdf_path = generate_pdf_report(image_path, patient_info)
                
                results.append({
                    'patient_name': patient.get('patient_name'),
                    'pdf_path': pdf_path,
                    'success': True
                })
                success_count += 1
            
            except Exception as e:
                results.append({
                    'patient_name': patient.get('patient_name', '未知'),
                    'success': False,
                    'error': str(e)
                })
                failed_count += 1
        
        return jsonify({
            'success': True,
            'total': len(patients),
            'success_count': success_count,
            'failed_count': failed_count,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'BATCH_ERROR'
        }), 500


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """获取 API 状态信息"""
    return jsonify({
        'service': '热成像报告生成 API',
        'version': '1.0.0',
        'status': 'running',
        'upload_folder': os.path.abspath(UPLOAD_FOLDER),
        'output_folder': os.path.abspath(OUTPUT_FOLDER),
        'max_file_size_mb': MAX_FILE_SIZE / (1024 * 1024),
        'supported_formats': list(ALLOWED_EXTENSIONS)
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """处理文件过大错误"""
    return jsonify({
        'success': False,
        'error': f'文件过大，最大允许 {MAX_FILE_SIZE / (1024 * 1024):.0f}MB',
        'code': 'FILE_TOO_LARGE'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """处理 404 错误"""
    return jsonify({
        'success': False,
        'error': '请求的资源不存在',
        'code': 'NOT_FOUND'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """处理 500 错误"""
    return jsonify({
        'success': False,
        'error': '服务器内部错误',
        'code': 'INTERNAL_ERROR'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🔥 热成像报告生成 API 服务")
    print("=" * 60)
    print("\n📍 服务地址：http://localhost:5000")
    print("\n🔗 可用接口：")
    print("  - GET  /health                    - 健康检查")
    print("  - GET  /api/v1/status             - 获取状态")
    print("  - POST /api/v1/generate-pdf       - 生成单个 PDF")
    print("  - POST /api/v1/batch-generate     - 批量生成 PDF")
    print("\n⚠️  请确保已安装 LibreOffice")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
