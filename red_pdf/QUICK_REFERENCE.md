# 🎯 DOC模板快速参考卡

## 📦 已生成的核心文件

### 模板文件（可直接使用）
```
✅ thermal_report_template.docx    (39 KB)
   → 通用报告模板，包含100+个占位符
   → 12页完整报告结构
   → 可在Word中直接编辑
   
✅ thermal_report_sample.docx      (40 KB)
   → 示例报告（已填充赵女士数据）
   → 展示最终效果
   → 可作为参考对比
```

### Python脚本（自动生成）
```
✅ generate_report.py   (8.3 KB)
   → 报告生成核心脚本
   → 包含 ThermalReportGenerator 类
   → 支持批量生成和自定义
   
✅ create_template.py   (15 KB)
   → 模板创建脚本
   → 可用于修改模板结构
   → 包含丰富的格式化示例
   
✅ analyze_template.py  (2.4 KB)
   → 模板分析工具
   → 快速了解模板结构
```

### 文档（使用指南）
```
✅ TEMPLATE_GUIDE.md        (9 KB)
   → 完整的使用指南
   → 所有占位符详细说明
   → 快速开始教程
   
✅ SOLUTION_SUMMARY.md      (11 KB)
   → 完整解决方案总结
   → 架构设计和集成方案
   → 高级用法示例
```

---

## ⚡ 3种快速使用方式

### 方式1️⃣：手动编辑（最简单）
```
1. 打开 thermal_report_template.docx
2. Ctrl+H 打开查找替换
3. 替换 {{占位符}} → 真实数据
4. 保存为患者报告
5. 导出为PDF
⏱️ 耗时：5-10分钟/份
```

### 方式2️⃣：Python自动生成（推荐）
```python
from generate_report import ThermalReportGenerator

gen = ThermalReportGenerator('thermal_report_template.docx')
gen.set_placeholder('患者名', '王女士')
gen.set_placeholder('年龄', '32')
# ... 设置其他数据 ...
gen.replace_placeholders()
gen.save('王女士_报告.docx')
```
⏱️ 耗时：<1秒/份

### 方式3️⃣：批量生成（最高效）
```python
import pandas as pd
from generate_report import ThermalReportGenerator

df = pd.read_excel('patients.xlsx')
for idx, row in df.iterrows():
    gen = ThermalReportGenerator('thermal_report_template.docx')
    for col in df.columns:
        gen.set_placeholder(col, row[col])
    gen.replace_placeholders()
    gen.save(f"{row['患者名']}_报告.docx")
```
⏱️ 耗时：<0.1秒/份（可并发）

---

## 🔑 核心占位符速查表

### 患者基本信息（5个）
| 占位符 | 示例值 | 说明 |
|--------|--------|------|
| `{{编号}}` | 20260322001 | 患者编号 |
| `{{患者名}}` | 赵女士 | 患者姓名 |
| `{{性别}}` | 女 | 性别 |
| `{{年龄}}` | 26 | 年龄 |
| `{{检查日期}}` | 2025-11-25 | 检查日期 |

### 热态和体质（9个）
| 占位符 | 示例值 | 说明 |
|--------|--------|------|
| `{{对称性}}` | 左右少腹不对称 0.93 | 身体对称性 |
| `{{规律性}}` | 正面热序列：肺,左胁,大腹 | 热源规律性 |
| `{{体质类型}}` | 阴虚体质，倾向气郁体质 | 体质分类 |
| `{{体质描述}}` | 津液不足，容易出现虚热 | 体质详情 |
| `{{首面区温度}}` | 29.31 | 首面区温度(℃) |
| `{{咽喉区温度}}` | 33.68 | 咽喉区温度(℃) |
| `{{肺区温度}}` | 34.37 | 肺区温度(℃) |
| `{{心区温度}}` | 34.24 | 心区温度(℃) |
| `{{肝区温度}}` | 34.07 | 肝区温度(℃) |

### 脏腑数据（36个，格式：部位_max/min/avg/rel）
```
{{左胸膺_max}}, {{左胸膺_min}}, {{左胸膺_avg}}, {{左胸膺_rel}}
{{右胸_max}}, {{右胸_min}}, {{右胸_avg}}, {{右胸_rel}}
{{虚里_max}}, {{虚里_min}}, {{虚里_avg}}, {{虚里_rel}}
{{胃脘_max}}, {{胃脘_min}}, {{胃脘_avg}}, {{胃脘_rel}}
{{左胁_max}}, {{左胁_min}}, {{左胁_avg}}, {{左胁_rel}}
{{右胁_max}}, {{右胁_min}}, {{右胁_avg}}, {{右胁_rel}}
{{大腹_max}}, {{大腹_min}}, {{大腹_avg}}, {{大腹_rel}}
{{小腹_max}}, {{小腹_min}}, {{小腹_avg}}, {{小腹_rel}}
{{右少腹_max}}, {{右少腹_min}}, {{右少腹_avg}}, {{右少腹_rel}}
```

