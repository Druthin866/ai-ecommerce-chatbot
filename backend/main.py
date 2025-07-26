from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# ✅ CORS to allow React frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production: replace "*" with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load CSVs from ecommerce_dataset folder
DATA_DIR = os.path.join(os.path.dirname(__file__), "ecommerce_dataset")

orders_df = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
products_df = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
inventory_df = pd.read_csv(os.path.join(DATA_DIR, "inventory_items.csv"))
users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))

# ✅ Helper function to handle chatbot prompts
def process_query(query: str) -> str:
    query = query.lower()

    if "order status" in query:
        return "To check order status, please provide your Order ID."
    elif "available" in query or "stock" in query:
        product = "shirt"  # <- Example: this should be parsed from query
        stock = inventory_df[inventory_df["product_id"] == 1]["available_quantity"].values
        return f"We currently have {stock[0]} units of {product} in stock." if stock.size > 0 else "Sorry, item not in stock."
    elif "product" in query or "details" in query:
        return str(products_df.head(3).to_dict(orient="records"))
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"

# ✅ API Endpoint
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_query = body.get("message", "")
    bot_response = process_query(user_query)
    return {"response": bot_response}
