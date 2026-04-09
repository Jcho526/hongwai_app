# 🎯 App启动与屏幕投射集成方案

## 📋 项目概述

本方案为你的红外热成像健康管理系统提供了完整的解决方案，实现：

1. **自动启动远程App** - "红外热成像健康管理平台"
2. **自动登录** - 无需手动输入验证码，自动勾选协议并登录
3. **屏幕投射** - 将远程App的屏幕实时投射到我们的App中
4. **双屏同步** - 本地摄像头 + 远程屏幕并排显示
5. **触摸转发** - 点击远程屏幕可直接控制远程App

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    我们的App（主应用）                      │
│  ┌────────────┬──────────────────────┬──────────────────┐  │
│  │ 登录页面   │      主菜单          │   实时监控页面    │  │
│  │ (index)    │     (main)           │  (liveMonitor)   │  │
│  └────────────┴──────────────────────┴──────────────────┘  │
│         ↓                                   ↓               │
│    ┌──────────────────────────────────────────────────┐    │
│    │        appLauncher Service (服务层)             │    │
│    │  • 启动远程App  • 自动登录  • 屏幕投射          │    │
│    └──────────────────────────────────────────────────┘    │
│         ↓                    ↓              ↓               │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓              ↓
┌─────────────────────────────────────────────────────────────┐
│              原生模块（需要开发的部分）                      │
│  ┌──────────────┬──────────────┬──────────────────────┐   │
│  │ thermal-adb  │ thermal-     │ thermal-webrtc-     │   │
│  │  -module     │  camera-     │ module              │   │
│  │              │  module      │                      │   │
│  └──────────────┴──────────────┴──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓              ↓
┌─────────────────────────────────────────────────────────────┐
│              远程App："红外热成像健康管理平台"              │
│         （需要支持Deep Link或ADB启动）                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 文件结构

```
services/
├── appLauncher.js          ← 核心服务：App启动与屏幕投射
├── remoteScreenDisplay.js  ← 远程屏幕显示组件
├── auth.js                 ← 认证服务
├── http.js                 ← HTTP请求服务
└── ...

pages/
├── index/
│   └── index.vue           ← 登录页
├── main/
│   └── main.vue            ← 主菜单页
├── capture/
│   ├── capture.vue         ← 旧的采图页面
│   ├── captureList.vue
│   └── liveMonitor.vue     ← ✨ 新的双屏监控页面
└── ...
```

---

## 🚀 使用流程

### 1️⃣ 登录应用
用户在 `pages/index/index.vue` 登录成功后，进入主菜单。

### 2️⃣ 点击"实时监控"
在 `pages/main/main.vue` 点击"实时监控"按钮，跳转到：
```javascript
uni.navigateTo({
  url: '/pages/capture/liveMonitor'
});
```

### 3️⃣ 页面自动启动远程App
`liveMonitor.vue` 的 `onShow()` 生命周期自动执行：
```javascript
async initRemoteScreencast() {
  // 1. 检查远程App是否运行
  const isRunning = await appLauncher.isTargetAppRunning();
  
  // 2. 如果没有运行，则启动它
  if (!isRunning) {
    await appLauncher.launchTargetApp();  // ← 自动启动
  }
  
  // 3. 启动屏幕投射
  await appLauncher.startScreencast();
}
```

### 4️⃣ 远程App自动登录
启动后，触发一系列ADB命令：
```javascript
// 等待3秒（App加载时间）
setTimeout(() => {
  this.autoClickAgree();    // ← 自动勾选协议
}, 3000);

// 500ms后点击登录
setTimeout(() => {
  this.autoClickLogin();    // ← 自动登录
}, 3500);
```

### 5️⃣ 屏幕投射开始
登录成功后，远程App的屏幕实时投射到我们的App的右侧区域。

### 6️⃣ 点击"实时监控"
用户在我们的App中看到远程App的屏幕，点击其中的"实时监控"按钮。
通过 `forwardTouchToRemote()` 函数，这个触摸事件被转发到远程App。

### 7️⃣ 远程App的实时监控开始
远程App进入实时监控页面，我们可以：
- 看到远程摄像头画面（投射到右侧）
- 点击左侧本地摄像头进行本地采图
- 点击"同步采图"同时采集本地和远程的图像

---

## 🔌 原生模块开发指南

### 需要开发的3个原生模块

#### 1. `thermal-adb-module` (必须)

**功能**：通过ADB与Android设备通信

**方法列表**：

```javascript
// 1. 启动应用
adbModule.launchApp({
  packageName: 'com.thermal.health',
  activity: 'com.thermal.health.LoginActivity'
}, callback);

// 2. 点击屏幕上的坐标
adbModule.clickPoint({
  x: 400,
  y: 600
}, callback);

// 3. 检查App是否运行
adbModule.isAppRunning({
  packageName: 'com.thermal.health'
}, callback);

// 4. 关闭App
adbModule.killApp({
  packageName: 'com.thermal.health'
}, callback);

// 5. 截屏
adbModule.takeScreenshot({
  packageName: 'com.thermal.health'
}, callback);

// 6. 触摸按下
adbModule.touchDown({ x: 100, y: 200 }, callback);

// 7. 触摸移动
adbModule.touchMove({ x: 150, y: 250 }, callback);

// 8. 触摸抬起
adbModule.touchUp({ x: 150, y: 250 }, callback);
```

