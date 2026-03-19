<template>
  <view class="page">
    <!-- 顶部栏 -->
    <view class="topbar">
      <view class="topbar-left" @tap="onAddPerson">
        <image src="/static/icons/addperson.png" class="top-icon" />
        <text class="top-txt">新建人员档案</text>
      </view>

      <view class="topbar-mid">
        <text class="top-title">客户管理</text>
      </view>

      <view class="topbar-right" @tap="goToMain">
        <image src="/static/icons/out.png" class="top-icon" />
        <text class="top-txt">退出</text>
      </view>
    </view>

    <!-- 搜索条（联想 + 防抖） -->
    <view class="search-row">
      <view class="tabs">
        <view class="tab-item" :class="{ active: activeTab === 'name' }" @tap="switchTab('name')">
          <text>姓名</text>
          <view v-if="activeTab === 'name'" class="tab-line"></view>
        </view>

        <view class="tab-item" :class="{ active: activeTab === 'phone' }" @tap="switchTab('phone')">
          <text>手机号</text>
          <view v-if="activeTab === 'phone'" class="tab-line"></view>
        </view>
      </view>

      <view class="search-wrap">
        <view class="search-box">
          <input
            class="search-input"
            v-model="keyword"
            placeholder="请输入搜索关键"
            placeholder-class="ph"
            confirm-type="search"
            @input="onKeywordInput"
            @focus="onKeywordFocus"
            @blur="onKeywordBlur"
            @confirm="onSearchNow"
          />
          <view class="search-btn" @tap="onSearchNow">
            <image src="/static/icons/search.png" class="search-icon" />
          </view>
        </view>

        <!-- 联想下拉 -->
        <view v-if="showSuggest && suggestions.length > 0" class="suggest-panel">
          <view
            v-for="(s, idx) in suggestions"
            :key="idx"
            class="suggest-item"
            @mousedown.prevent
            @touchstart.prevent
            @tap="pickSuggestion(s)"
          >
            <text class="suggest-main">{{ s.main }}</text>
            <text v-if="s.sub" class="suggest-sub">{{ s.sub }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 内容区 -->
    <scroll-view class="content" scroll-y>
      <view v-if="pagedList.length === 0" class="empty">
        <text class="empty-txt">暂无人员数据</text>
      </view>

      <view
        v-for="item in pagedList"
        :key="item.id"
        class="person-card"
        @tap="onDetail(item)"
      >
        <!-- 左侧三行 -->
        <view class="card-left">
          <text class="line">ID:{{ item.id }}</text>
          <text class="line">姓名:{{ item.name }}</text>
          <text class="line">性别:{{ item.gender }}</text>
        </view>

        <!-- 右侧：四个圆形图标 + 编辑删除 + 箭头 -->
        <view class="card-right">
          <button class="act act-camera" @tap.stop="onCapture(item)">
            <image src="/static/icons/zhao.png" class="act-icon" mode="aspectFit" />
          </button>

          <button class="act act-vs" @tap.stop="onCompare(item)">
            <image src="/static/icons/vs2.png" class="act-icon" mode="aspectFit" />
          </button>

          <button class="act act-report" @tap.stop="onReport(item)">
            <image src="/static/icons/false.png" class="act-icon" mode="aspectFit" />
          </button>

          <button class="act act-diag" @tap.stop="onDiagnose(item)">
            <image src="/static/icons/zhen.png" class="act-icon" mode="aspectFit" />
          </button>

          <!-- ✅ 改动：编辑不跳转，打开弹窗 -->
          <view class="big-btn edit-btn" @tap.stop="onEdit(item)">编辑</view>

          <view class="big-btn del-btn" @tap.stop="onDelete(item)">删除</view>

          <text class="arrow">›</text>
        </view>
      </view>
    </scroll-view>

    <!-- 分页条 -->
    <view class="pager">
      <text class="pager-left">总数 {{ total }}</text>
      <text class="pager-mid">{{ page }}/{{ pageTotal }}</text>

      <view class="pager-right">
        <view class="pager-btn" @tap="prevPage">‹</view>
        <view class="pager-split"></view>
        <view class="pager-btn" @tap="nextPage">›</view>
      </view>
    </view>

    <!-- 底部 -->
    <view class="bottombar">
      <view class="bottom-item" @tap="onAddPerson">
        <image src="/static/icons/addperson.png" class="bottom-icon" />
        <text class="bottom-txt">新建人员档案</text>
      </view>

      <view class="bottom-split"></view>

      <view class="bottom-item" @tap="goToMain">
        <image src="/static/icons/out.png" class="bottom-icon" />
        <text class="bottom-txt">退出</text>
      </view>

      <view class="safe-pad"></view>
    </view>

    <!-- ✅ 新增：编辑弹窗（不跳转页面） -->
    <view v-if="showEdit" class="mask" @tap="closeEdit">
      <view class="edit-panel" @tap.stop>
        <view class="edit-header">
          <text class="edit-title">编辑人员信息</text>
          <text class="edit-close" @tap="closeEdit">×</text>
        </view>

        <scroll-view class="edit-body" scroll-y>
          <view class="form-row">
            <text class="form-label">姓名</text>
            <input class="form-input" v-model="editForm.name" placeholder="请输入姓名" />
          </view>

          <view class="form-row">
            <text class="form-label">性别</text>
            <view class="gender-row">
              <view class="gender-item" :class="{ gOn: editForm.gender === '男' }" @tap="editForm.gender='男'">男</view>
              <view class="gender-item" :class="{ gOn: editForm.gender === '女' }" @tap="editForm.gender='女'">女</view>
            </view>
          </view>

          <view class="form-row">
            <text class="form-label">年龄</text>
            <input class="form-input" v-model="editForm.age" type="number" placeholder="请输入年龄" />
          </view>

          <view class="form-row">
            <text class="form-label">手机号1</text>
            <input class="form-input" v-model="editForm.phone1" placeholder="请输入手机号1" />
          </view>

          <view class="form-row">
            <text class="form-label">手机号2</text>
            <input class="form-input" v-model="editForm.phone2" placeholder="请输入手机号2" />
          </view>

          <view class="form-row">
            <text class="form-label">手机号3</text>
            <input class="form-input" v-model="editForm.phone3" placeholder="请输入手机号3" />
          </view>

          <view class="form-row">
            <text class="form-label">亲属手机号</text>
            <input class="form-input" v-model="editForm.relativePhone" placeholder="请输入亲属手机号" />
          </view>

          <view class="form-row">
            <text class="form-label">身份证号</text>
            <input class="form-input" v-model="editForm.idCard" placeholder="请输入身份证号" />
          </view>
        </scroll-view>

        <view class="edit-footer">
          <view class="btn ghost" @tap="closeEdit">取消</view>
          <view class="btn primary" @tap="saveEdit">保存</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getAllPersons } from "../utils/personStore.js";

