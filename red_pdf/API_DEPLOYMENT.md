# 热成像 API 部署指南

## 📋 快速概览

| 项目 | 信息 |
|------|------|
| **项目名** | 热成像报告生成 API |
| **版本** | 1.0.0 |
| **框架** | Flask |
| **Python 版本** | 3.7+ |
| **主要功能** | 根据热成像图片自动生成医学分析报告 PDF |
| **核心端点** | POST /api/v1/generate-pdf, POST /api/v1/batch-generate |

---

## 📂 文件结构

```
red_pdf/
├── thermal_api.py                 # 🌟 Flask API 主程序（核心）
├── thermal_client.py              # Python 客户端库
├── test_api.py                    # 集成测试脚本
├── API_USAGE_GUIDE.md            # API 使用文档
├── API_DEPLOYMENT.md             # 本文档 - 部署指南
├── generate_report.py             # 报告生成引擎
├── thermal_report_template.docx   # 报告模板
├── requirements.txt               # Python 依赖
├── start_api.bat                  # Windows 批处理启动脚本
├── start_api.ps1                  # Windows PowerShell 启动脚本
├── start_api_simple.ps1          # 简化版 PowerShell 启动脚本
└── [其他配置文件...]
```

---

## 🚀 快速开始

### 方式 1️⃣: Windows PowerShell（推荐）

**一键启动（最简单）：**
```powershell
.\start_api_simple.ps1
```

该脚本会自动：
- ✅ 检测 Python 安装
- ✅ 验证依赖包
- ✅ 提示安装缺失的包
- ✅ 启动 API 服务

### 方式 2️⃣: 手动启动

**1. 安装 Python（3.7+）**
```
https://www.python.org/downloads/
```

**2. 进入项目目录**
```powershell
cd c:\Users\1\Desktop\新\red_pdf
```

**3. 安装依赖**
```powershell
pip install -r requirements.txt
```

**4. 启动服务**
```powershell
python thermal_api.py
```

**预期输出：**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 方式 3️⃣: Docker 部署（生产环境）

**创建 Dockerfile：**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖（LibreOffice）
RUN apt-get update && apt-get install -y \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY thermal_api.py .
COPY thermal_report_template.docx .
COPY generate_report.py .

# 暴露端口
EXPOSE 5000

# 启动服务
CMD ["python", "thermal_api.py"]
```

**构建和运行：**
```bash
docker build -t thermal-api:1.0.0 .
docker run -p 5000:5000 thermal-api:1.0.0
```

---

## ✅ 验证安装

### 1. 健康检查
```bash
curl http://localhost:5000/health
```
**预期响应：**
```json
{
  "status": "healthy",
  "message": "热成像报告生成 API 服务运行中"
}
```

### 2. 查看服务状态
```bash
curl http://localhost:5000/api/v1/status
```

### 3. 运行集成测试
```powershell
python test_api.py --url http://localhost:5000
```

---

## 📚 使用示例

### Python 集成示例

```python
from thermal_client import ThermalAPIClient

# 初始化客户端
client = ThermalAPIClient('http://localhost:5000')

# 验证服务
health = client.health_check()
print(f"服务状态: {health['status']}")

# 生成单个报告
result = client.generate_pdf(
    image_path='thermal_image.png',
    patient_name='赵女士',
    patient_age=35,
    patient_gender='女',
    patient_id='PT001',
    output_path='report.pdf'
)

if result['success']:
    print(f"✅ 报告已保存: {result['pdf_path']}")
else:
    print(f"❌ 生成失败: {result['error']}")
```

### JavaScript/Vue.js 示例

```javascript
// 生成单个报告
const formData = new FormData();
formData.append('file', imageFile);
formData.append('patient_name', '赵女士');
formData.append('patient_age', 35);

const response = await fetch('http://localhost:5000/api/v1/generate-pdf', {
    method: 'POST',
    body: formData
});

