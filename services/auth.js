import { httpRequest, setAuthToken, clearAuthToken } from "./http";

const USER_KEY = "auth_user";

export async function loginByPassword({ username, password }) {
  const res = await httpRequest({
    url: "/api/auth/login",
    method: "POST",
    data: { username, password }
  });

  const token = res?.data?.token || "";
  const user = res?.data?.user || null;

  if (token) {
    setAuthToken(token);
  }
  if (user) {
    uni.setStorageSync(USER_KEY, user);
  }

  return { token, user };
}

export async function logout() {
  try {
    await httpRequest({
      url: "/api/auth/logout",
      method: "POST"
    });
  } finally {
    clearAuthToken();
    uni.removeStorageSync(USER_KEY);
  }
}

export function getCurrentUser() {
  return uni.getStorageSync(USER_KEY) || null;
}
