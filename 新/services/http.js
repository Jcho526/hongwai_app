const BASE_URL = "http://127.0.0.1:3000";
const USE_MOCK = false;
const TOKEN_KEY = "auth_token";

export function getAuthToken() {
  return String(uni.getStorageSync(TOKEN_KEY) || "");
}

export function setAuthToken(token) {
  uni.setStorageSync(TOKEN_KEY, token || "");
}

export function clearAuthToken() {
  uni.removeStorageSync(TOKEN_KEY);
}

export function httpRequest({ url, method = "GET", data = {}, header = {} }) {
  return new Promise((resolve, reject) => {
    if (USE_MOCK) {
      resolve({ code: 0, message: "ok", data: null });
      return;
    }

    const token = getAuthToken();
    const finalHeader = {
      ...header
    };
    if (token) {
      finalHeader.Authorization = `Bearer ${token}`;
    }

    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: finalHeader,
      success: (res) => {
        const body = res && res.data ? res.data : {};
        if (res.statusCode === 401) {
          clearAuthToken();
          uni.reLaunch({ url: "/pages/index/index" });
          reject(new Error(body.message || "登录已过期"));
          return;
        }

        if (typeof body.code === "number" && body.code !== 0) {
          reject(new Error(body.message || "请求失败"));
          return;
        }
        resolve(body);
      },
      fail: (err) => {
        const msg = (err && (err.errMsg || err.message)) || "网络请求失败";
        reject(new Error(msg));
      }
    });
  });
}

export function isMockEnabled() {
  return USE_MOCK;
}
