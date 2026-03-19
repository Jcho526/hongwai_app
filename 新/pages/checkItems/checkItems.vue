<template>
  <view class="page">
    <!-- 顶部栏 -->
    <view class="header">
      <view class="back" @tap="goBack">‹</view>
      <text class="header-title">检查项目</text>
      <view class="back-holder"></view>
    </view>

    <scroll-view class="body" scroll-y>
      <!-- 选择项目 -->
      <view class="panel">
        <text class="panel-title">选择项目：</text>

        <!-- 三按钮横排（稳定） -->
        <view class="mode-row">
          <view class="mode-btn" :class="{ active: mode === 'quanke' }" @tap="setMode('quanke')">
            <image class="mode-icon" src="/static/icons/quanke.png" mode="aspectFit" />
            <text class="mode-text">全科</text>
          </view>

          <view class="mode-btn" :class="{ active: mode === 'mianzhen' }" @tap="setMode('mianzhen')">
            <image class="mode-icon" src="/static/icons/mianzhen.png" mode="aspectFit" />
            <text class="mode-text">面诊</text>
          </view>

          <view class="mode-btn" :class="{ active: mode === 'zhongyi' }" @tap="setMode('zhongyi')">
            <image class="mode-icon" src="/static/icons/zhongyi.png" mode="aspectFit" />
            <text class="mode-text">中医治未病</text>
          </view>
        </view>

        <!-- 红字标题（居中） -->
        <text class="red-title">{{ redTitle }}</text>

        <!-- 说明 -->
        <text class="desc">{{ descText }}</text>

        <!-- 热图：全科/中医（4张） -->
        <view v-if="mode !== 'mianzhen'" class="heat-grid">
          <view class="heat-cell" v-for="(img, idx) in heat4" :key="idx">
            <text class="heat-no">{{ idx + 1 }}</text>
            <image class="heat-img" :src="img" mode="aspectFit" />
          </view>
        </view>

        <!-- 热图：面诊（2张） -->
        <view v-else class="face-row">
          <view class="face-cell" v-for="(img, idx) in heat2" :key="idx">
            <image class="face-img" :src="img" mode="aspectFit" />
          </view>
        </view>
      </view>

      <!-- 报告选项 + 系统选项：只在“全科”显示 -->
      <view v-if="mode === 'quanke'" class="panel">
        <text class="panel-title">报告选项:</text>

        <view class="opt-row">
          <view class="opt-item" @tap="toggleReport('system')">
            <view class="ck" :class="{ on: report.system }"><text v-if="report.system" class="tick">✓</text></view>
            <text class="opt-text">系统</text>
          </view>

          <view class="opt-item" @tap="toggleReport('cnwe')">
            <view class="ck" :class="{ on: report.cnwe }"><text v-if="report.cnwe" class="tick">✓</text></view>
            <text class="opt-text">中西医两份</text>
          </view>
        </view>

        <view class="opt-row">
          <view class="opt-item" @tap="toggleReport('part')">
            <view class="ck" :class="{ on: report.part }"><text v-if="report.part" class="tick">✓</text></view>
            <text class="opt-text">部位</text>
          </view>

          <view class="opt-item" @tap="toggleReport('single')">
            <view class="ck" :class="{ on: report.single }"><text v-if="report.single" class="tick">✓</text></view>
            <text class="opt-text">单项报告</text>
          </view>
        </view>

        <!-- 系统选项 -->
        <view class="sys-block">
          <text class="panel-title2">系统选项:</text>

          <view class="sys-grid">
            <view class="sys-item" v-for="s in sysList" :key="s.key" @tap="toggleSys(s.key)">
              <view class="ck small" :class="{ on: s.checked }">
                <text v-if="s.checked" class="tick">✓</text>
              </view>
              <text class="sys-text">{{ s.name }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 医生输入 -->
      <view class="doctor-panel">
        <view class="doctor-row">
          <text class="doctor-label">医生：</text>
          <input class="doctor-input" v-model="doctor" placeholder="请输入检测医生名字" placeholder-class="ph" />
        </view>
      </view>

      <view style="height: 170rpx;"></view>
    </scroll-view>

    <!-- 底部栏 -->
    <view class="footer">
      <view class="foot-btn" @tap.stop="onTake">
        <image class="foot-icon" src="/static/icons/take.png" mode="aspectFit" />
        <text class="foot-text">拍照</text>
      </view>

      <view class="foot-split"></view>

      <view class="foot-btn" @tap.stop="onBaoGao">
        <image class="foot-icon" src="/static/icons/baogao.png" mode="aspectFit" />
        <text class="foot-text">出报告采图</text>
      </view>

      <view class="foot-split"></view>

      <view class="foot-btn" @tap.stop="goBack">
        <image class="foot-icon" src="/static/icons/out2.png" mode="aspectFit" />
        <text class="foot-text">退出</text>
      </view>

      <view class="safe-pad"></view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // ✅ 补上：从 person.vue 传过来的人员ID
      personId: "",

      mode: "quanke",
      doctor: "",
      report: {
        system: true,
        cnwe: false,
        part: false,
        single: false
      },
      heat4: [
        "/static/icons/re1.png",
        "/static/icons/re2.png",
        "/static/icons/re3.png",
        "/static/icons/re4.png"
      ],
      heat2: [
        "/static/icons/re5.png",
        "/static/icons/re6.png"
      ],
      sysList: [
        { key: "loop", name: "循环系统", checked: true },
        { key: "breath", name: "呼吸系统", checked: true },
        { key: "digest", name: "消化系统", checked: true },
        { key: "uro", name: "泌尿生殖系统", checked: true },
        { key: "sport", name: "运动系统", checked: true },
        { key: "endo", name: "内分泌与免疫系统", checked: true },
        { key: "other", name: "其他", checked: true }
      ]
    };
  },

  // ✅ 补上：接收 person.vue 传来的 personId
  onLoad(query) {
    this.personId = (query && query.personId) ? String(query.personId) : "";
  },

  computed: {
    redTitle() {
      if (this.mode === "mianzhen") return "面诊的采集标准";
      if (this.mode === "zhongyi") return "中医治未病采集标准";
      return "全科、康复，内科(重大疾病风险)的采图标准";
    },
    descText() {
      if (this.mode === "mianzhen") {
        return "采集人体正面部1张，仰头1张，共2张。头面部尽量占满屏幕。";
      }
      return "双手向下，掌心向前，五指打开，双腿自然分开。按上身正面，上身背面，下身背面，下身正面共采集4张热图。建议按照左侧的序号采图";
    }
  },

  methods: {
    goBack() {
      uni.navigateBack();
    },

    setMode(m) {
      this.mode = m;
    },

    toggleReport(k) {
      this.report[k] = !this.report[k];
    },

    toggleSys(key) {
      const i = this.sysList.findIndex(x => x.key === key);
      if (i >= 0) this.sysList[i].checked = !this.sysList[i].checked;
    },

    // ✅ 拍照：初始化采集会话 → 跳转采图页
    onTake() {
      const session = {
        personId: this.personId || "",
        mode: this.mode,                       // quanke / mianzhen / zhongyi
        max: this.mode === "mianzhen" ? 2 : 4,
        images: []
      };

      try {
        uni.setStorageSync("capture_session", session);
      } catch (e) {}

      const url = "/pages/capture/capture";

      uni.navigateTo({
        url,
        success: () => {
          console.log("navigateTo success:", url);
        },
        fail: (err) => {
          console.error("navigateTo fail:", err);
          uni.showToast({
            title: "跳转失败：" + (err.errMsg || ""),
            icon: "none"
          });
        }
      });
    },

    // ✅ “出报告采图”你先占位（后续你要区分逻辑再细化）
    onBaoGao() {
      uni.showToast({ title: "出报告采图（待接入）", icon: "none" });
      // 如果你希望它也进入采图页，就直接调用 onTake()
      // this.onTake();
    }
  }
};
</script>