### 三焦数据（12个）
```
上焦: {{上焦_max}}, {{上焦_min}}, {{上焦_avg}}, {{上焦_rel}}
中焦: {{中焦_max}}, {{中焦_min}}, {{中焦_avg}}, {{中焦_rel}}
下焦: {{下焦_max}}, {{下焦_min}}, {{下焦_avg}}, {{下焦_rel}}
```

### 调理建议（5个）
| 占位符 | 内容 |
|--------|------|
| `{{中医调理原则}}` | 例：以养阴润肺为原则 |
| `{{推荐中药方案}}` | 例：百合固金汤 |
| `{{穴位调理}}` | 例：肺俞穴按揉 |
| `{{药食同源建议}}` | 例：麦冬、银耳 |
| `{{起居注意事项}}` | 例：22点前入睡 |

### 最终评估（7个）
| 占位符 | 示例 |
|--------|------|
| `{{主要证型}}` | 肺阴虚证 |
| `{{总体体质}}` | 阴虚体质 |
| `{{三焦状况}}` | 上焦热，下焦寒 |
| `{{气血状况}}` | 气血瘀堵与不足并存 |
| `{{主要问题}}` | 肺阴虚，脾阳虚 |
| `{{最终评估日期}}` | 2026-03-22 |
| `{{评估医生}}` | 医生姓名 |

**⚠️ 注意**：占位符必须完全匹配，包括大小写和括号！

---

## 💾 文件保存位置

```
c:\Users\1\Desktop\新\red_pdf\
│
├─ 模板文件
│  ├─ thermal_report_template.docx     ✅ 通用模板
│  └─ thermal_report_sample.docx       📄 示例报告
│
├─ Python脚本
│  ├─ generate_report.py               🚀 生成报告
│  ├─ create_template.py               🔨 创建模板
│  └─ analyze_template.py              🔍 分析模板
│
├─ 文档
│  ├─ TEMPLATE_GUIDE.md                📚 使用指南
│  └─ SOLUTION_SUMMARY.md              📋 完整方案
│
└─ 其他
   ├─ 中医治未病_content.txt           📄 中医内容
   ├─ 印刷版-热图字典_content.txt      📊 热图字典
   └─ thermal_dict.json                🔑 知识库
```

---

## 🎯 今日成果

### ✅ 完成清单
- [x] 理解现有DOC模板结构
- [x] 创建通用DOC模板（12页）
- [x] 开发Python自动生成脚本
- [x] 编写完整使用指南
- [x] 生成示例报告
- [x] 提供快速参考卡

### 📊 关键指标
- **模板占位符**: 100+ 个
- **支持自动替换**: 是
- **生成速度**: <1秒/份
- **支持批量生成**: 是
- **文件大小**: ~40KB
- **页数**: 12 页完整报告

---

## 🚀 立即开始

### 第1步：复制模板
```bash
# 使用现有模板
cp thermal_report_template.docx my_report.docx
```

### 第2步：填充数据（选择一种方式）

**方式A - 在Word中手动替换**
```
打开 my_report.docx → Ctrl+H → 替换所有占位符 → 保存
```

**方式B - 用Python脚本**
```bash
python generate_report.py
```

### 第3步：转换为PDF
```bash
# 需要LibreOffice
soffice --headless --convert-to pdf my_report.docx
```

---

## 📞 常见问题

**Q: 占位符不能是中文吗？**  
A: 可以是中文，只要与set_placeholder()中的key完全匹配

**Q: 能直接在表格里插入图片吗？**  
A: 表格单元格中不能直接插入占位符图片，需要手动或用高级脚本

**Q: 支持条件显示吗？**  
A: 暂不支持，可以在数据准备时就确定要显示的内容

**Q: 能自动转PDF吗？**  
A: 可以，使用LibreOffice或python-uno库

---

## 💡 下一步建议

1. **集成热图分析** - 自动提取热图特征填充模板
2. **添加数据库** - 保存患者信息和报告历史
3. **开发Web界面** - 上传热图→自动生成报告
4. **多语言支持** - 英文/中文版本
5. **电子签名** - 医疗合规要求
6. **报告版本控制** - 追踪修改历史

---

**🎉 模板系统已就绪，可以投入使用！**

最后更新：2026年3月22日 11:30  
下载模板：thermal_report_template.docx
