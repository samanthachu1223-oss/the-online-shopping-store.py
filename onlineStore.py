import streamlit as st

# Sample product data
PRODUCTS = [
    {"id": "p1", "title": "Classic White T-Shirt", "description": "100% cotton.", "price": 499},
    {"id": "p2", "title": "Street Hoodie", "description": "Soft brushed interior.", "price": 1290},
    {"id": "p3", "title": "Classic Jeans", "description": "Durable denim.", "price": 1890},
    {"id": "p4", "title": "Running Sneakers", "description": "Lightweight cushioning.", "price": 2590},
]

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'show_checkout' not in st.session_state:
    st.session_state.show_checkout = False

# Helper functions
def add_to_cart(product_id, qty=1):
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + qty
    st.experimental_rerun()  # Force refresh immediately

def clear_cart():
    st.session_state.cart = {}
    st.experimental_rerun()

# Sidebar
st.sidebar.subheader("Shopping Cart")
if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    total = 0
    for pid, qty in st.session_state.cart.items():
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if not product:
            continue
        st.sidebar.write(f"{product['title']} x {qty} = NT$ {product['price']*qty:,}")
        total += product['price'] * qty
    st.sidebar.write(f"Total: NT$ {total:,}")
    if st.sidebar.button("Clear Cart"):
        clear_cart()

# Product list
for product in PRODUCTS:
    st.subheader(product['title'])
    st.write(product['description'])
    st.write(f"Price: NT$ {product['price']:,}")
    if st.button("Add to Cart", key=product['id']):
        add_to_cart(product['id'])
