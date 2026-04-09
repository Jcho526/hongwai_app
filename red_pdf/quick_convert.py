#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用docx2pdf将DOCX转换为PDF
"""

import os
import glob
from docx2pdf import convert

# 查找最新的热图分析报告
files = glob.glob('热图分析报告_*.docx')
if not files:
    print("❌ 找不到DOCX文件")
    exit(1)

docx_file = max(files, key=os.path.getctime)
print(f"📄 转换文件：{docx_file}")

try:
    pdf_file = docx_file.replace('.docx', '.pdf')
    print(f"🔄 转换中...")
    convert(docx_file, pdf_file)
    
    if os.path.exists(pdf_file):
        file_size = os.path.getsize(pdf_file)
        print(f"\n✅ 转换成功！")
        print(f"📁 PDF文件：{pdf_file}")
        print(f"💾 文件大小：{file_size / 1024:.1f} KB")
    else:
        print(f"❌ 转换失败")

except Exception as e:
    print(f"❌ 错误：{e}")
