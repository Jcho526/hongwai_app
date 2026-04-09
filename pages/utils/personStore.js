// utils/personStore.js
// 本地人员档案存储（uni.setStorageSync 持久化）

const STORE_KEY = "person_list";

function safeGetList() {
  try {
    const raw = uni.getStorageSync(STORE_KEY);
    if (!raw) return [];
    if (Array.isArray(raw)) return raw;
    if (typeof raw === "string") {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    }
    return [];
  } catch (e) {
    return [];
  }
}

function safeSetList(list) {
  try {
    uni.setStorageSync(STORE_KEY, list);
  } catch (e) {
    uni.setStorageSync(STORE_KEY, JSON.stringify(list || []));
  }
}

// 取全部人员（按 createdAt 倒序）
export function getAllPersons() {
  const list = safeGetList();
  return list
    .filter((x) => x && x.id)
    .sort((a, b) => Number(b.createdAt || 0) - Number(a.createdAt || 0));
}

// 新增一个人员（插入到最前面）
export function addOnePerson(person) {
  const list = getAllPersons();
  list.unshift(person);
  safeSetList(list);
  return list;
}

// 删除（可选）
export function deletePersonById(id) {
  const list = getAllPersons().filter((p) => String(p.id) !== String(id));
  safeSetList(list);
  return list;
}

// 清空（可选）
export function clearPersons() {
  safeSetList([]);
}

// 生成 10 位数字 ID（尽量避免重复）
export function gen10Id() {
  const existed = new Set(getAllPersons().map((p) => String(p.id)));
  for (let i = 0; i < 30; i++) {
    const id = String(Math.floor(1000000000 + Math.random() * 9000000000));
    if (!existed.has(id)) return id;
  }
  return String(Date.now()).slice(-10);
}