if (response.ok) {
    const blob = await response.blob();
    // 下载或处理 PDF...
} else {
    console.error(await response.json());
}
```

### cURL 示例

```bash
# 单个生成
curl -X POST http://localhost:5000/api/v1/generate-pdf \
  -F "file=@thermal.png" \
  -F "patient_name=赵女士" \
  -F "patient_age=35" \
  --output report.pdf

# 批量生成
curl -X POST http://localhost:5000/api/v1/batch-generate \
  -H "Content-Type: application/json" \
  -d '{
    "patients": [
      {"image_path": "img1.png", "patient_name": "患者1"},
      {"image_path": "img2.png", "patient_name": "患者2"}
    ]
  }'
```

---

## 🔧 配置选项

### 修改 API 端口

编辑 `thermal_api.py`，找到最后一行：

```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

改为你需要的端口（如 8080）：

```python
app.run(host='0.0.0.0', port=8080, debug=False)
```

### 修改最大文件大小

编辑 `thermal_api.py`，找到：

```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
```

改为需要的大小（例如 100MB）：

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

### 启用 Debug 模式（开发环境）

编辑最后一行：

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 📊 生产环境部署

### 推荐架构

```
┌─────────────┐
│   客户端    │ (Vue.js / 移动应用)
└──────┬──────┘
       │ HTTP
       ↓
┌──────────────────┐
│   Nginx/Proxy    │ (负载均衡)
└──────┬───────────┘
       │
   ┌───┴───────┬───────┬───────┐
   ↓           ↓       ↓       ↓
┌────────────────────────────────┐
│  多个 Flask API 实例 (3-5个)   │
│  thermal_api.py (进程 1)       │
│  thermal_api.py (进程 2)       │
│  thermal_api.py (进程 3)       │
└────────────────────────────────┘
   ↓         ↓         ↓
┌─────────────────────────────┐
│  共享存储 / 数据库           │
│  - PDF 输出文件夹            │
│  - 模板文件                  │
│  - 日志                      │
└─────────────────────────────┘
```

### 使用 Gunicorn 部署（生产推荐）

**1. 安装 Gunicorn：**
```bash
pip install gunicorn
```

