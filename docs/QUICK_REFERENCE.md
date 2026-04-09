# 🎯 App启动器 - 快速参考卡

## 📋 一页纸快速查询

### 核心API

```javascript
// 启动远程应用（自动登录）
await appLauncher.launchTargetApp();

// 启动屏幕投射
await appLauncher.startScreencast();

// 检查应用是否运行
const isRunning = await appLauncher.isTargetAppRunning();

// 在远程应用中点击
await appLauncher.clickRemoteMonitor();

// 停止屏幕投射
await appLauncher.stopScreencast();

// 关闭远程应用
await appLauncher.killTargetApp();

// 监听屏幕更新
uni.$on('screencast-update', (data) => {
  console.log('收到新的屏幕更新:', data.imageBase64);
});
```

---

## 🔧 必要配置（3处）

### 配置1: 包名和Activity

```javascript
// services/appLauncher.js 第8-9行
this.targetAppPackage = 'com.example.thermalhealth';
this.targetAppActivity = 'com.example.thermalhealth.MainActivity';
```

### 配置2: 注册页面

```json
// pages.json 中的 pages 数组添加
{
  "path": "pages/capture/liveMonitor",
  "style": { "navigationStyle": "custom" }
}
```

### 配置3: 更新导航

```javascript
// pages/main/main.vue 的 goToLive() 方法
goToLive() {
  uni.navigateTo({ url: '/pages/capture/liveMonitor' });
}
```

---

## 📱 新页面的主要功能

```
liveMonitor.vue
├─ 左侧: 本地摄像头
├─ 右侧: 远程屏幕（支持触摸）
├─ 顶部: 状态栏（App状态 + FPS）
└─ 底部: 工具栏
   ├─ 远程点击
   ├─ 双屏切换
   ├─ 本地采图
   ├─ 同步采图
   └─ 退出
```

---

## 🎬 自动化流程（内部流程）

```
点击"实时监控"
    ↓
检查远程App是否运行
    ├─ 否: 启动应用 (ADB/Deep Link)
    └─ 是: 跳过启动
    ↓
等待3秒（应用加载）
    ↓
自动点击"同意"按钮 (坐标: 100, 600)
    ↓
自动点击"登录"按钮 (坐标: 400, 700)
    ↓
等待2秒（登录完成）
    ↓
启动屏幕投射 (优先级: WebRTC > ADB > 直播)
    ↓
显示双屏界面
```

---

## 📊 性能基准

| 指标 | 数值 |
|------|------|
| 应用启动时间 | 3-5秒 |
| 屏幕投射延迟 | 200-500ms |
| 屏幕投射帧率 | 2fps |
| 触摸转发延迟 | <200ms |
| 内存占用 | <300MB |

---

## 🐛 常见问题快速解决

### 问题1: 自动点击不工作

**原因**: 坐标不对（与UI布局有关）

**解决**:
```bash
# 获取屏幕分辨率
adb shell wm size

# 截屏查看坐标
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png

# 用图像编辑器打开，测量按钮位置
# 然后修改 appLauncher.js 中的坐标
```

### 问题2: 屏幕投射黑屏

**原因**: 权限不足或格式错误

**解决**:
```javascript
// 增加启动延迟
await this.sleep(5000);  // 改为5秒
await appLauncher.startScreencast();
```

### 问题3: 触摸不响应

**原因**: 坐标缩放比例错误

**解决**:
```javascript
// 获取实际远程分辨率，修改缩放比例
const REMOTE_WIDTH = 1920;   // 实际值
const REMOTE_HEIGHT = 1080;  // 实际值
```

### 问题4: 应用启动失败

**原因**: 包名错误

**解决**:
```bash
# 获取正确的包名
adb shell pm list packages | grep thermal

# 获取正确的Activity
adb shell dumpsys package com.actual.package | grep -A 1 "MAIN"
```

---

## 📂 文件结构

```
services/
├── appLauncher.js          (核心服务 - 318行)
└── remoteScreenDisplay.js  (显示组件 - 149行)

pages/capture/
└── liveMonitor.vue         (双屏页面 - 400行)

docs/
├── README.md               (集成包总览)
├── APP_LAUNCHER_INTEGRATION.md   (完整方案)
├── TECHNICAL_IMPLEMENTATION.md   (技术指南)
├── IMPLEMENTATION_CHECKLIST.md   (检查清单)
└── QUICK_START_DEMO.md     (快速演示)
```

---

## 🔑 关键方法签名

### launchTargetApp()
```javascript
async launchTargetApp(): Promise<boolean>
// 返回: 启动成功为true，失败为false
// 内部: 启动App + 自动登录（3-5秒）
```

### startScreencast()
```javascript
async startScreencast(): Promise<boolean>
// 返回: 启动成功为true，失败为false
// 事件: 发送 'screencast-update' 事件
// 延迟: 200-500ms（取决于方案）
```

### isTargetAppRunning()
```javascript
async isTargetAppRunning(): Promise<boolean>
// 返回: 运行中为true，已停止为false
```

### clickRemoteMonitor()
```javascript
async clickRemoteMonitor(): Promise<void>
// 功能: 在远程应用中模拟点击"实时监控"按钮
// 坐标: 默认 (400, 600)
```

---

## 📡 事件监听

### screencast-update 事件

```javascript
uni.$on('screencast-update', (data) => {
  data.imageBase64    // 截屏的base64编码
  data.timestamp      // 时间戳（毫秒）
  data.streamData     // WebRTC流数据（可选）
});

// 清理监听
uni.$off('screencast-update', handler);
```

