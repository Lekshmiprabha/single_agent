from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# --- products dictionary ---
products = {
    "Bluetooth Speaker": {"price": 45,  "rating": 4.5, "description": "Compact wireless speaker with 10-hour battery life and rich 360° sound."},
    "Laptop":            {"price": 200, "rating": 4.9, "description": "Lightweight laptop with fast processor, perfect for work and study."},
    "Keyboard":          {"price": 100, "rating": 4.2, "description": "Mechanical keyboard with tactile keys and adjustable RGB backlight."},
    "Headphone":         {"price": 20,  "rating": 4.7, "description": "Over-ear headphones with noise isolation and deep bass sound."}
}

# --- reviews dictionary ---
reviews = {
    "Bluetooth Speaker": {"number_of_reviews": 1200, "rating": 4.5},
    "Laptop":            {"number_of_reviews": 3400, "rating": 4.9},
    "Keyboard":          {"number_of_reviews": 890,  "rating": 4.2},
    "Headphone":         {"number_of_reviews": 2100, "rating": 4.7}
}

# --- tool ---
@tool
def get_full_product_details(product_name: str) -> str:
    """Given a product name, returns all details including price, description, rating and reviews."""
    name = product_name.title()
    if name not in products and name not in reviews:
        return f"Sorry, the product '{name}' is not available in our store."
    p = products[name]
    r = reviews[name]
    return (
        f"Product     : {name}\n"
        f"Price       : ${p['price']}\n"
        f"Description : {p['description']}\n"
        f"Rating      : {p['rating']} out of 5 stars\n"
        f"Reviews     : {r['number_of_reviews']:,} customers have reviewed this product"
    )

# --- agent ---
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

agent = create_react_agent(
    llm,
    tools=[get_full_product_details],
    prompt="You are a helpful product assistant for an online tech store. Use the tool to get product details and answer the user's question in a friendly, conversational way."
)

# --- chat loop ---
print("Welcome to the Product Assistant! Type 'quit' to exit.\n")

while True:
    question = input("You: ")

    if question.lower() == "quit":
        print("Goodbye! 👋")
        break

    response = agent.invoke({"messages": question})
    print(f"\nAssistant: {response['messages'][-1].content}")
    print("-" * 50)