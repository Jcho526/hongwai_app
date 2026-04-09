# 🏥 红外热图分析报告 - DOC模板使用指南

## 📋 项目概述

本项目包含以下核心文件：

1. **thermal_report_template.docx** - 通用模板文件
2. **generate_report.py** - 报告自动生成脚本
3. **create_template.py** - 模板创建脚本
4. **analyze_template.py** - 模板分析脚本

---

## 🎯 模板结构

模板包含以下主要部分：

### 第1页：标题页
```
红外热像·中医可视化

[基本信息表]
编号：{{编号}}
姓名：{{患者名}}
性别：{{性别}}  年龄：{{年龄}}
检查日期：{{检查日期}}
```

### 第2页：目录和注意事项
- 报告内容目录
- 采集注意事项
- 重要说明

### 第3页：实时热成像
- 中医经络穴位图
- 热态分布
- 对称性和规律性

### 第4-5页：体质辨识
- 九种体质辨识模型
- 面部反射区温度分布表
- 体质类型描述

### 第6页：脏腑辨证
- 脏腑温度分析表
- 各部位的极大值、极小值、平均值、相对值
- 主要证型描述

### 第7-8页：三焦分析
- 上焦、中焦、下焦温度数据
- 经络穴位图
- 三焦分析结论

### 第9页：经络穴位检测
- 十二正经穴位温度数据
- 各经络的平均温度

### 第10页：气血瘀堵分析
- 气血瘀堵区域列表
- 气血不足区域列表
- 手掌热图分析

### 第11-12页：总体评估与调理建议
- 总体评估表
- 中医调理原则
- 推荐中药方案
- 穴位调理方法
- 药食同源建议
- 起居注意事项
- 免责声明

---

## 🔑 占位符说明

### 基本信息占位符
```
{{编号}}           - 患者编号
{{患者名}}         - 患者姓名
{{性别}}           - 患者性别
{{年龄}}           - 患者年龄
{{检查日期}}       - 检查日期
```

### 热态分布占位符
```
{{对称性}}         - 身体对称性指数
{{规律性}}         - 热源分布规律性
```

### 体质信息占位符
```
{{体质类型}}       - 体质分类
{{体质描述}}       - 体质详细描述
```

### 温度数据占位符（面部反射区）
```
{{首面区温度}}     - 首面区温度
{{咽喉区温度}}     - 咽喉区温度
{{肺区温度}}       - 肺区温度
{{心区温度}}       - 心区温度
{{肝区温度}}       - 肝区温度
{{脾区温度}}       - 脾区温度
{{膀胱温度}}       - 膀胱反射区温度
{{小肠区温度}}     - 小肠区温度
{{胃区温度}}       - 胃区温度
```

### 脏腑温度占位符（格式: {{部位_max}}、{{部位_min}}、{{部位_avg}}、{{部位_rel}}）
```
{{左胸膺_max}}     - 左胸膺最大值
{{左胸膺_min}}     - 左胸膺最小值
{{左胸膺_avg}}     - 左胸膺平均值
{{左胸膺_rel}}     - 左胸膺相对值
...（同理适用于其他部位）
```

### 三焦温度占位符
```
{{上焦_max}}, {{上焦_min}}, {{上焦_avg}}, {{上焦_rel}}
{{中焦_max}}, {{中焦_min}}, {{中焦_avg}}, {{中焦_rel}}
{{下焦_max}}, {{下焦_min}}, {{下焦_avg}}, {{下焦_rel}}
{{三焦分析}}       - 三焦分析文字描述
```

### 气血分析占位符
```
{{气血检查日期}}   - 气血检查日期
{{气血瘀堵区域}}   - 气血瘀堵的具体区域
{{气血不足区域}}   - 气血不足的具体区域
```

### 证型和调理占位符
```
{{主要证型}}       - 主要中医证型
{{证型详细描述}}   - 证型的详细描述
{{中医调理原则}}   - 调理的基本原则
{{推荐中药方案}}   - 推荐的中药方案
{{穴位调理}}       - 穴位调理建议
{{药食同源建议}}   - 食疗建议
{{起居注意事项}}   - 日常起居注意
```

### 最终评估占位符
```
{{总体体质}}       - 总体体质结论
{{三焦状况}}       - 三焦总体状况
{{气血状况}}       - 气血总体状况
{{主要问题}}       - 主要健康问题
{{最终评估日期}}   - 最终评估日期
{{评估医生}}       - 评估医生姓名
{{医疗机构}}       - 医疗机构名称
```

### 图片占位符
```
[图片占位符：热图正面图像]
[图片占位符：热图背面图像]
[图片占位符：体质辨识图表]
[图片占位符：任脉穴位图]
[图片占位符：督脉穴位图]
[图片占位符：膀胱经穴位图]
[图片占位符：手掌热图]
```

