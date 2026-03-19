<template>
  <view class="container">
    <!-- 顶部栏 -->
    <view class="header">
      <!-- 左：返回 -->
      <view class="header-left" @click="goBack">
        <image src="/static/icons/back.png" class="icon" />
      </view>

      <!-- 中：标题 -->
      <view class="header-title">
        <text class="title">增加人员</text>
      </view>

      <!-- 右：退出（行为 = 返回） -->
      <view class="header-right" @click="goBack">
        <text class="exit-text">退出</text>
      </view>
    </view>

    <!-- 表单 -->
    <view class="form-container">
      <view class="form-item">
        <text class="label">*</text>
        <text class="label-text">姓名：</text>
        <input v-model="formData.name" placeholder="请输入姓名" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label">*</text>
        <text class="label-text">性别：</text>
        <view class="radio-group">
          <view class="radio-item" @click="selectGender('男')">
            <image
              :src="formData.gender === '男' ? '/static/icons/check.png' : '/static/icons/radio.png'"
              class="radio-icon"
            />
            <text>男</text>
          </view>
          <view class="radio-item" @click="selectGender('女')">
            <image
              :src="formData.gender === '女' ? '/static/icons/check.png' : '/static/icons/radio.png'"
              class="radio-icon"
            />
            <text>女</text>
          </view>
        </view>
      </view>

      <view class="form-item">
        <text class="label">*</text>
        <text class="label-text">年龄：</text>
        <input v-model="formData.age" type="number" placeholder="请输入年龄" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label">*</text>
        <text class="label-text">手机号1：</text>
        <input v-model="formData.phone1" placeholder="请输入手机号" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label-text">手机号2：</text>
        <input v-model="formData.phone2" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label-text">手机号3：</text>
        <input v-model="formData.phone3" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label-text">亲属手机号：</text>
        <input v-model="formData.relativePhone" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label-text">身份证号：</text>
        <input v-model="formData.idCard" class="input-box" />
      </view>

      <view class="form-item">
        <text class="label-text">扫码添加人员：</text>
        <view class="qrcode-box"></view>
      </view>
    </view>

    <!-- 底部按钮 -->
    <view class="button-group">
      <button class="btn" @click="savePerson">保存</button>
      <button class="btn" @click="resetForm">再次新建人员</button>
      <button class="btn" @click="capture">采图</button>
      <button class="btn" @click="goBack">退出</button>
    </view>
  </view>
</template>

<script>
import { addOnePerson, gen10Id } from "../utils/personStore.js";

export default {
  data() {
    return {
      formData: {
        name: "",
        gender: "男",
        age: "",
        phone1: "",
        phone2: "",
        phone3: "",
        relativePhone: "",
        idCard: ""
      }
    };
  },
  methods: {
    // ✅ 返回（左上角 & 退出统一）
    goBack() {
      uni.navigateBack();
    },

    selectGender(gender) {
      this.formData.gender = gender;
    },

    savePerson() {
      if (!this.formData.name) {
        return uni.showToast({ title: "请输入姓名", icon: "none" });
      }

      const person = {
        id: gen10Id(),
        ...this.formData,
        age: Number(this.formData.age),
        createdAt: Date.now()
      };

      addOnePerson(person);
      uni.showToast({ title: "保存成功", icon: "success" });

      setTimeout(() => {
        uni.navigateBack();
      }, 300);
    },

    resetForm() {
      this.formData = {
        name: "",
        gender: "男",
        age: "",
        phone1: "",
        phone2: "",
        phone3: "",
        relativePhone: "",
        idCard: ""
      };
    },

    capture() {
      uni.showToast({ title: "采图（待接入）", icon: "none" });
    }
  }
};
</script>

<style scoped>
.container {
  background: #f5f5f5;
  min-height: 100vh;
}

/* 顶部栏 */
.header {
  height: 90rpx;
  background: #00c4b8;
  display: flex;
  align-items: center;
  padding: 0 20rpx;
  color: #fff;
}

.header-left,
.header-right {
  width: 120rpx;
  display: flex;
  align-items: center;
}

.header-right {
  justify-content: flex-end;
}

.header-title {
  flex: 1;
  text-align: center;
}

.icon {
  width: 40rpx;
  height: 40rpx;
}

.exit-text {
  font-size: 30rpx;
}

.title {
  font-size: 34rpx;
  font-weight: bold;
}

/* 表单 */
.form-container {
  margin: 20rpx;
  background: #fff;
  border-radius: 10rpx;
  padding: 20rpx;
}

.form-item {
  margin-bottom: 20rpx;
}

.input-box {
  background: #e6f7ff;
  height: 80rpx;
  border-radius: 10rpx;
  padding: 0 20rpx;
}

.radio-group {
  display: flex;
  gap: 40rpx;
}

.radio-icon {
  width: 30rpx;
  height: 30rpx;
}

/* 底部按钮 */
.button-group {
  display: flex;
  gap: 20rpx;
  padding: 20rpx;
}

.btn {
  flex: 1;
  background: #00c4b8;
  color: #fff;
  border-radius: 20rpx;
}
</style>