---

## 🎨 UI布局

### 宽屏布局（平板横屏）
```
┌──────────────────────────┬──────────────────────────┐
│                          │                          │
│     本地摄像头           │    远程投射屏幕          │
│     (50%)                │    (50%)                 │
│                          │    (支持触摸)            │
│                          │                          │
└──────────────────────────┴──────────────────────────┘
```

### 竖屏布局（手机竖屏）
```
┌──────────────────────────┐
│                          │
│     本地摄像头           │
│     (50%)                │
│                          │
├──────────────────────────┤
│                          │
│    远程投射屏幕          │
│    (50%)                 │
│    (支持触摸)            │
│                          │
└──────────────────────────┘
```

---

## 💻 代码使用示例

### 完整示例

```vue
<script>
import appLauncher from '../../services/appLauncher';

export default {
  data() {
    return {
      remoteScreenImage: null,
      isConnecting: false
    };
  },

  async mounted() {
    try {
      this.isConnecting = true;

      // 1. 启动远程应用
      console.log('启动远程应用...');
      await appLauncher.launchTargetApp();

      // 2. 启动屏幕投射
      console.log('启动屏幕投射...');
      await appLauncher.startScreencast();

      // 3. 监听屏幕更新
      uni.$on('screencast-update', (data) => {
        if (data.imageBase64) {
          this.remoteScreenImage = 'data:image/png;base64,' + data.imageBase64;
        }
      });

      this.isConnecting = false;
      uni.showToast({ title: '连接成功', icon: 'success' });

    } catch (error) {
      this.isConnecting = false;
      uni.showToast({ 
        title: '连接失败: ' + error.message, 
        icon: 'error' 
      });
    }
  },

  beforeUnmount() {
    uni.$off('screencast-update');
    appLauncher.stopScreencast();
  }
}
</script>
```

---

## 🔌 原生模块方法

### thermal-adb-module

```javascript
// 启动应用
adbModule.launchApp({
  packageName: 'com.example.app',
  activity: 'com.example.app.MainActivity'
}, callback);

// 点击屏幕
adbModule.clickPoint({ x: 100, y: 200 }, callback);

// 检查应用
adbModule.isAppRunning({ packageName: 'com.example.app' }, callback);

// 截屏
adbModule.takeScreenshot({ packageName: 'com.example.app' }, callback);

// 触摸事件
adbModule.touchDown({ x: 100, y: 200 }, callback);
adbModule.touchMove({ x: 150, y: 250 }, callback);
adbModule.touchUp({ x: 150, y: 250 }, callback);
```

### 回调格式

```javascript
{
  success: true,          // 操作是否成功
  error: '',              // 错误信息
  imageBase64: '',        // 仅用于截屏
  running: true           // 仅用于isAppRunning
}
```

---

## ⚙️ 配置参考

### 常见分辨率坐标表

#### 1920x1200 (10英寸平板)
```javascript
agreeButtonX: 100,    loginButtonX: 400,   monitorButtonX: 400
agreeButtonY: 600,    loginButtonY: 700,   monitorButtonY: 600
```

#### 2560x1600 (大平板)
```javascript
agreeButtonX: 150,    loginButtonX: 500,   monitorButtonX: 500
agreeButtonY: 800,    loginButtonY: 950,   monitorButtonY: 800
```

#### 1080x1920 (手机竖屏)
```javascript
agreeButtonX: 50,     loginButtonX: 200,   monitorButtonX: 200
agreeButtonY: 1000,   loginButtonY: 1200,  monitorButtonY: 1000
```

---

## 📚 文档导航

| 需要 | 文档 | 时间 |
|------|------|------|
| 快速了解 | QUICK_START_DEMO.md | 15分钟 |
| 完整方案 | APP_LAUNCHER_INTEGRATION.md | 30分钟 |
| 技术细节 | TECHNICAL_IMPLEMENTATION.md | 45分钟 |
| 实施步骤 | IMPLEMENTATION_CHECKLIST.md | 60分钟 |
| 快速查询 | 本文件 (QUICK_REFERENCE.md) | 5分钟 |

---

## 🚀 快速命令

```bash
# 获取应用列表
adb shell pm list packages

# 启动应用
adb shell am start -n com.package/com.package.Activity

# 截屏
adb shell screencap -p /sdcard/screen.png

# 查看日志
adb logcat | grep app-name

# 获取分辨率
adb shell wm size

# 输入文本
adb shell input text "hello"

# 点击屏幕
adb shell input tap 100 200
```

---

## ✨ 工作流速记

```
配置 → 开发模块 → 修改导航 → 测试 → 优化 → 上线

时间: 30min + 4-6h + 5min + 4-5h + 1h = 10-12小时
```

---

## 📞 快速排查

| 症状 | 可能原因 | 解决方案 |
|------|--------|---------|
| 自动点击不工作 | 坐标错误 | 截屏获取正确坐标 |
| 屏幕投射黑屏 | 权限不足 | 增加延迟或使用WebRTC |
| 触摸无响应 | 缩放比例错 | 检查分辨率参数 |
| 应用不启动 | 包名错误 | 用adb查询正确包名 |
| FPS过低 | 硬件性能 | 减少刷新频率 |

---

**打印此卡，放在手边参考！** 📌

最后更新: 2026年3月22日