export default {
  name: "person",
  data() {
    return {
      STORAGE_KEY: "persons",
      DELETED_KEY: "persons_deleted_ids",
      activeTab: "name",
      keyword: "",
      total: 0,
      page: 1,
      pageTotal: 1,
      pageSize: 20,
      allList: [],
      filteredList: [],

      showSuggest: false,
      suggestions: [],

      debounceMs: 300,
      debounceTimer: null,
      blurTimer: null,

      // ✅ 新增：编辑弹窗数据
      showEdit: false,
      editForm: {
        id: "",
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
  computed: {
    pagedList() {
      const start = (this.page - 1) * this.pageSize;
      return this.filteredList.slice(start, start + this.pageSize);
    }
  },
  watch: {
    activeTab() {
      this.page = 1;
      this.refreshSuggest();
      this.applyFilter();
    }
  },
  onShow() {
    this.reloadList();
  },
  beforeDestroy() {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    if (this.blurTimer) clearTimeout(this.blurTimer);
  },
  methods: {
    goToMain() {
      const MAIN_URL = "/pages/main/main"; // ⚠️ 不同就改这里
      uni.reLaunch({ url: MAIN_URL });
    },

    onAddPerson() {
      uni.navigateTo({ url: "/pages/person/addPerson" });
    },

    switchTab(tab) {
      this.activeTab = tab;
    },

    onKeywordInput() {
      this.showSuggest = true;
      this.refreshSuggest();

      if (this.debounceTimer) clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.page = 1;
        this.applyFilter();
      }, this.debounceMs);
    },

    onKeywordFocus() {
      this.showSuggest = true;
      this.refreshSuggest();
    },

    onKeywordBlur() {
      if (this.blurTimer) clearTimeout(this.blurTimer);
      this.blurTimer = setTimeout(() => {
        this.showSuggest = false;
      }, 180);
    },

    onSearchNow() {
      if (this.debounceTimer) clearTimeout(this.debounceTimer);
      this.page = 1;
      this.applyFilter();
      this.refreshSuggest();
      this.showSuggest = false;
    },

    pickSuggestion(s) {
      this.keyword = s.value;
      this.onSearchNow();
    },

    refreshSuggest() {
      const kw = (this.keyword || "").trim();
      if (!kw) {
        this.suggestions = [];
        return;
      }

      const list = Array.isArray(this.allList) ? this.allList : [];
      const out = [];
      const seen = new Set();

      if (this.activeTab === "name") {
        for (const p of list) {
          const name = String(p.name || "");
          if (!name) continue;
          if (!name.includes(kw)) continue;
          if (seen.has(name)) continue;

          seen.add(name);
          out.push({
            main: name,
            sub: p.phone1 ? `手机号1：${p.phone1}` : "",
            value: name
          });
          if (out.length >= 6) break;
        }
      } else {
        for (const p of list) {
          const phones = [p.phone1, p.phone2, p.phone3, p.relativePhone]
            .map((x) => String(x || ""))
            .filter(Boolean);

          const hit = phones.find((ph) => ph.includes(kw));
          if (!hit) continue;

          const key = `${hit}-${p.id}`;
          if (seen.has(key)) continue;

          seen.add(key);
          out.push({
            main: hit,
            sub: p.name ? `姓名：${p.name}` : "",
            value: hit
          });
          if (out.length >= 6) break;
        }
      }

      this.suggestions = out;
    },

    reloadList() {
      // 1) 读本地 persons（你删除时写入的）
      let cacheList = [];
      try {
        const cache = uni.getStorageSync(this.STORAGE_KEY);
        if (Array.isArray(cache)) cacheList = cache;
      } catch (e) {}
    
      // 2) 读 personStore（你新增很可能写到这里）
      const storeListRaw = getAllPersons();
      const storeList = Array.isArray(storeListRaw) ? storeListRaw : [];
    
      // 3) 读删除黑名单（防止删除后复活）
      let deletedIds = [];
      try {
        const del = uni.getStorageSync(this.DELETED_KEY);
        if (Array.isArray(del)) deletedIds = del;
      } catch (e) {}
      const delSet = new Set(deletedIds.map(String));
    
      // 4) 合并两份数据：以 id 为主键，优先用 cache（因为你编辑/删除会先落到 cache）
      const map = new Map();
      for (const p of storeList) {
        if (!p || p.id == null) continue;
        map.set(String(p.id), p);
      }
      for (const p of cacheList) {
        if (!p || p.id == null) continue;
        map.set(String(p.id), p); // cache 覆盖 store
      }
    
      // 5) 过滤掉已删除的 id
      let merged = Array.from(map.values()).filter(p => !delSet.has(String(p.id)));
    
      // 6) 你如果希望保持原有顺序，可以按 id 排一下（可删）
      merged.sort((a, b) => String(b.id).localeCompare(String(a.id)));
    
      // 7) 写回 persons，让后续统一
      try {
        uni.setStorageSync(this.STORAGE_KEY, merged);
      } catch (e) {}
    
      this.allList = merged;
      this.applyFilter();
      this.refreshSuggest();
    },

    applyFilter() {
      const kw = (this.keyword || "").trim();
      let list = Array.isArray(this.allList) ? [...this.allList] : [];

      if (kw) {
        if (this.activeTab === "name") {
          list = list.filter((p) => String(p.name || "").includes(kw));
        } else {
          list = list.filter((p) => {
            const phones = [p.phone1, p.phone2, p.phone3, p.relativePhone];
            return phones.some((x) => String(x || "").includes(kw));
          });
        }
      }

      this.filteredList = list;
      this.total = list.length;
      this.pageTotal = Math.max(1, Math.ceil(this.total / this.pageSize));
      if (this.page > this.pageTotal) this.page = this.pageTotal;
    },

    onDelete(item) {
      uni.showModal({
        title: "删除人员",
        content: `确认删除【${item.name || ""}】吗？`,
        success: (res) => {
          if (!res.confirm) return;

          const id = item.id;
          const newAll = (Array.isArray(this.allList) ? this.allList : []).filter((p) => p.id !== id);

          try {
            uni.setStorageSync(this.STORAGE_KEY, newAll);
          } catch (e) {}

          this.allList = newAll;
          this.page = 1;
          this.applyFilter();
          this.refreshSuggest();

          uni.showToast({ title: "已删除", icon: "none" });
		  // ✅ 记录删除黑名单（防止退出回来复活）
		  try {
		    const del = uni.getStorageSync(this.DELETED_KEY);
		    const arr = Array.isArray(del) ? del : [];
		    const sid = String(id);
		    if (!arr.includes(sid)) arr.push(sid);
		    uni.setStorageSync(this.DELETED_KEY, arr);
		  } catch (e) {}

        }
      });
    },

    // ✅ 改动：编辑不跳转页面，改为弹窗回填
    onEdit(item) {
      this.editForm = {
        id: item.id,
        name: item.name || "",
        gender: item.gender || "男",
        age: item.age || "",
        phone1: item.phone1 || "",
        phone2: item.phone2 || "",
        phone3: item.phone3 || "",
        relativePhone: item.relativePhone || "",
        idCard: item.idCard || ""
      };
      this.showEdit = true;
    },

    closeEdit() {
      this.showEdit = false;
    },

    saveEdit() {
      const name = (this.editForm.name || "").trim();
      if (!name) {
        uni.showToast({ title: "请输入姓名", icon: "none" });
        return;
      }

      const id = this.editForm.id;
      const idx = (Array.isArray(this.allList) ? this.allList : []).findIndex(p => p.id === id);

      if (idx === -1) {
        uni.showToast({ title: "未找到该人员", icon: "none" });
        this.showEdit = false;
        return;
      }

      const old = this.allList[idx];
      const updated = {
        ...old,
        name: this.editForm.name,
        gender: this.editForm.gender,
        age: this.editForm.age,
        phone1: this.editForm.phone1,
        phone2: this.editForm.phone2,
        phone3: this.editForm.phone3,
        relativePhone: this.editForm.relativePhone,
        idCard: this.editForm.idCard
      };

      this.allList.splice(idx, 1, updated);

      try {
        uni.setStorageSync(this.STORAGE_KEY, this.allList);
      } catch (e) {}

      // 刷新筛选/联想/分页
      this.applyFilter();
      this.refreshSuggest();

      this.showEdit = false;
      uni.showToast({ title: "已保存", icon: "none" });
    },

    // ✅ 关键：拍照按钮进入“检查项目”页面
    onCapture(item) {
      uni.showToast({ title: "进入检查项目", icon: "none" });

      uni.navigateTo({
        url: `/pages/checkItems/checkItems?personId=${encodeURIComponent(item.id)}`
      });
    },

    onCompare(item) {
      uni.showToast({ title: `对比：${item.name}`, icon: "none" });
    },
    onReport(item) {
      uni.showToast({ title: `报告：${item.name}`, icon: "none" });
    },
    onDiagnose(item) {
      uni.showToast({ title: `诊断：${item.name}`, icon: "none" });
    },
    onDetail(item) {
      const url =
        `/pages/photoRecords/photoRecords?personId=${encodeURIComponent(item.id)}` +
        `&name=${encodeURIComponent(item.name || "")}` +
        `&gender=${encodeURIComponent(item.gender || "")}` +
        `&phone=${encodeURIComponent(item.phone1 || "")}`;
    
      uni.navigateTo({ url });
    },


    prevPage() {
      if (this.page <= 1) return;
      this.page--;
    },
    nextPage() {
      if (this.page >= this.pageTotal) return;
      this.page++;
    }
  }
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  padding-bottom: 110rpx;
}

/* 顶部 */
.topbar {
  height: 92rpx;
  display: flex;
  align-items: center;
  padding: 0 22rpx;
  box-sizing: border-box;
  background: #ffffff;
}
.topbar-left,
.topbar-right {
  width: 260rpx;
  display: flex;
  align-items: center;
}
.topbar-left { justify-content: flex-start; }
.topbar-right { justify-content: flex-end; }
.topbar-mid { flex: 1; display: flex; justify-content: center; align-items: center; }
.top-title { font-size: 30rpx; color: #22c1be; font-weight: 600; letter-spacing: 1rpx; }
.top-txt { font-size: 26rpx; color: #22c1be; }
.top-icon { width: 32rpx; height: 32rpx; margin-right: 10rpx; }

/* 搜索行 */
.search-row {
  height: 90rpx;
  display: flex;
  align-items: center;
  padding: 0 18rpx;
  box-sizing: border-box;
  background: #ffffff;
}
.tabs { width: 210rpx; display: flex; align-items: center; }
.tab-item {
  width: 92rpx;
  text-align: center;
  font-size: 26rpx;
  color: #8a8a8a;
  position: relative;
  padding-bottom: 10rpx;
}
.tab-item.active { color: #22c1be; font-weight: 600; }
.tab-line {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 0rpx;
  width: 52rpx;
  height: 6rpx;
  border-radius: 6rpx;
  background: #22c1be;
}

.search-wrap { flex: 1; position: relative; }
.search-box {
  height: 60rpx;
  background: #f5f7f7;
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  padding-left: 18rpx;
  box-sizing: border-box;
  border: 1rpx solid #e9eeee;
}
.search-input { flex: 1; height: 60rpx; font-size: 26rpx; color: #333; }
.ph { color: #b9b9b9; font-size: 26rpx; }
.search-btn {
  width: 60rpx;
  height: 60rpx;
  border-radius: 60rpx;
  background: #1e8fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.search-icon { width: 28rpx; height: 28rpx; }

/* 联想面板 */
.suggest-panel {
  position: absolute;
  left: 0;
  right: 0;
  top: 68rpx;
  background: #ffffff;
  border: 1rpx solid #e9eeee;
  border-radius: 14rpx;
  box-shadow: 0 10rpx 26rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;
  z-index: 999;
}
.suggest-item { padding: 18rpx; border-bottom: 1rpx solid #f2f2f2; }
.suggest-item:last-child { border-bottom: none; }
.suggest-main { font-size: 26rpx; color: #333; }
.suggest-sub { display: block; margin-top: 6rpx; font-size: 22rpx; color: #888; }

.content { flex: 1; background: #ffffff; }
.empty { padding: 80rpx 0; display: flex; align-items: center; justify-content: center; }
.empty-txt { color: #9a9a9a; font-size: 28rpx; }

/* 卡片 */
.person-card {
  margin: 14rpx 18rpx;
  padding: 20rpx 18rpx;
  background: #ffffff;
  border-radius: 12rpx;
  border: 1rpx solid #eeeeee;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 左侧 */
.card-left {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
  color: #333;
  flex: 1;
  min-width: 0;
}
.line { font-size: 28rpx; }

/* 右侧 */
.card-right {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex-shrink: 0;
}

/* 圆形按钮 */
.act {
  width: 72rpx;
  height: 72rpx;
  border-radius: 36rpx;
  display: flex;
  align-items: center;
  justify-content: center;

  border: none;
  padding: 0;
  margin: 0;
  background: transparent;
  line-height: 1;
}
.act::after { border: none; }
.act-icon { width: 40rpx; height: 40rpx; }

/* 颜色 */
.act-camera { background: #7acb78; }
.act-vs { background:#ffffff; border: 2rpx solid #132c78; }
.act-report { background: #ffffff; border: 2rpx solid #f4a23a; }
.act-diag   { background: #ffffff; border: 2rpx solid #7acb78; }

/* 编辑/删除 */
.big-btn {
  height: 72rpx;
  padding: 0 24rpx;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  font-weight: 700;
  color: #ffffff;
}
.edit-btn { background: #22c1be; }
.del-btn { background: #ff5b5b; }

/* 箭头 */
.arrow {
  font-size: 52rpx;
  color: #bdbdbd;
  margin-left: 6rpx;
  line-height: 1;
}

/* 分页 */
.pager {
  height: 84rpx;
  background: #f3f3f3;
  border-top: 1rpx solid #e6e6e6;
  display: flex;
  align-items: center;
  padding: 0 18rpx;
  box-sizing: border-box;
}
.pager-left { width: 200rpx; font-size: 24rpx; color: #6f6f6f; }
.pager-mid { flex: 1; text-align: center; font-size: 24rpx; color: #6f6f6f; }
.pager-right {
  width: 150rpx;
  height: 54rpx;
  background: #efefef;
  border: 1rpx solid #dddddd;
  border-radius: 6rpx;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.pager-btn {
  flex: 1;
  height: 54rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  color: #6f6f6f;
}
.pager-split { width: 1rpx; height: 54rpx; background: #dddddd; }

/* 底部 */
.bottombar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 110rpx;
  background: #ffffff;
  border-top: 1rpx solid #e6e6e6;
  display: flex;
  align-items: center;
  z-index: 999;
}
.bottom-item { flex: 1; height: 110rpx; display: flex; align-items: center; justify-content: center; }
.bottom-icon { width: 34rpx; height: 34rpx; margin-right: 10rpx; }
.bottom-txt { font-size: 28rpx; color: #22c1be; font-weight: 600; }
.bottom-split { width: 1rpx; height: 70rpx; background: #e6e6e6; }
.safe-pad {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: env(safe-area-inset-bottom);
  background: #ffffff;
}

/* ✅ 新增：编辑弹窗样式（不影响你原页面） */
.mask{
  position: fixed;
  left:0; right:0; top:0; bottom:0;
  background: rgba(0,0,0,.45);
  z-index: 9999;
  display:flex;
  align-items:center;
  justify-content:center;
  padding: 24rpx;
  box-sizing: border-box;
}
.edit-panel{
  width: 680rpx;
  max-height: 82vh;
  background:#fff;
  border-radius: 16rpx;
  overflow: hidden;
  display:flex;
  flex-direction: column;
}
.edit-header{
  height: 92rpx;
  background: #22c1be;
  display:flex;
  align-items:center;
  padding: 0 22rpx;
  box-sizing: border-box;
}
.edit-title{ flex:1; color:#fff; font-size: 32rpx; font-weight: 700; }
.edit-close{ color:#fff; font-size: 44rpx; line-height: 1; padding: 10rpx; }

.edit-body{
  flex: 1;
  padding: 18rpx 22rpx;
  box-sizing: border-box;
}
.form-row{ margin-bottom: 18rpx; }
.form-label{ display:block; color:#333; font-size: 26rpx; margin-bottom: 10rpx; }
.form-input{
  height: 70rpx;
  background: #f2f4f4;
  border-radius: 10rpx;
  padding: 0 16rpx;
  box-sizing: border-box;
  font-size: 28rpx;
  color: #111;
}
.gender-row{ display:flex; gap: 18rpx; }
.gender-item{
  flex: 1;
  height: 70rpx;
  border-radius: 10rpx;
  background: #f2f4f4;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 28rpx;
  color:#555;
  font-weight: 700;
}
.gender-item.gOn{
  background: #22c1be;
  color:#fff;
}
.edit-footer{
  height: 96rpx;
  display:flex;
  gap: 18rpx;
  padding: 16rpx 22rpx;
  box-sizing: border-box;
  border-top: 1rpx solid #eee;
}
.btn{
  flex:1;
  border-radius: 12rpx;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 30rpx;
  font-weight: 800;
}
.btn.ghost{
  background:#f2f4f4;
  color:#333;
}
.btn.primary{
  background:#22c1be;
  color:#fff;
}
</style>
