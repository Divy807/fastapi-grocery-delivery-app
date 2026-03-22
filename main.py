from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
# Sample grocery items
items = [
    {"id": 1, "name": "Tomato", "price": 30, "unit": "kg", "category": "Vegetable", "in_stock": True},
    {"id": 2, "name": "Milk", "price": 50, "unit": "litre", "category": "Dairy", "in_stock": True},
    {"id": 3, "name": "Rice", "price": 60, "unit": "kg", "category": "Grain", "in_stock": True},
    {"id": 4, "name": "Apple", "price": 120, "unit": "kg", "category": "Fruit", "in_stock": False},
    {"id": 5, "name": "Eggs", "price": 70, "unit": "dozen", "category": "Dairy", "in_stock": True},
    {"id": 6, "name": "Potato", "price": 25, "unit": "kg", "category": "Vegetable", "in_stock": True},
]
orders = []
order_counter = 1
cart = []

# PYDANTIC MODELS
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)
    delivery_address: str = Field(..., min_length=10)
    delivery_slot: str = "Morning"
    bulk_order: bool = False
class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)
    delivery_slot: str = "Morning"
class NewItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    unit: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    in_stock: bool = True

# HELPER FUNCTIONS
def find_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return None
def calculate_order_total(price, quantity, delivery_slot, bulk_order=False):
    original_total = price * quantity
    discount = 0
    # Bulk discount
    if bulk_order and quantity >= 10:
        discount = original_total * 0.08
    discounted_total = original_total - discount
    # Delivery charges
    if delivery_slot == "Morning":
        delivery_charge = 40
    elif delivery_slot == "Evening":
        delivery_charge = 60
    else:
        delivery_charge = 0
    final_total = discounted_total + delivery_charge
    return {
        "original_total": original_total,
        "discount": discount,
        "final_total": final_total
    }

def filter_items_logic(category=None, max_price=None, unit=None, in_stock=None):
    result = items

    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if unit is not None:
        result = [i for i in result if i["unit"].lower() == unit.lower()]

    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    return result

@app.get("/helpers/test")
def test_helpers(item_id: int, quantity: int = 1, delivery_slot: str = "Morning", bulk_order: bool = False):
    
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found (find_item failed)")

    total_data = calculate_order_total(item["price"], quantity, delivery_slot, bulk_order)

    return {
        "item_found": item,
        "calculation": total_data
    }


# GET ROUTES FUNCTIONS
@app.get("/")
def home():
    return {"message": "Welcome to FreshMart Grocery"}

@app.get("/items")
def get_items():
    in_stock_count = len([i for i in items if i["in_stock"]])
    return {"items": items, "total": len(items), "in_stock_count": in_stock_count}

@app.get("/items/summary")
def items_summary():
    in_stock_count = len([i for i in items if i["in_stock"]])
    out_stock = len(items) - in_stock_count
    category_count = {}
    for i in items:
        category_count[i["category"]] = category_count.get(i["category"], 0) + 1
    return {
        "total": len(items),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock,
        "categories": category_count
    }

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total": len(orders)}

# POST ORDER FUNCTIONS
@app.post("/orders")
def create_order(data: OrderRequest):
    global order_counter
    item = find_item(data.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not item["in_stock"]:
        raise HTTPException(status_code=400, detail="Item out of stock")
    total_data = calculate_order_total(item["price"], data.quantity, data.delivery_slot, data.bulk_order)
    order = {
        "order_id": order_counter,
        "customer_name": data.customer_name,
        "item_name": item["name"],
        "quantity": data.quantity,
        "unit": item["unit"],
        "delivery_slot": data.delivery_slot,
        "total_cost": total_data["final_total"],
        "status": "confirmed"
    }
    orders.append(order)
    order_counter += 1
    return order


# FILTER FUNCTION
@app.get("/items/filter")
def filter_items(category: Optional[str] = None,
                 max_price: Optional[int] = None,
                 unit: Optional[str] = None,
                 in_stock: Optional[bool] = None):

    result = filter_items_logic(category, max_price, unit, in_stock)
    return {"results": result, "total": len(result)}

# DAY 4: CRUD functions
@app.post("/items", status_code=201)
def add_item(new_item: NewItem):

    for i in items:
        if i["name"].lower() == new_item.name.lower():
            raise HTTPException(status_code=400, detail="Item already exists")

    new_id = max([i["id"] for i in items]) + 1

    item = new_item.dict()
    item["id"] = new_id

    items.append(item)

    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):

    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if price is not None:
        item["price"] = price

    if in_stock is not None:
        item["in_stock"] = in_stock

    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):

    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for order in orders:
        if order["item_name"] == item["name"]:
            raise HTTPException(status_code=400, detail="Item has active orders")

    items.remove(item)

    return {"message": "Item deleted successfully"}


