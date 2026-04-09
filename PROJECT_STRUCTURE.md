# 📁 项目文件结构说明

## 核心功能文件

### 前端相关

#### 1. **pages/capture/capture.vue** ⭐ 重要
采图页面，包含"生成报告"功能

**包含的方法：**
```javascript
// 生成报告主方法
async onGenReport()

// 读取图片文件并转换为 Base64
readImageAsBase64(imagePath)

// 调用 PDF 生成 API
async callGeneratePdfApi(imageBase64Data, session)

// 保存生成的报告到本地存储
savePdfInfo(result)
```

**关键按钮：**
```html
<!-- 采图按钮 -->
<view class="tool-item" @tap.stop="onCapture">
  <text class="tool-text">采图</text>
</view>

<!-- 生成报告按钮 -->
<view class="tool-item" @tap.stop="onGenReport">
  <text class="tool-text">生成报告</text>
</view>
```

---

#### 2. **services/apiConfig.js** ⭐ 重要
API 配置和工具函数

**导出的函数：**
```javascript
getApiUrl(endpoint)        // 获取 API URL
getApiTimeout()           // 获取超时时间
getApiConfig()            // 获取完整配置
getBaseUrl()              // 获取基础 URL
checkApiHealth()          // 检查 API 健康状态
getApiStatus()            // 获取 API 状态信息
```

**使用示例：**
```javascript
import { getApiUrl, getApiTimeout } from '../../services/apiConfig.js';

const apiUrl = getApiUrl('generateReport');
const timeout = getApiTimeout();
```

---

#### 3. **pages/systemSettings/systemSettings.vue**
系统设置页面，包含 API 管理功能

**功能：**
- API 连接状态检查
- API 地址配置
- API 详细信息显示

---

### 后端相关

#### 4. **red_pdf/thermal_api.py** ⭐ 重要
Flask REST API 应用

**API 端点：**
```
POST /api/v1/generate-pdf
  - 接收：Base64 图片和患者信息
  - 返回：DOCX 二进制文件

GET /health
  - 健康检查端点

GET /api/v1/status
  - 获取 API 状态信息
```

**启动方式：**
```powershell
cd "C:\Users\1\Desktop\新\red_pdf"
conda activate dip
python thermal_api.py
```

---

#### 5. **red_pdf/thermal_analyzer.py**
热成像分析器（支持库）

#### 6. **red_pdf/thermal_dict.json**
热成像字典数据

---

## 文档文件

### 快速参考

| 文件 | 用途 | 首选人群 |
|------|------|---------|
| **START_HERE.md** | 5分钟快速启动 | 急于上手的人 |
| **README_COMPLETION.md** | 一页纸完成说明 | 想快速了解的人 |
| **TASK_STATUS.md** | 详细任务说明 | 想了解细节的人 |
| **TASK_COMPLETION.md** | 完整流程说明 | 想学习实现的人 |
| **IMPLEMENTATION_COMPLETE.md** | 实现和验证 | 想深入学习的人 |
| **VERIFICATION_CHECKLIST.md** | 验收清单 | 做质量检查的人 |

---

## 完整项目结构

```
c:\Users\1\Desktop\新\
├── 📄 README.md                          # 项目主说明
├── 📄 START_HERE.md ⭐                    # 快速开始（首先看这个！）
├── 📄 README_COMPLETION.md                # 任务完成说明
├── 📄 TASK_STATUS.md                     # 任务状态
├── 📄 TASK_COMPLETION.md                 # 完成验证
├── 📄 IMPLEMENTATION_COMPLETE.md          # 实现完成
├── 📄 VERIFICATION_CHECKLIST.md           # 验收清单
│
├── 📁 pages/                             # 前端页面
│   ├── 📁 capture/                       # 采图页面
│   │   ├── capture.vue ⭐ (修改)         # 包含 4 个新方法
│   │   └── captureList.vue
│   ├── 📁 photoRecords/                  # 报告列表页面
│   │   └── photoRecords.vue
│   ├── 📁 person/                        # 患者信息页面
│   │   ├── person.vue
│   │   └── addPerson.vue
│   ├── 📁 systemSettings/                # 系统设置
│   │   └── systemSettings.vue (修改)     # API 管理
│   └── 📁 utils/
│       └── personStore.js
│
├── 📁 services/                          # 服务模块
│   ├── apiConfig.js ⭐ (新建)             # API 配置
│   ├── auth.js
│   ├── http.js
│   ├── persons.js
│   ├── reports.js
│   └── systemSettings.js
│
├── 📁 red_pdf/                           # 后端 Python 目录
│   ├── 📄 thermal_api.py ⭐ (修改)       # Flask REST API
│   ├── 📄 thermal_analyzer.py            # 热成像分析器
│   ├── 📄 thermal_dict.json              # 热成像字典
│   ├── 📄 read_pdf.py
│   ├── 📄 requirements.txt
│   ├── 📄 environment.yml
│   ├── 📄 activate_env.ps1
│   ├── 📄 activate_env.bat
│   ├── 📄 start_api.ps1
│   ├── 📄 start_api.bat
│   └── 📁 (其他 PDF 文件和资源)
│
├── 📁 server/                            # Node.js 后端（可选）
│   ├── package.json
│   ├── app.js
│   └── ...
│
├── 📁 static/                            # 静态资源
│   ├── 📁 icons/                         # 图标
│   └── 📁 reports/                       # 报告样例
│
└── 📁 unpackage/                         # HBuilder 生成目录

⭐ = 重要改动或新建文件
(修改) = 已修改的现有文件
(新建) = 新创建的文件
```