**2. 启动多进程服务：**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 thermal_api:app
```

**参数说明：**
- `-w 4`: 4 个工作进程（CPU核心数）
- `-b 0.0.0.0:5000`: 绑定所有网卡的 5000 端口

**3. 配置 Nginx 反向代理：**
```nginx
upstream thermal_api {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name api.thermal.example.com;
    
    location /api {
        proxy_pass http://thermal_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
```

### 使用 Supervisor 守护进程

**1. 安装 Supervisor：**
```bash
pip install supervisor
```

**2. 创建配置文件 `/etc/supervisor/conf.d/thermal_api.conf`：**
```ini
[program:thermal_api]
directory=/path/to/red_pdf
command=gunicorn -w 4 -b 0.0.0.0:5000 thermal_api:app
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=10
stdout_logfile=/var/log/thermal_api_stdout.log
stderr_logfile=/var/log/thermal_api_stderr.log
```

**3. 启动服务：**
```bash
supervisorctl reread
supervisorctl update
supervisorctl start thermal_api
```

---

## 🔒 安全性配置

### 1. 启用 HTTPS

**使用自签名证书测试：**
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

**在 Flask 中使用：**
```python
app.run(
    host='0.0.0.0',
    port=5000,
    ssl_context=('cert.pem', 'key.pem')
)
```

### 2. 添加 API 认证

编辑 `thermal_api.py`，添加认证装饰器：

```python
from functools import wraps

API_KEY = 'your-secret-key-here'

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('Authorization')
        if not key or key != f'Bearer {API_KEY}':
            return {'error': '未授权'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/v1/generate-pdf', methods=['POST'])
@require_api_key
def generate_pdf():
    # ...
```

### 3. 速率限制

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/v1/generate-pdf', methods=['POST'])
@limiter.limit("5 per minute")
def generate_pdf():
    # ...
```

---

## 🐛 故障排查

### 问题 1: 无法启动服务

**错误信息：** `Address already in use`

**解决方案：**
```bash
# 查找占用 5000 端口的进程
netstat -ano | findstr :5000

# 杀死进程（使用 PID）
taskkill /PID <PID> /F

# 或改用其他端口
python thermal_api.py --port 8080
```

### 问题 2: PDF 转换失败

**错误消息：** `PDF 转换失败，请检查 LibreOffice 是否已安装`

**解决方案：**
```bash
# Windows: 下载安装 LibreOffice
# https://www.libreoffice.org/download/

# Linux:
sudo apt-get install libreoffice

# macOS:
brew install libreoffice
```

### 问题 3: 模板文件不存在

**错误消息：** `模板文件不存在: thermal_report_template.docx`

**解决方案：**
```bash
# 确保文件在 red_pdf 文件夹中
ls thermal_report_template.docx  # Linux/macOS
dir thermal_report_template.docx # Windows

# 如果文件丢失，重新生成模板
python generate_report.py --create-template
```

### 问题 4: 内存不足

**症状：** 处理大文件时进程崩溃

**解决方案：**
```python
# 编辑 thermal_api.py，减小 MAX_FILE_SIZE
MAX_FILE_SIZE = 20 * 1024 * 1024  # 改为 20MB

# 或使用异步处理任务队列（Celery）
pip install celery redis
```

---

## 📈 性能优化

### 1. 启用 gzip 压缩
```python
from flask_compress import Compress
Compress(app)
```

### 2. 添加响应缓存
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/v1/status')
@cache.cached(timeout=300)
def get_status():
    # ...
```

### 3. 异步任务处理（高并发）

```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379')

@celery.task
def generate_pdf_async(image_path, patient_data):
    # 后台处理 PDF 生成
    return generate_pdf_sync(image_path, patient_data)

@app.route('/api/v1/generate-pdf-async', methods=['POST'])
def generate_pdf_async_endpoint():
    # 返回任务 ID，客户端轮询获取结果
    task = generate_pdf_async.delay(...)
    return {'task_id': task.id}, 202
```

---

## 📝 日志配置

### 启用详细日志

编辑 `thermal_api.py`：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('thermal_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 在路由中使用
@app.route('/api/v1/generate-pdf', methods=['POST'])
def generate_pdf():
    logger.info(f'生成 PDF: {patient_name}')
    # ...
```

---

## 🔄 更新和维护

### 更新依赖
```bash
pip install --upgrade -r requirements.txt
```

### 备份重要文件
```bash
# 备份模板和日志
xcopy thermal_report_template.docx backup\ /Y
xcopy *.log backup\ /Y
```

### 监控服务状态

创建健康检查脚本（`monitor.py`）：

```python
import requests
import time
from datetime import datetime

def health_check():
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✅ 服务健康")
            return True
    except:
        print(f"[{datetime.now()}] ❌ 服务离线！")
        # 可选：自动重启或告警
        return False

# 每 5 分钟检查一次
while True:
    health_check()
    time.sleep(300)
```

---

## 📞 技术支持

### 获取帮助

1. **查看文档**：
   - `API_USAGE_GUIDE.md` - 详细使用文档
   - `thermal_api.py` 中的代码注释

2. **运行测试**：
   ```bash
   python test_api.py
   ```

3. **检查日志**：
   ```bash
   tail -f thermal_api.log  # Linux/macOS
   Get-Content thermal_api.log -Tail 20  # PowerShell
   ```

---

## 📋 检查清单

部署前请确认：

- [ ] Python 3.7+ 已安装
- [ ] 所有依赖已安装 (`pip install -r requirements.txt`)
- [ ] LibreOffice 已安装（PDF 转换必需）
- [ ] 模板文件 `thermal_report_template.docx` 存在
- [ ] 健康检查通过 (`curl http://localhost:5000/health`)
- [ ] 集成测试通过 (`python test_api.py`)
- [ ] 防火墙允许端口 5000（或使用的端口）
- [ ] 有足够的磁盘空间存储 PDF 输出
- [ ] 配置了备份策略

---

**版本**: 1.0.0  
**最后更新**: 2024-01-15  
**维护者**: 热成像系统团队
