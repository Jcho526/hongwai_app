#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从热图图片生成PDF报告
"""

from generate_report import ThermalReportGenerator
from datetime import datetime
import os

def generate_pdf_from_image(image_path):
    """
    从热图图片生成完整的PDF报告
    
    Args:
        image_path: 热图图片路径
    """
    
    print("=" * 60)
    print("🔥 热图分析报告自动生成系统")
    print("=" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"❌ 错误：找不到图片文件 {image_path}")
        return False
    
    print(f"\n✅ 检测到图片：{os.path.basename(image_path)}")
    
    # 创建报告生成器
    print("\n📋 加载模板...")
    gen = ThermalReportGenerator('thermal_report_template.docx')
    
    # 设置默认患者信息
    print("📝 填充患者信息...")
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
        
        # 面部反射区温度（示例值）
        '首面区温度': '0',
        '咽喉区温度': '0',
        '肺区温度': '0',
        '心区温度': '0',
        '肝区温度': '0',
        '脾区温度': '0',
        '膀胱温度': '0',
        '小肠区温度': '0',
        '胃区温度': '0',
        
        # 脏腑数据（示例值）
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
    
    # 填充所有占位符
    for key, value in patient_data.items():
        gen.set_placeholder(key, value)
    
    # 替换占位符
    print("🔄 替换占位符...")
    gen.replace_placeholders()
    
    # 生成DOCX报告
    docx_filename = f"热图分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    print(f"\n💾 保存DOCX报告：{docx_filename}")
    gen.save(docx_filename)
    
    # 转换为PDF
    print("📄 转换为PDF...")
    try:
        import subprocess
        pdf_filename = docx_filename.replace('.docx', '.pdf')
        
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', '.',
            docx_filename
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF已生成：{pdf_filename}")
            print("\n" + "=" * 60)
            print(f"📊 报告生成成功！")
            print(f"📁 文件位置：c:\\Users\\1\\Desktop\\新\\red_pdf\\{pdf_filename}")
            print("=" * 60)
            return True
        else:
            print(f"⚠️ PDF转换失败，但DOCX已生成：{docx_filename}")
            print(f"错误信息：{result.stderr}")
            print("\n提示：请手动打开DOCX文件，另存为PDF")
            return False
    
    except FileNotFoundError:
        print(f"⚠️ 未找到LibreOffice，请先安装LibreOffice")
        print(f"✅ DOCX报告已生成：{docx_filename}")
        print("💡 提示：可以用Word手动转换为PDF，或安装LibreOffice后重试")
        return False

if __name__ == '__main__':
    # 使用检测到的图片
    image_file = 'Snipaste_2026-03-22_11-27-51.png'
    
    if os.path.exists(image_file):
        generate_pdf_from_image(image_file)
    else:
        print(f"❌ 找不到图片文件：{image_file}")
        print("\n请确保图片文件在当前目录下")
