import streamlit as st

# -----------------------------
# Advanced Online Shop - Streamlit Version (Fixed)
# -----------------------------

PRODUCTS = [
    {"id": "p1", "title": "Classic White T-Shirt", "description": "100% cotton, breathable and comfortable.", "price": 499},
    {"id": "p2", "title": "Street Hoodie", "description": "Soft brushed interior for warmth.", "price": 1290},
    {"id": "p3", "title": "Classic Jeans", "description": "Durable denim with a timeless cut.", "price": 1890},
    {"id": "p4", "title": "Running Sneakers", "description": "Lightweight cushioning for running and daily wear.", "price": 2590},
]

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'show_checkout' not in st.session_state:
    st.session_state.show_checkout = False
if 'order_completed' not in st.session_state:
    st.session_state.order_completed = None

# Helper functions

def format_currency(amount):
    return f"NT$ {amount:,}"

def add_to_cart(product_id, qty=1):
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + qty

def remove_from_cart(product_id):
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def set_qty(product_id, qty):
    if qty <= 0:
        remove_from_cart(product_id)
    else:
        st.session_state.cart[product_id] = qty

def clear_cart():
    st.session_state.cart = {}

# -----------------------------
# UI Layout
# -----------------------------

st.title("Advanced Online Shop")

# Sidebar: Search and Cart
search_query = st.sidebar.text_input("Search products", "")

st.sidebar.subheader("Shopping Cart")
if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    total = 0
    for pid, qty in list(st.session_state.cart.items()):  # use list() to avoid runtime error if dict changes
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if not product:
            continue
        st.sidebar.write(f"{product['title']} x {qty} = {format_currency(product['price'] * qty)}")
        new_qty = st.sidebar.number_input(f"Quantity for {product['title']}", min_value=0, value=qty, key=f"qty_{pid}")
        set_qty(pid, new_qty)
        total += product['price'] * new_qty

    shipping = 120 if total > 0 else 0
    st.sidebar.write(f"Subtotal: {format_currency(total)}")
    st.sidebar.write(f"Shipping: {format_currency(shipping)}")
    st.sidebar.write(f"Total: {format_currency(total + shipping)}")

    if st.sidebar.button("Clear Cart"):
        clear_cart()

    if st.sidebar.button("Checkout"):
        st.session_state.show_checkout = True

# Filter products
filtered_products = [p for p in PRODUCTS if search_query.lower() in p['title'].lower() or search_query.lower() in p['description'].lower()]

# Display products
for product in filtered_products:
    st.subheader(product['title'])
    st.write(product['description'])
    st.write(f"Price: {format_currency(product['price'])}")
    if st.button("Add to Cart", key=f"add_{product['id']}"):
        add_to_cart(product['id'])
        st.success(f"Added {product['title']} to cart!")

# Checkout form
if st.session_state.show_checkout:
    st.subheader("Checkout")
    with st.form(key='checkout_form'):
        name = st.text_input("Full Name", "")
        email = st.text_input("Email", "")
        address = st.text_area("Shipping Address", "")
        submitted = st.form_submit_button("Place Order")
        if submitted:
            total = sum(PRODUCTS[i]['price']*qty for i, (pid, qty) in enumerate(st.session_state.cart.items()) if any(p['id']==pid for p in PRODUCTS))
            shipping = 120 if total > 0 else 0
            st.session_state.order_completed = {
                "id": f"ORD-{st.session_state.cart.__hash__()}",
                "customer": {"name": name, "email": email, "address": address},
                "items": st.session_state.cart.copy(),
                "total": total + shipping
            }
            st.session_state.cart = {}
