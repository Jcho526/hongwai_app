import PyPDF2
import os

# 获取当前目录下的所有PDF文件
pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

# 遍历所有PDF文件
for pdf_file in pdf_files:
    print(f"\n{'='*50}")
    print(f"读取文件: {pdf_file}")
    print(f"{'='*50}")
    
    try:
        # 打开PDF文件
        with open(pdf_file, 'rb') as file:
            # 创建PDF阅读器对象
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 获取PDF总页数
            num_pages = len(pdf_reader.pages)
            print(f"总页数: {num_pages}")
            
            # 创建输出文件名
            output_file = f"{os.path.splitext(pdf_file)[0]}_content.txt"
            
            # 打开输出文件
            with open(output_file, 'w', encoding='utf-8') as out_file:
                # 写入文件信息
                out_file.write(f"{'='*50}\n")
                out_file.write(f"文件: {pdf_file}\n")
                out_file.write(f"总页数: {num_pages}\n")
                out_file.write(f"{'='*50}\n\n")
                
                # 遍历每一页
                for page_num in range(num_pages):
                    print(f"处理第 {page_num + 1} 页...")
                    # 获取当前页
                    page = pdf_reader.pages[page_num]
                    # 提取文本
                    text = page.extract_text()
                    # 写入文件
                    out_file.write(f"--- 第 {page_num + 1} 页 ---")
                    out_file.write(text)
                    out_file.write("\n\n")
                
            print(f"内容已保存到: {output_file}")
                
    except Exception as e:
        print(f"读取文件 {pdf_file} 时出错: {str(e)}")

print(f"\n{'='*50}")
print("所有PDF文件读取完成")
print(f"{'='*50}")