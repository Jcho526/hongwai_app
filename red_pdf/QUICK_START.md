# 热成像 API - 快速配置指南

## 📋 5 分钟快速开始

### 步骤 1: 安装 Python（如未安装）

访问 https://www.python.org/downloads/ 下载 Python 3.9 或更新版本

### 步骤 2: 打开 PowerShell

`Win + X` → 选择 "Windows PowerShell（管理员）"

### 步骤 3: 进入项目文件夹

```powershell
cd C:\Users\1\Desktop\新\red_pdf
```

### 步骤 4: 安装依赖

```powershell
pip install -r requirements.txt
```

> 💡 **提示**: 这会安装 Flask、python-docx 等必要的包

### 步骤 5: 验证 LibreOffice（重要！）

```powershell
where soffice.exe
```

如果找不到，需要安装 LibreOffice：
- 下载: https://www.libreoffice.org/download/
- 安装默认选项即可

### 步骤 6: 启动 API

```powershell
python thermal_api.py
```

**输出应该是：**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 步骤 7: 验证服务（新开 PowerShell 窗口）

```powershell
curl http://localhost:5000/health
```

**预期输出：**
```json
{
  "status": "healthy",
  "message": "热成像报告生成 API 服务运行中"
}
```

✅ **完成！API 已准备就绪**

---

## 🧪 测试 API

### 方式 1: 使用自动化测试脚本（推荐）

```powershell
python test_api.py
```

该脚本会自动测试所有端点

### 方式 2: 使用 cURL 生成单个 PDF

需要一个图片文件（如 `thermal.png`）：

```powershell
curl -X POST http://localhost:5000/api/v1/generate-pdf `
  -F "file=@thermal.png" `
  -F "patient_name=测试患者" `
  -F "patient_age=30" `
  -F "patient_gender=男" `
  --output report.pdf
```

### 方式 3: 使用 Python 客户端

```python
from thermal_client import ThermalAPIClient

client = ThermalAPIClient('http://localhost:5000')
result = client.generate_pdf(
    image_path='thermal.png',
    patient_name='赵女士',
    patient_age=35,
    patient_gender='女',
    output_path='report.pdf'
)

print(f"✅ PDF 已生成: {result['pdf_path']}")
```

---

## 📁 关键文件说明

| 文件 | 用途 |
|------|------|
| `thermal_api.py` | 🌟 API 主程序 - Flask 服务器 |
| `thermal_report_template.docx` | 报告模板 |
| `generate_report.py` | 报告生成引擎 |
| `thermal_client.py` | Python 客户端库 |
| `test_api.py` | 集成测试脚本 |
| `requirements.txt` | Python 依赖列表 |
| `API_USAGE_GUIDE.md` | 完整 API 文档 |
| `API_DEPLOYMENT.md` | 部署和配置指南 |

---

## 🔌 API 端点速览

### 健康检查
```
GET /health
```
验证 API 是否正在运行

### 获取状态
```
GET /api/v1/status
```
获取 API 版本和功能信息

### 生成单个 PDF ⭐
```
POST /api/v1/generate-pdf
Content-Type: multipart/form-data

参数:
  file (必需) - 热成像图片
  patient_name - 患者名
  patient_age - 患者年龄
  patient_gender - 患者性别
  patient_id - 患者 ID
```

### 批量生成 PDF ⭐
```
POST /api/v1/batch-generate
Content-Type: application/json

请求体:
{
  "patients": [
    {"image_path": "img1.png", "patient_name": "患者1"},
    {"image_path": "img2.png", "patient_name": "患者2"}
  ]
}
```

---

## ⚙️ 常见问题解决

### Q1: 运行 `start_api_simple.ps1` 时出现错误

**解决:**
1. 检查文件是否存在
2. 手动运行: `python thermal_api.py`

### Q2: "Cannot find python"

**解决:**
```powershell
# 检查 Python 是否在 PATH 中
python --version

# 如果无法识别，使用完整路径
C:\Python39\python.exe thermal_api.py
```

### Q3: "ModuleNotFoundError: No module named 'flask'"

**解决:**
```powershell
pip install flask
```

### Q4: "LibreOffice 转换失败"

**解决:**
1. 安装 LibreOffice: https://www.libreoffice.org/download/
2. 重启 PowerShell 窗口
3. 再试一次

### Q5: "Address already in use"

**解决:**
```powershell
# 查看谁占用了 5000 端口
netstat -ano | findstr :5000

# 杀死该进程（替换 <PID>）
taskkill /PID <PID> /F

# 或改用另一个端口
python thermal_api.py --port 8080
```

---

## 🚀 进阶用法

### 在 Vue.js 中使用

```javascript
// 在 Vue 组件中
async function generateReport(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);
    formData.append('patient_name', '赵女士');
    
    const response = await fetch('http://localhost:5000/api/v1/generate-pdf', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'report.pdf';
        a.click();
    }
}
```

### 批量处理

```python
import os
from thermal_client import ThermalAPIClient

client = ThermalAPIClient('http://localhost:5000')

# 处理文件夹中的所有图片
images = [f for f in os.listdir('images') if f.endswith(('.png', '.jpg'))]

for image in images:
    result = client.generate_pdf(
        image_path=f'images/{image}',
        patient_name=image.split('.')[0],
        output_path=f'reports/{image.split(".")[0]}.pdf'
    )
    print(f"处理: {image} -> {'成功' if result['success'] else '失败'}")
```

---

## 📊 检查清单

启动前检查：

- [ ] Python 3.7+ 已安装
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] LibreOffice 已安装
- [ ] `thermal_report_template.docx` 文件存在
- [ ] `thermal_api.py` 文件存在
- [ ] `generate_report.py` 文件存在

---

## 📖 更多信息

- **详细 API 文档**: 打开 `API_USAGE_GUIDE.md`
- **部署指南**: 打开 `API_DEPLOYMENT.md`
- **代码示例**: 查看 `thermal_client.py`
- **运行测试**: 执行 `python test_api.py`

---

## 💬 需要帮助？

1. **检查日志**: 在 API 运行窗口查看错误信息
2. **运行测试**: `python test_api.py` 可以诊断问题
3. **查看文档**: 相关文档在 `API_USAGE_GUIDE.md` 中
4. **查看示例**: 参考 `thermal_client.py` 中的使用示例

---

**现在就开始！** 执行以下命令启动服务：

```powershell
python thermal_api.py
```

**祝你使用愉快！🎉**