<style scoped>
/* 整体 */
.page {
  min-height: 100vh;
  background: #efefef;
  padding-bottom: 150rpx;
}

/* 顶部 */
.header {
  height: 110rpx;
  background: #17b3a8;
  display: flex;
  align-items: center;
  padding: 0 24rpx;
  box-sizing: border-box;
}
.back {
  width: 90rpx;
  font-size: 56rpx;
  color: #fff;
  line-height: 1;
}
.header-title {
  flex: 1;
  text-align: center;
  color: #fff;
  font-size: 38rpx;
  font-weight: 700;
}
.back-holder { width: 90rpx; }

.body { height: calc(100vh - 110rpx - 150rpx); }

/* 白色块 */
.panel {
  background: #fff;
  margin: 16rpx 16rpx 0;
  border-radius: 10rpx;
  padding: 22rpx;
  box-sizing: border-box;
}

.panel-title {
  font-size: 32rpx;
  color: #333;
  margin-bottom: 16rpx;
}
.panel-title2 {
  font-size: 32rpx;
  color: #333;
  margin: 22rpx 0 16rpx;
}

/* 3按钮横排 */
.mode-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 18rpx;
}
.mode-btn {
  flex: 1;
  height: 150rpx;
  border-radius: 10rpx;
  border: 6rpx solid #666;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-sizing: border-box;
}
.mode-btn.active {
  border-color: #17b3a8;
}
.mode-icon {
  width: 86rpx;
  height: 86rpx;
}
.mode-text {
  font-size: 32rpx;
  font-weight: 700;
  color: #111;
}

