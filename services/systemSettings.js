import { httpRequest, isMockEnabled } from "./http";

const SETTINGS_KEY = "system_settings_mock";

const defaultSettings = {
  serialNo: "1009Z0YGVM28",
  deviceModel: "IR-TD-206",
  version: "v1.0.74",
  reportType: "无",
  expireTime: "无",
  reportTotal: 15,
  reportXiYi: 9,
  reportZhongYi: 3,
  reportMianZhen: 3,
  reportDanXiang: 2,
  imageSavePath: "qa/qa_thermal",
  reversePortraitImage: false,
  reportCountHint: 20,
  reportDayHint: 10,
  screenCaptureEnable: false,
  typecCameraEnable: false,
  qrCodeUrl: ""
};

function getMockSettings() {
  try {
    const raw = uni.getStorageSync(SETTINGS_KEY);
    if (!raw) return { ...defaultSettings };
    if (typeof raw === "string") {
      const parsed = JSON.parse(raw);
      return { ...defaultSettings, ...parsed };
    }
    return { ...defaultSettings, ...raw };
  } catch (e) {
    return { ...defaultSettings };
  }
}

function setMockSettings(settings) {
  const next = { ...defaultSettings, ...settings };
  try {
    uni.setStorageSync(SETTINGS_KEY, next);
  } catch (e) {
    uni.setStorageSync(SETTINGS_KEY, JSON.stringify(next));
  }
  return next;
}

export async function getSystemSettings() {
  if (isMockEnabled()) {
    return getMockSettings();
  }

  const res = await httpRequest({
    url: "/api/system/settings",
    method: "GET"
  });
  return res.data || defaultSettings;
}

export async function saveSystemSettings(payload) {
  if (isMockEnabled()) {
    return setMockSettings(payload);
  }

  const res = await httpRequest({
    url: "/api/system/settings",
    method: "POST",
    data: payload
  });
  return res.data || payload;
}

export async function logoutRequest() {
  if (isMockEnabled()) return true;
  await httpRequest({
    url: "/api/auth/logout",
    method: "POST"
  });
  return true;
}

export async function deactivateAccountRequest() {
  if (isMockEnabled()) return true;
  await httpRequest({
    url: "/api/auth/deactivate",
    method: "POST"
  });
  return true;
}

export async function checkVersionRequest() {
  if (isMockEnabled()) {
    return {
      hasNewVersion: false,
      latestVersion: defaultSettings.version,
      downloadUrl: ""
    };
  }

  const res = await httpRequest({
    url: "/api/system/version/check",
    method: "GET"
  });
  return res.data || { hasNewVersion: false };
}
