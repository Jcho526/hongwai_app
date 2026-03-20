import { httpRequest, isMockEnabled } from "./http";

const PERSONS_KEY = "persons_mock_backend";

function safeGetPersons() {
  try {
    const raw = uni.getStorageSync(PERSONS_KEY);
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

function safeSetPersons(list) {
  try {
    uni.setStorageSync(PERSONS_KEY, list);
  } catch (e) {
    uni.setStorageSync(PERSONS_KEY, JSON.stringify(list || []));
  }
}

function normalizePerson(payload = {}) {
  return {
    id: payload.id,
    name: String(payload.name || "").trim(),
    gender: payload.gender || "男",
    age: Number(payload.age || 0),
    phone1: String(payload.phone1 || "").trim(),
    phone2: String(payload.phone2 || "").trim(),
    phone3: String(payload.phone3 || "").trim(),
    relativePhone: String(payload.relativePhone || "").trim(),
    idCard: String(payload.idCard || "").trim(),
    createdAt: Number(payload.createdAt || Date.now()),
    updatedAt: Date.now()
  };
}

function genPersonId() {
  return `${Date.now()}${Math.floor(1000 + Math.random() * 9000)}`;
}

function filterPersons(list, { keyword = "", searchType = "name" } = {}) {
  const kw = String(keyword || "").trim();
  if (!kw) return list;

  if (searchType === "phone") {
    return list.filter((p) => {
      const phones = [p.phone1, p.phone2, p.phone3, p.relativePhone];
      return phones.some((x) => String(x || "").includes(kw));
    });
  }

  return list.filter((p) => String(p.name || "").includes(kw));
}

function pagePersons(list, { page = 1, pageSize = 20 } = {}) {
  const currentPage = Math.max(1, Number(page || 1));
  const currentSize = Math.max(1, Number(pageSize || 20));
  const total = list.length;
  const start = (currentPage - 1) * currentSize;
  const data = list.slice(start, start + currentSize);

  return {
    list: data,
    total,
    page: currentPage,
    pageSize: currentSize
  };
}

export async function listPersons(params = {}) {
  if (isMockEnabled()) {
    const all = safeGetPersons().sort((a, b) => Number(b.createdAt || 0) - Number(a.createdAt || 0));
    const filtered = filterPersons(all, params);
    return pagePersons(filtered, params);
  }

  const res = await httpRequest({
    url: "/api/persons",
    method: "GET",
    data: params
  });

  return {
    list: res?.data?.list || [],
    total: Number(res?.data?.total || 0),
    page: Number(res?.data?.page || params.page || 1),
    pageSize: Number(res?.data?.pageSize || params.pageSize || 20)
  };
}

export async function createPerson(payload) {
  if (isMockEnabled()) {
    const list = safeGetPersons();
    const person = normalizePerson({ ...payload, id: genPersonId() });
    list.unshift(person);
    safeSetPersons(list);
    return person;
  }

  const res = await httpRequest({
    url: "/api/persons",
    method: "POST",
    data: payload
  });
  return res?.data;
}

export async function updatePerson(id, payload) {
  if (isMockEnabled()) {
    const list = safeGetPersons();
    const index = list.findIndex((p) => String(p.id) === String(id));
    if (index < 0) throw new Error("人员不存在");

    const merged = normalizePerson({
      ...list[index],
      ...payload,
      id: list[index].id,
      createdAt: list[index].createdAt
    });

    list.splice(index, 1, merged);
    safeSetPersons(list);
    return merged;
  }

  const res = await httpRequest({
    url: `/api/persons/${encodeURIComponent(id)}`,
    method: "PUT",
    data: payload
  });
  return res?.data;
}

export async function deletePerson(id) {
  if (isMockEnabled()) {
    const list = safeGetPersons().filter((p) => String(p.id) !== String(id));
    safeSetPersons(list);
    return true;
  }

  await httpRequest({
    url: `/api/persons/${encodeURIComponent(id)}`,
    method: "DELETE"
  });
  return true;
}
