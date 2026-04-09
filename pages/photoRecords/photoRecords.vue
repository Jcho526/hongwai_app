<template>
  <view class="page">
    <view class="topbar">
      <view class="back" @tap="goBack">‹</view>
      <text class="title">{{ headerTitle }}</text>
      <view class="right" @tap="onShare">分享照片</view>
    </view>

    <view class="section">
      <text class="section-title">热成像照片</text>
    </view>

    <scroll-view class="body" scroll-y>
      <view v-if="photos.length === 0" class="empty">暂无照片</view>

      <view class="grid">
        <view class="item" v-for="p in photos" :key="p.id">
          <image class="img" :src="p.path" mode="aspectFill" />
          <view class="time">{{ p.timeText }}</view>
          <view class="del" @tap.stop="remove(p.id)">删除</view>
        </view>
      </view>

      <view style="height: 140rpx;"></view>
    </scroll-view>

    <view class="bottom-exit" @tap="goBack">
      <text class="exit-text">退出</text>
    </view>
  </view>
</template>

<script>
function pad2(n) { return n < 10 ? "0"+n : ""+n; }
function fmtTime(ts) {
  const d = new Date(ts);
  return `${d.getFullYear()}-${pad2(d.getMonth()+1)}-${pad2(d.getDate())} ${pad2(d.getHours())}:${pad2(d.getMinutes())}:${pad2(d.getSeconds())}`;
}

export default {
  data() {
    return {
      personId: "",
      name: "",
      gender: "",
      phone: "",
      photos: []
    };
  },

  computed: {
    headerTitle() {
      const n = this.name || "";
      const g = this.gender || "";
      const p = this.phone || "";
      return `${n} ${g} ${p}`.trim();
    }
  },

  onLoad(q) {
    this.personId = q.personId ? String(q.personId) : "";
    this.name = q.name ? decodeURIComponent(q.name) : "";
    this.gender = q.gender ? decodeURIComponent(q.gender) : "";
    this.phone = q.phone ? decodeURIComponent(q.phone) : "";
  },

  onShow() {
    this.loadPhotos();
  },

  methods: {
    key() {
      return `person_photos_${this.personId}`;
    },

    loadPhotos() {
      let arr = [];
      try {
        const v = uni.getStorageSync(this.key());
        if (Array.isArray(v)) arr = v;
      } catch (e) {}

      // 兜底：补齐 timeText
      arr = arr.map(x => ({
        ...x,
        timeText: x.timeText || fmtTime(x.ts || Date.now())
      }));

      this.photos = arr;
    },

    remove(id) {
      const arr = this.photos.filter(x => x.id !== id);
      this.photos = arr;
      try {
        uni.setStorageSync(this.key(), arr);
      } catch (e) {}
    },

    goBack() {
      uni.navigateBack();
    },

    onShare() {
      uni.showToast({ title: "分享（待接入）", icon: "none" });
    }
  }
};
</script>

<style scoped>
.page { height: 100vh; background: #fff; display: flex; flex-direction: column; }
.topbar { height: 110rpx; background: #17b3a8; display: flex; align-items: center; padding: 0 20rpx; box-sizing: border-box; }
.back { width: 70rpx; color: #fff; font-size: 56rpx; line-height: 1; }
.title { flex: 1; text-align: center; color: #fff; font-size: 34rpx; font-weight: 800; }
.right { width: 160rpx; text-align: right; color: #fff; font-size: 28rpx; }

.section { padding: 22rpx 22rpx 0; }
.section-title { font-size: 32rpx; font-weight: 800; color: #111; }

.body { flex: 1; }
.empty { padding: 80rpx 0; text-align: center; color: #999; font-size: 30rpx; }

.grid { display: flex; flex-wrap: wrap; gap: 18rpx; padding: 22rpx; box-sizing: border-box; }
.item { width: calc(50% - 9rpx); height: 420rpx; position: relative; overflow: hidden; border-radius: 10rpx; background: #000; }
.img { width: 100%; height: 100%; }
.time { position: absolute; left: 10rpx; bottom: 10rpx; color: #fff; font-size: 22rpx; background: rgba(0,0,0,.45); padding: 6rpx 10rpx; border-radius: 8rpx; }
.del { position: absolute; right: 10rpx; top: 10rpx; background: rgba(65,120,255,.85); color: #fff; font-size: 26rpx; padding: 10rpx 18rpx; border-radius: 10rpx; }

.bottom-exit { height: 110rpx; display: flex; align-items: center; justify-content: center; border-top: 1rpx solid #eee; }
.exit-text { color: #17b3a8; font-size: 34rpx; font-weight: 900; }
</style>