#  CART FUNCTIONS
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)
    if not item or not item["in_stock"]:
        raise HTTPException(status_code=400, detail="Item unavailable")
    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Updated quantity", "cart": cart}
    cart.append({"item_id": item_id, "name": item["name"], "price": item["price"], "quantity": quantity})
    return {"message": "Added to cart", "cart": cart}

@app.get("/cart")
def view_cart():
    total = 0
    details = []
    for c in cart:
        subtotal = c["price"] * c["quantity"]
        total += subtotal
        details.append({**c, "subtotal": subtotal})
    return {"cart": details, "grand_total": total}

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Item removed"}
    raise HTTPException(status_code=404, detail="Item not in cart")

@app.post("/cart/checkout", status_code=201)
def checkout(data: CheckoutRequest):
    global order_counter
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    placed_orders = []
    grand_total = 0
    for c in cart:
        total_data = calculate_order_total(c["price"], c["quantity"], data.delivery_slot)
        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item_name": c["name"],
            "quantity": c["quantity"],
            "delivery_slot": data.delivery_slot,
            "total_cost": total_data["final_total"]
        }
        grand_total += total_data["final_total"]
        placed_orders.append(order)
        orders.append(order)
        order_counter += 1
    cart.clear()
    return {"orders": placed_orders, "grand_total": grand_total}


# SEARCH, SORT, PAGINATION FUNCTIONS
@app.get("/items/search")
def search_items(keyword: str):
    result = [i for i in items if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]
    return {"results": result, "total_found": len(result)}

@app.get("/items/sort")
def sort_items(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    reverse = True if order == "desc" else False
    sorted_items = sorted(items, key=lambda x: x[sort_by], reverse=reverse)
    return {"sorted": sorted_items}

@app.get("/items/page")
def paginate_items(page: int = 1, limit: int = 4):
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    total_pages = (total + limit - 1) // limit
    return {
        "page": page,
        "total_pages": total_pages,
        "data": items[start:end]
    }

@app.get("/orders/search")
def search_orders(name: str):
    result = [o for o in orders if name.lower() in o["customer_name"].lower()]
    return {"results": result}

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    reverse = True if order == "desc" else False
    sorted_orders = sorted(orders, key=lambda x: x["total_cost"], reverse=reverse)
    return {"orders": sorted_orders}

@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):
    total = len(orders)
    start = (page - 1) * limit
    end = start + limit
    total_pages = (total + limit - 1) // limit
    return {
        "page": page,
        "total_pages": total_pages,
        "data": orders[start:end]
    }

@app.get("/items/browse")
def browse_items(keyword: Optional[str] = None,
                 category: Optional[str] = None,
                 in_stock: Optional[bool] = None,
                 sort_by: str = "price",
                 order: str = "asc",
                 page: int = 1,
                 limit: int = 4):
    result = items
    # Step 1: keyword search
    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]
    # Step 2: category filter
    if category:
        result = [i for i in result if i["category"].lower() == category.lower()]
    # Step 3: stock filter
    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]
    # Step 4: sorting
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)
    # Step 5: pagination
    total = len(result)
    start = (page - 1) * limit
    end = start + limit
    total_pages = (total + limit - 1) // limit
    return {
        "total": total,
        "page": page,
        "total_pages": total_pages,
        "data": result[start:end]
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
