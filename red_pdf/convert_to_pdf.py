#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将DOCX转换为PDF的多种方法
"""

import os
import subprocess
import sys

def convert_docx_to_pdf_method1(docx_path):
    """方法1：使用LibreOffice"""
    try:
        cmd = ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', '.', docx_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            pdf_path = docx_path.replace('.docx', '.pdf')
            return pdf_path if os.path.exists(pdf_path) else None
    except:
        pass
    return None

def convert_docx_to_pdf_method2(docx_path):
    """方法2：使用docx2pdf库"""
    try:
        from docx2pdf.core import convert
        pdf_path = docx_path.replace('.docx', '.pdf')
        convert(docx_path, pdf_path)
        return pdf_path if os.path.exists(pdf_path) else None
    except:
        pass
    return None

def convert_docx_to_pdf_method3(docx_path):
    """方法3：使用python-uno（LibreOffice UNO）"""
    try:
        import uno
        from com.sun.star.beans import PropertyValue
        
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context)
        
        ctx = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        
        props = (PropertyValue("Hidden", 0, True, 0),)
        url = 'file:///' + os.path.abspath(docx_path).replace('\\', '/')
        doc = desktop.loadComponentFromURL(url, "_blank", 0, props)
        
        pdf_path = docx_path.replace('.docx', '.pdf')
        export_props = (PropertyValue("FilterName", 0, "MS Word 2007 XML", 0),)
        pdf_url = 'file:///' + os.path.abspath(pdf_path).replace('\\', '/')
        doc.storeToURL(pdf_url, export_props)
        doc.close(True)
        
        return pdf_path if os.path.exists(pdf_path) else None
    except:
        pass
    return None

def convert_with_backup(docx_path):
    """使用多种方法尝试转换"""
    print(f"\n📄 开始转换：{os.path.basename(docx_path)}")
    print("-" * 60)
    
    # 方法1：LibreOffice
    print("尝试方法1：LibreOffice...")
    result = convert_docx_to_pdf_method1(docx_path)
    if result:
        print(f"✅ 成功！PDF已生成：{os.path.basename(result)}")
        return result
    
    # 方法2：docx2pdf
    print("尝试方法2：docx2pdf...")
    try:
        subprocess.run(['pip', 'install', 'docx2pdf', '-q'], timeout=30)
        result = convert_docx_to_pdf_method2(docx_path)
        if result:
            print(f"✅ 成功！PDF已生成：{os.path.basename(result)}")
            return result
    except:
        pass
    
    # 返回失败
    print("❌ 自动转换失败")
    return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        docx_file = sys.argv[1]
    else:
        # 查找最新的热图分析报告
        import glob
        files = glob.glob('热图分析报告_*.docx')
        if files:
            docx_file = max(files, key=os.path.getctime)
        else:
            print("❌ 找不到DOCX文件")
            sys.exit(1)
    
    if not os.path.exists(docx_file):
        print(f"❌ 文件不存在：{docx_file}")
        sys.exit(1)
    
    pdf_file = convert_with_backup(docx_file)
    
    if pdf_file:
        print(f"\n✅ 转换完成！")
        print(f"📁 PDF位置：{os.path.abspath(pdf_file)}")
    else:
        print(f"\n⚠️ 自动转换失败")
        print(f"💡 请手动方式：")
        print(f"   1. 用Word打开 {docx_file}")
        print(f"   2. 另存为 → 格式选PDF")
        print(f"   3. 保存即可")