/* 红标题居中 */
.red-title {
  display: block;
  text-align: center;
  color: #d11;
  font-size: 32rpx;
  font-weight: 800;
  margin: 18rpx 0 10rpx;
}

/* 描述 */
.desc {
  font-size: 28rpx;
  line-height: 44rpx;
  color: #111;
}

/* 4热图 2x2 */
.heat-grid {
  margin-top: 18rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}
.heat-cell {
  width: calc(50% - 5rpx);
  height: 320rpx;
  background: #000;
  position: relative;
  overflow: hidden;
}
.heat-no {
  position: absolute;
  left: 10rpx;
  top: 8rpx;
  color: #d11;
  font-size: 30rpx;
  font-weight: 800;
  z-index: 2;
}
.heat-img {
  width: 100%;
  height: 100%;
}

/* 面诊 2图 */
.face-row {
  margin-top: 18rpx;
  display: flex;
  gap: 10rpx;
}
.face-cell {
  flex: 1;
  height: 340rpx;
  background: #000;
  overflow: hidden;
}
.face-img {
  width: 100%;
  height: 100%;
}

/* 报告选项 */
.opt-row {
  display: flex;
  margin-top: 18rpx;
}
.opt-item {
  width: 50%;
  display: flex;
  align-items: center;
  gap: 14rpx;
}
.opt-text {
  font-size: 30rpx;
  color: #111;
}

/* checkbox */
.ck {
  width: 36rpx;
  height: 36rpx;
  border-radius: 4rpx;
  border: 4rpx solid #8b8b8b;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}
.ck.small {
  width: 34rpx;
  height: 34rpx;
}
.ck.on {
  border-color: #0f8f86;
  background: #0f8f86;
}
.tick {
  color: #fff;
  font-size: 26rpx;
  font-weight: 900;
  line-height: 1;
}

/* 系统选项布局 */
.sys-grid {
  display: flex;
  flex-wrap: wrap;
  row-gap: 18rpx;
}
.sys-item {
  width: 50%;
  display: flex;
  align-items: center;
  gap: 14rpx;
}
.sys-text {
  font-size: 30rpx;
  color: #111;
}

/* 医生输入块 */
.doctor-panel {
  background: #fff;
  margin: 16rpx 16rpx 0;
  border-radius: 10rpx;
  padding: 18rpx 22rpx;
  box-sizing: border-box;
}
.doctor-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}
.doctor-label {
  font-size: 30rpx;
  color: #333;
}
.doctor-input {
  flex: 1;
  height: 72rpx;
  background: #f2f2f2;
  border-radius: 8rpx;
  padding: 0 16rpx;
  font-size: 28rpx;
  color: #111;
}
.ph { color: #999; }

/* 底部栏 */
.footer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 150rpx;
  background: #fff;
  border-top: 1rpx solid #e6e6e6;
  display: flex;
  z-index: 99999;      /* ✅ 提高层级，避免被 scroll-view 覆盖 */
  pointer-events: auto;
}
.foot-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
}
.foot-icon {
  width: 78rpx;
  height: 78rpx;
}
.foot-text {
  font-size: 30rpx;
  font-weight: 700;
  color: #111;
}
.foot-split {
  width: 2rpx;
  background: #17b3a8;
  opacity: 0.5;
  margin: 22rpx 0;
}
.safe-pad {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: env(safe-area-inset-bottom);
  background: #fff;
}
</style>
