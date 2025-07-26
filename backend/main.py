from fastapi import FastAPI, Query
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
inventory = pd.read_csv("backend/ecommerce_dataset/inventory_items.csv")
order_items = pd.read_csv("backend/ecommerce_dataset/order_items.csv")
orders = pd.read_csv("backend/ecommerce_dataset/orders.csv")
products = pd.read_csv("backend/ecommerce_dataset/products.csv")

@app.get("/")
def read_root():
    return {"message": "Chatbot Backend API Working!"}

@app.get("/top-products")
def get_top_sold_products():
    top = order_items["product_id"].value_counts().head(5)
    top_products = products[products["id"].isin(top.index)][["name", "brand"]]
    return top_products.to_dict(orient="records")

@app.get("/order-status")
def get_order_status(order_id: int = Query(...)):
    order = orders[orders["order_id"] == order_id]
    if order.empty:
        return {"error": "Order ID not found"}
    return {
        "order_id": int(order_id),
        "status": order["status"].values[0],
        "shipped_at": order["shipped_at"].values[0],
        "delivered_at": order["delivered_at"].values[0],
        "returned_at": order["returned_at"].values[0]
    }

@app.get("/inventory-check")
def get_inventory(product_name: str = Query(...)):
    inv = inventory[inventory["product_name"].str.lower() == product_name.lower()]
    available = inv[inv["sold_at"].isnull()]
    return {"product": product_name, "available_stock": len(available)}
