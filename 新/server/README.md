# hongwai 后端（Node.js + Express + MySQL）

## 1. 功能说明

- 账号密码登录（密码加密存储）
- JWT 鉴权
- 人员档案 CRUD（增删改查）
- **按账号隔离数据**（`persons.user_id`）
- 系统设置保存/读取（`system_settings.user_id` 唯一）

> 这保证了“每个登录账号只能看到自己的人员档案和系统设置”。

---

## 2. 初始化步骤

### 2.1 安装依赖

```bash
cd c:\Users\x1526\Desktop\新\新\server
npm install
```

### 2.2 配置环境变量

复制 `.env.example` 为 `.env`，并修改数据库账号密码：

```env
PORT=3000
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=hongwai
JWT_SECRET=replace_with_your_jwt_secret
JWT_EXPIRES_IN=7d
```

### 2.3 初始化数据库

执行：`sql/init.sql`

---

## 3. 启动服务

```bash
cd c:\Users\x1526\Desktop\新\新\server
npm run dev
```

健康检查：

`GET http://127.0.0.1:3000/api/health`

---

## 4. 首次创建账号

项目里已提供注册接口：

`POST /api/auth/register`

请求体示例：

```json
{
  "username": "admin",
  "password": "123456",
  "nickname": "管理员"
}
```

然后使用该账号在前端登录即可。

---

## 5. 核心接口

### 鉴权

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`
- `POST /api/auth/deactivate`

### 人员档案（需登录）

- `GET /api/persons?page=1&pageSize=20&keyword=&searchType=name`
- `POST /api/persons`
- `PUT /api/persons/:id`
- `DELETE /api/persons/:id`

### 系统设置（需登录）

- `GET /api/system/settings`
- `POST /api/system/settings`
- `GET /api/system/version/check`

---

## 6. 前端联调

前端文件：`新/services/http.js`

- `USE_MOCK = false`
- `BASE_URL = "http://127.0.0.1:3000"`

真机调试时请改成你电脑局域网 IP，例如：

`http://192.168.1.100:3000`