---

## 💻 使用方法

### 方法1：使用Python脚本自动生成报告

```python
from generate_report import ThermalReportGenerator

# 创建报告生成器
generator = ThermalReportGenerator('thermal_report_template.docx')

# 设置患者基本信息
generator.set_placeholder('编号', '20260322001')
generator.set_placeholder('患者名', '赵女士')
generator.set_placeholder('性别', '女')
generator.set_placeholder('年龄', '26')
generator.set_placeholder('检查日期', '2025-11-25')

# 设置其他数据...

# 替换占位符
generator.replace_placeholders()

# 保存报告
generator.save('output_report.docx')
```

### 方法2：直接在Word中编辑

1. 打开 `thermal_report_template.docx`
2. 使用 Word 的"查找和替换"功能：
   - Ctrl+H 打开查找和替换对话框
   - 在"查找"框输入：`{{患者名}}`
   - 在"替换为"框输入：`赵女士`
   - 点击"全部替换"

---

## 🚀 快速开始

### 第1步：准备数据

收集患者信息和热图分析数据：
```python
patient_data = {
    '编号': '20260322001',
    '患者名': '赵女士',
    '性别': '女',
    '年龄': '26',
    '检查日期': '2025-11-25',
    # ... 其他数据
}
```

### 第2步：运行生成脚本

```bash
python generate_report.py
```

### 第3步：检查生成的报告

打开生成的 `thermal_report_sample.docx` 文件检查内容。

### 第4步：转换为PDF

```bash
# 使用LibreOffice
soffice --headless --convert-to pdf thermal_report_sample.docx
```

---

## 📊 数据格式说明

### 温度数据
- 格式：浮点数，精确到小数点后2位
- 示例：`34.78`、`27.32`、`29.03`

### 区域异常面积
- 格式：`区域名称[面积数值]`
- 示例：`左后脑[197]`、`右后背区域[452]`

### 多行文本
- 在Python脚本中使用 `\n` 换行
- 示例：
  ```python
  text = '第一行内容\n第二行内容\n第三行内容'
  ```

---

## 🔧 高级用法

### 批量生成报告

```python
import pandas as pd
from generate_report import ThermalReportGenerator

# 读取患者数据（Excel或CSV）
df = pd.read_csv('patients.csv')

# 逐行生成报告
for index, row in df.iterrows():
    generator = ThermalReportGenerator('thermal_report_template.docx')
    
    # 为每个患者填充数据
    for col, value in row.items():
        generator.set_placeholder(col, value)
    
    generator.replace_placeholders()
    generator.save(f'report_{row["编号"]}.docx')
```

### 插入图片到模板

```python
from docx import Document
from docx.shared import Inches

doc = Document('thermal_report_template.docx')

# 在指定位置插入图片
for i, paragraph in enumerate(doc.paragraphs):
    if '热图正面图像' in paragraph.text:
        # 在这个段落后插入图片
        doc.paragraphs[i]._element.addnext(
            doc.add_picture('front_thermal_image.jpg', width=Inches(5))._element
        )

doc.save('report_with_images.docx')
```

---

## 📋 文件清单

```
red_pdf/
├── thermal_report_template.docx      ⭐ 通用模板
├── thermal_report_sample.docx        📄 示例报告
├── create_template.py                🔨 模板创建脚本
├── generate_report.py                🚀 报告生成脚本
├── analyze_template.py               🔍 模板分析脚本
└── TEMPLATE_GUIDE.md                 📚 本使用指南
```

---

## 🎨 模板定制建议

### 修改样式
1. 在Word中打开模板
2. 修改字体、颜色、大小
3. 保存为新的模板文件
4. 更新Python脚本中的模板路径

### 添加公司LOGO
1. 在首页插入公司LOGO图片
2. 调整图片大小和位置
3. 保存模板

### 修改页脚和页眉
1. 在Word中点击"插入" -> "页眉和页脚"
2. 添加医疗机构信息、页码等
3. 保存模板

---

## ⚠️ 注意事项

1. **占位符命名**：占位符必须完全匹配，包括大小写和符号
2. **图片替换**：图片占位符需要手动替换或使用高级Python脚本
3. **编码问题**：确保Python脚本使用UTF-8编码
4. **LibreOffice转PDF**：需要安装LibreOffice或使用在线转换工具

---

## 🔗 相关链接

- [python-docx文档](https://python-docx.readthedocs.io/)
- [LibreOffice下载](https://www.libreoffice.org/)
- [中医体质分类及判定标准](http://www.chinahealthcare.com/)

---

## 📞 技术支持

如有任何问题或建议，请联系开发团队。

**最后更新时间**：2026年3月22日