**回调格式**：
```javascript
{
  success: true,      // 操作是否成功
  error: '',          // 错误信息（如果有）
  data: {},           // 返回数据（如截屏的base64）
  imageBase64: ''     // 仅用于takeScreenshot
}
```

---

#### 2. `thermal-webrtc-module` (可选 - 高级方案)

**功能**：通过WebRTC进行实时视频流传输（更流畅的屏幕投射）

**方法列表**：

```javascript
// 1. 启动WebRTC屏幕投射
rtcModule.startScreencast({
  targetPackage: 'com.thermal.health',
  serverUrl: 'wss://your-signal-server.com:8443'
}, callback);

// 2. 停止屏幕投射
rtcModule.stopScreencast(callback);

// 3. 发送触摸事件
rtcModule.forwardTouch({
  type: 'down',  // 'down', 'move', 'up'
  x: 100,
  y: 200
}, callback);
```

---

#### 3. `thermal-camera-module` (可选 - 增强本地摄像头)

**功能**：增强的摄像头控制（用于本地采图）

**方法列表**：

```javascript
// 1. 启动摄像头
cameraModule.startCamera({
  mode: 'thermal',  // 热成像模式
  fps: 30
}, callback);

// 2. 采图
cameraModule.capture({
  format: 'base64'  // 或 'file'
}, callback);

// 3. 停止摄像头
cameraModule.stopCamera(callback);
```

---

## 🛠️ 开发实施步骤

### 第1步：配置远程App信息

编辑 `services/appLauncher.js`，修改包名和Activity名称：

```javascript
this.targetAppPackage = 'com.thermal.health';     // ← 改为实际的包名
this.targetAppActivity = 'com.thermal.health.LoginActivity';  // ← 改为实际的Activity
```

### 第2步：开发原生模块

创建对应的Uniapp插件（通常用Java/Kotlin）:

```
nativeplugins/
├── thermal-adb-module/
│   ├── android/
│   │   └── ThermalAdbModule.kt      (Kotlin实现)
│   └── package.json
└── thermal-webrtc-module/
    ├── android/
    │   └── ThermalWebRTCModule.kt
    └── package.json
```

### 第3步：更新pages.json

注册新页面：

```json
{
  "path": "pages/capture/liveMonitor",
  "style": {
    "navigationStyle": "custom"
  }
}
```

### 第4步：集成到主菜单

修改 `pages/main/main.vue`，更改"实时监控"按钮的跳转：

```javascript
// 原代码
goToLive() {
  uni.navigateTo({
    url: '/pages/capture/capture'  // ← 旧页面
  });
}

// 修改为
goToLive() {
  uni.navigateTo({
    url: '/pages/capture/liveMonitor'  // ← 新页面
  });
}
```

### 第5步：配置信令服务器（可选）

如果使用WebRTC方案，配置信令服务器：

```javascript
// appLauncher.js
serverUrl: 'wss://your-signal-server.com:8443'  // ← 改为你的服务器
```

---

## 🔑 关键实现细节

### 自动登录流程

```javascript
async launchTargetApp() {
  // 1. 通过ADB启动应用
  adbModule.launchApp({
    packageName: 'com.thermal.health',
    activity: 'com.thermal.health.LoginActivity'
  });

  // 2. 等待3秒让界面加载完成
  await new Promise(resolve => setTimeout(resolve, 3000));

  // 3. 自动点击"同意"按钮（坐标需要根据实际调整）
  adbModule.clickPoint({ x: 100, y: 600 });

  // 4. 等待500ms
  await new Promise(resolve => setTimeout(resolve, 500));

  // 5. 自动点击"登录"按钮
  adbModule.clickPoint({ x: 400, y: 700 });

  // 6. 等待2秒让登录完成
  await new Promise(resolve => setTimeout(resolve, 2000));

  // 7. 开始屏幕投射
  await appLauncher.startScreencast();
}
```

### 屏幕投射方案（优先级）

1. **WebRTC** (最佳) - 实时流、低延迟、高品质
2. **ADB截屏轮询** (良好) - 简单易实现、延迟≈500ms、帧率20fps
3. **摄像头直播** (可用) - 需要远程App支持、帧率30fps

### 触摸事件转发

