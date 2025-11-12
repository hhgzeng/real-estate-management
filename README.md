# 房地产管理系统

这是一个房产销售管理系统，旨在帮助房地产公司高效管理房产信息、销售订单和客户关系。系统分为前端和后端两部分，前端使用Vue.js构建，后端使用Django框架开发。

## 技术栈

### 后端

- Python 3.13
- Django 4.2.17
- Django CORS Headers
- PyMySQL
- QRCode

### 前端

- Vue.js 3
- Vue Router
- Node.js
- npm/yarn

## 系统功能

- 多角色用户系统（管理员、销售人员、客户）
- 房产信息管理
- 销售订单处理
- 客户管理
- 账户管理

## 安装说明

### 后端安装

1. 进入后端目录：

```bash
cd real_estate_backend
```

2. 创建虚拟环境并激活：

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# 或
.\env\Scripts\activate  # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 运行数据库迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

5. 启动后端服务器：

```bash
python manage.py runserver
```

### 前端安装

1. 进入前端目录：

```bash
cd real-estate-frontend
```

2. 安装依赖：

```bash
npm install
# 或
yarn install
```

3. 启动开发服务器：

```bash
npm run serve
# 或
yarn serve
```

## 使用说明

### 用户角色

- 管理员：系统管理、用户管理、数据统计
- 销售人员：房产管理、客户跟进、订单处理
- 客户：浏览房产、预约看房、查看订单

### 主要功能模块

1. 首页：展示热门房产和系统公告
2. 用户中心：个人信息管理
3. 房产管理：房产信息的CRUD操作
4. 订单管理：订单处理和跟踪