---

## 使用流程

### 1️⃣ 启动 API
```powershell
# PowerShell 窗口 1
cd "C:\Users\1\Desktop\新\red_pdf"
conda activate dip
python thermal_api.py

# 看到这样的输出说明成功：
# Running on http://127.0.0.1:5000
```

### 2️⃣ 启动应用
```
HBuilder 窗口：
1. 打开项目 → C:\Users\1\Desktop\新
2. Ctrl+Alt+H 运行到浏览器
```

### 3️⃣ 测试功能
```
1. 进入应用
2. 选择患者
3. 进入采图页面
4. 点击"采图" → 拍照
5. 点击"生成报告" → 自动生成！
```

---

## 关键文件速查

### 如果我想...

#### ...修改 API 地址
→ 编辑 `services/apiConfig.js`，修改 `API_CONFIG.development.baseUrl`

#### ...修改 API 超时时间
→ 编辑 `services/apiConfig.js`，修改 `timeout` 字段

#### ...看采图页面的代码
→ 打开 `pages/capture/capture.vue`，搜索 `onGenReport`

#### ...调试 API 请求
→ 打开浏览器 F12，Network 标签，看 POST 请求

#### ...查看保存的报告数据
→ 打开浏览器 F12，Application → LocalStorage，找 `person_reports_*`

#### ...修改 API 响应数据
→ 编辑 `red_pdf/thermal_api.py`，修改 `generate_pdf` 函数

#### ...添加新的 API 端点
→ 在 `red_pdf/thermal_api.py` 添加 `@app.route()` 装饰器

#### ...修改报告生成模板
→ 编辑 `red_pdf/thermal_analyzer.py` 中的 `ThermalReportGenerator` 类

---

## 环境配置

### Python 环境（后端）
```
环境管理器：conda
环境名称：dip
Python 版本：3.8+

必装包：
- flask==3.1.3
- python-docx==1.2.0
- requests==2.32.5
```

### Node.js 环境（前端）
```
框架：UniApp + Vue 3
运行工具：HBuilder
目标平台：Web / iOS / Android
```

---

## 常用命令

### 启动 API
```powershell
cd "C:\Users\1\Desktop\新\red_pdf"
conda activate dip
python thermal_api.py
```

### 停止 API
```powershell
Ctrl+C  (在 PowerShell 中)
```

### 激活 Python 环境
```powershell
conda activate dip
```

### 查看 Python 包
```powershell
conda list
```

### 更新 Python 包
```powershell
pip install --upgrade flask python-docx requests
```

---

## 文件修改历史

| 文件 | 修改内容 | 日期 |
|------|--------|------|
| `pages/capture/capture.vue` | 添加 4 个方法 | 2026-03-22 |
| `services/apiConfig.js` | 新建文件 | 2026-03-22 |
| `red_pdf/thermal_api.py` | 优化和增强 | 2026-03-22 |
| `pages/systemSettings/systemSettings.vue` | 添加 API 管理 | 2026-03-22 |

---

## 🎯 快速导航

**我是新手，怎么开始？**
→ 看 `START_HERE.md`

**我想了解任务完成情况**
→ 看 `README_COMPLETION.md` 或 `TASK_STATUS.md`

**我想深入学习实现细节**
→ 看 `IMPLEMENTATION_COMPLETE.md`

**我想做质量检查**
→ 看 `VERIFICATION_CHECKLIST.md`

**我要调试 API**
→ 按 F12，打开浏览器开发工具

**我找不到某个文件**
→ 参考上面的项目结构

---

**记住：一切都已准备好，只需启动 API 和应用即可！** 🚀