```javascript
onRemoteScreenTouch(type, event) {
  const touch = event.touches[0];
  
  // 获取屏幕容器信息
  const rect = element.getBoundingClientRect();
  
  // 计算相对坐标
  const relativeX = touch.clientX - rect.left;
  const relativeY = touch.clientY - rect.top;
  
  // 缩放到目标分辨率（假设目标分辨率1920x1080）
  const scaledX = Math.floor(relativeX * (1920 / rect.width));
  const scaledY = Math.floor(relativeY * (1080 / rect.height));
  
  // 转发到远程应用
  adbModule.clickPoint({ x: scaledX, y: scaledY });
}
```

---

## 🎨 UI界面说明

### liveMonitor.vue 页面布局

```
┌─────────────────────────────────────────────┐
│  实时监控（双屏模式）  [远程应用: 运行中]   │  ← 顶部状态栏
├───────────────┬───────────────────────────┤
│               │                           │
│   本地摄像头  │   远程投射屏幕            │  ← 主内容区
│   （左侧）    │   （右侧，支持触摸）      │
│               │                           │
├───────────────┴───────────────────────────┤
│ 远程  双屏  采图  同步采图  退出            │  ← 底部工具栏
└─────────────────────────────────────────────┘
```

### 界面特性

- ✅ 双屏并排显示（本地 + 远程）
- ✅ 触摸点实时显示（调试用）
- ✅ FPS显示（投射帧率）
- ✅ 远程App状态监控
- ✅ 响应式设计（支持平板横屏）

---

## 📊 性能指标

| 指标 | 预期值 | 实现方案 |
|------|--------|---------|
| 启动时间 | <5秒 | ADB启动 |
| 屏幕投射延迟 | 200-500ms | ADB截屏或WebRTC |
| 投射帧率 | 20-30fps | ADB截屏轮询500ms |
| 触摸转发延迟 | <100ms | ADB直接点击 |
| 内存占用 | <200MB | 优化图像缓存 |

---

## 🐛 故障排查

### 问题1：ADB模块返回undefined

**原因**：原生插件未正确安装或平台不支持

**解决**：
```javascript
if (!adbModule) {
  console.warn('ADB模块不可用，使用降级方案');
  // 降级到Deep Link或手动启动
}
```

### 问题2：屏幕投射黑屏

**可能原因**：
1. 远程App还未进入摄像头界面
2. ADB截屏权限不足
3. 图像编码失败

**解决**：
1. 增加等待时间
2. 检查ADB权限
3. 使用WebRTC方案

### 问题3：触摸不响应

**可能原因**：
1. 坐标缩放计算错误
2. 远程App分辨率不是1920x1080
3. ADB权限不足

**解决**：
1. 修改缩放比例（见下方）
2. 获取实际分辨率动态调整
3. 检查ADB权限

---

## 📱 分辨率适配

如果远程App的分辨率不是1920x1080，需要修改缩放比例：

```javascript
// appLauncher.js 中修改
const REMOTE_WIDTH = 1920;   // ← 改为实际宽度
const REMOTE_HEIGHT = 1080;  // ← 改为实际高度

// 然后在forwardTouchToRemote中使用
const scaledX = Math.floor(relativeX * (REMOTE_WIDTH / rect.width));
const scaledY = Math.floor(relativeY * (REMOTE_HEIGHT / rect.height));
```

---

## 🔐 安全考虑

1. **包名验证**：启动前验证目标App的包名和签名
2. **权限检查**：使用ADB前检查是否有USB调试权限
3. **账户隐私**：不要在代码中硬编码登录凭证
4. **屏幕数据**：考虑对投射数据进行加密

---

## 📚 相关资源

- [Uni-app 官方文档](https://uniapp.dcloud.io/)
- [Android ADB 文档](https://developer.android.com/studio/command-line/adb)
- [WebRTC 文档](https://webrtc.org/)
- [UniApp 原生插件开发](https://nativesupport.dcloud.net.cn/)

---

## ✅ 集成检查清单

- [ ] 修改 `appLauncher.js` 中的包名和Activity名
- [ ] 开发 `thermal-adb-module` 原生插件
- [ ] （可选）开发 `thermal-webrtc-module` 插件
- [ ] 在 `pages.json` 中注册 `liveMonitor.vue` 页面
- [ ] 修改 `pages/main/main.vue` 的 `goToLive()` 方法
- [ ] 测试自动启动远程App功能
- [ ] 测试自动登录功能
- [ ] 测试屏幕投射功能
- [ ] 测试触摸转发功能
- [ ] 在实际平板上进行完整流程测试

---

## 💡 建议与扩展

### 短期优化
1. 增加启动进度提示
2. 优化截屏帧率（考虑性能）
3. 添加错误重试机制
4. 实现截屏缓存

### 中期功能
1. 支持录屏（保存双屏视频）
2. 手势识别（多指触摸转发）
3. 截图标注
4. 快速键盘输入转发

### 长期规划
1. WebRTC P2P直连（跳过服务器）
2. 多设备屏幕投射
3. AI辅助识别功能
4. 云端数据同步

---

**创建日期**：2026年3月22日  
**最后更新**：2026年3月22日  
**版本**：v1.0  
**作者**：GitHub Copilot
