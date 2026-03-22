# 🛒 FreshMart Grocery Delivery API

🚀 FastAPI-based Grocery Delivery API with cart system, order workflow, filtering, sorting, and pagination. Built as a complete backend project.

---

## 📌 Project Overview

A fully functional **FastAPI-based Grocery Delivery System** built as a final project.
This API allows users to browse grocery items, manage a cart, place orders, and handle deliveries with advanced features.

---

## 🚀 Features

### 📦 Items Management

* View all grocery items
* Get item by ID
* Add new items
* Update item details
* Delete items (with validation)

### 🛍 Cart System

* Add items to cart
* Merge quantities automatically
* Remove items
* View cart with subtotal & grand total
* Checkout system

### 📦 Orders System

* Create orders
* Bulk order discount (8%)
* Delivery slot charges
* View all orders

### 🔍 Advanced Features

* Search items by keyword
* Filter items (category, price, stock, unit)
* Sort items (price, name, category)
* Pagination for items & orders
* Combined browsing endpoint

### ⚙️ Helper Functions

* `find_item()` for item lookup
* `calculate_order_total()` for pricing logic
* Dedicated test endpoint: `/helpers/test`

---

## 🧪 API Endpoints Overview

### 🟢 Basic

* `GET /` → Welcome message
* `GET /items`
* `GET /items/{item_id}`
* `GET /items/summary`

### 🔵 Orders

* `POST /orders`
* `GET /orders`
* `GET /orders/search`
* `GET /orders/sort`
* `GET /orders/page`

### 🟡 Items Advanced

* `GET /items/filter`
* `GET /items/search`
* `GET /items/sort`
* `GET /items/page`
* `GET /items/browse`

### 🟠 Cart

* `POST /cart/add`
* `GET /cart`
* `DELETE /cart/{item_id}`
* `POST /cart/checkout`

### 🟣 Helpers

* `GET /helpers/test`

---

## ⚙️ Tech Stack

* ⚡ FastAPI
* 🐍 Python
* 📦 Pydantic (Data Validation)
* 🚀 Uvicorn (ASGI Server)

---

## ▶️ How to Run the Project

### 1. Clone Repository

```bash
git clone https://github.com/your-username/fastapi-grocery-delivery-app.git
cd fastapi-grocery-delivery-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
uvicorn main:app --reload
```

### 4. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📸 Screenshots

All API endpoints are tested using Swagger UI.
Screenshots are available in the `/screenshots` folder.

---

## 💡 Key Highlights

* Clean and modular code structure
* Proper use of Pydantic validation
* Real-world cart & checkout workflow
* Fully implemented search, sort, pagination
* Error handling with proper status codes
* Follows FastAPI best practices

---

## 🧠 Learning Outcomes

* Built REST APIs using FastAPI
* Implemented CRUD operations
* Designed multi-step workflows
* Applied filtering, sorting, pagination
* Improved debugging and API design skills

---

## 🏷️ Tags / Topics

fastapi, python, rest-api, backend, grocery-app, api-development, pydantic, uvicorn, crud, pagination, shopping-cart, order-management

---

## 👩‍💻 Author

**Divya Patel**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
