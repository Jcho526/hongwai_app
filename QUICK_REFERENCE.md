# 🚀 快速参考卡片

## 启动步骤（3 步）

### 步骤 1️⃣：启动 API 服务
```
打开 PowerShell，复制粘贴：
conda activate dip && cd "C:\Users\1\Desktop\新\red_pdf" && python thermal_api.py
```
✅ 看到 `Running on http://127.0.0.1:5000` 表示成功

### 步骤 2️⃣：启动 HBuilder
- 打开 HBuilder
- 打开项目：`C:\Users\1\Desktop\新`
- 按 `Ctrl+Alt+H` 启动到浏览器

### 步骤 3️⃣：测试功能
1. 进入应用
2. 进入 **系统设置**
3. 向下滚动找到 **🔥 API 服务配置**
4. 点击 **检查连接** → 看到 🟢**已连接** 表示成功

---

## 使用流程

```
应用首页
  ↓
选择患者 / 新增患者
  ↓
进入采图页面
  ↓
点击"采图"按钮 → 拍照（可拍 2-4 张）
  ↓
点击"生成报告"按钮
  ↓
等待 2-3 秒
  ↓
自动跳转到报告列表
  ↓
✅ 完成！
```

---

## 常见问题速查表

| 问题 | 解决方案 |
|------|--------|
| ❌ "无法连接到 API" | 检查 PowerShell 是否在运行 API |
| 🔴 API 显示离线 | 在系统设置中点击"检查连接" |
| ⏱️ 生成报告很慢 | 正常的，需要 2-3 秒 |
| 📁 DOCX 打不开 | 检查 `python-docx` 是否正确安装 |
| 🌐 真机无法连接 | 修改 API 地址为 PC IP 地址 |

---

## 关键地址

| 项目 | 地址/路径 |
|------|----------|
| API 服务 | `http://localhost:5000` |
| API 健康检查 | `http://localhost:5000/health` |
| API 状态 | `http://localhost:5000/api/v1/status` |
| HBuilder 项目 | `C:\Users\1\Desktop\新` |
| API 服务器 | `C:\Users\1\Desktop\新\red_pdf` |
| 配置文件 | `services/apiConfig.js` |
| 采图页面 | `pages/capture/capture.vue` |
| 设置页面 | `pages/systemSettings/systemSettings.vue` |

---

## 配置 API 地址

### 开发环境（本地）
编辑 `services/apiConfig.js`：
```javascript
development: {
  baseUrl: 'http://localhost:5000',  // ← 这里
}
```

### 生产环境（其他服务器）
编辑 `services/apiConfig.js`：
```javascript
production: {
  baseUrl: 'http://192.168.1.100:5000',  // ← 改为实际 IP
}
```

---

## 文件清单

✅ **已创建/修改的文件：**
- `services/apiConfig.js` - API 配置
- `pages/capture/capture.vue` - 采图页面（已集成）
- `pages/systemSettings/systemSettings.vue` - 设置页面（已集成）
- `API_TEST.html` - API 测试页面
- `test_api_direct.py` - Python 测试脚本

⚠️ **需要单独启动：**
- API 服务（PowerShell）
- HBuilder 应用

---

## 测试工具

### 方法 1：HTML 网页测试
```
打开：C:\Users\1\Desktop\新\API_TEST.html
功能：上传图片 → 生成报告 → 下载 DOCX
```

### 方法 2：Python 脚本测试
```powershell
conda activate dip
cd "C:\Users\1\Desktop\新"
python test_api_direct.py
```

### 方法 3：应用内测试
```
打开应用 → 系统设置 → API 服务配置 → 检查连接
```

---

## 成功标志 ✅

- [ ] PowerShell 显示 `Running on http://127.0.0.1:5000`
- [ ] HBuilder 应用可以打开
- [ ] 系统设置中 API 状态显示 🟢**已连接**
- [ ] 可以拍照采集图片
- [ ] 可以点击"生成报告"成功生成 DOCX
- [ ] 报告出现在报告列表中

如果以上所有项都 ✅，说明集成成功！

---

**需要更详细的文档？** 查看 `HBUILDER_INTEGRATION_GUIDE.md`
