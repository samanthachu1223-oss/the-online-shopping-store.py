import streamlit as st

# -----------------------------
# Advanced Online Shop - Safe Stable Version
# -----------------------------

PRODUCTS = [
    {"id": "p1", "title": "Classic White T-Shirt", "description": "100% cotton, breathable and comfortable.", "price": 499},
    {"id": "p2", "title": "Street Hoodie", "description": "Soft brushed interior for warmth.", "price": 1290},
    {"id": "p3", "title": "Classic Jeans", "description": "Durable denim with a timeless cut.", "price": 1890},
    {"id": "p4", "title": "Running Sneakers", "description": "Lightweight cushioning for running and daily wear.", "price": 2590},
]

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "show_checkout" not in st.session_state:
    st.session_state.show_checkout = False
if "order_completed" not in st.session_state:
    st.session_state.order_completed = None

# Helper functions
def format_currency(amount):
    return f"NT$ {amount:,}"

def add_to_cart(pid, qty=1):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + qty
    st.rerun()

def update_cart_qty(pid, qty):
    if qty <= 0:
        st.session_state.cart.pop(pid, None)
    else:
        st.session_state.cart[pid] = qty
    st.rerun()

def clear_cart():
    st.session_state.cart = {}
    st.rerun()

# -----------------------------
# UI
# -----------------------------
st.title("🛒 Advanced Online Shop")

# Sidebar
search_query = st.sidebar.text_input("Search products", "")

st.sidebar.subheader("Shopping Cart")

if not st.session_state.cart:
    st.sidebar.write("Your cart is empty.")
else:
    total = 0
    cart_snapshot = list(st.session_state.cart.items())  # make a safe copy

    for pid, qty in cart_snapshot:
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            continue
        st.sidebar.write(f"**{product['title']}** — {format_currency(product['price'])} × {qty} = {format_currency(product['price'] * qty)}")

        new_qty = st.sidebar.number_input(
            f"Quantity for {product['title']}",
            min_value=0,
            value=qty,
            key=f"qty_{pid}"
        )
        if new_qty != qty:
            update_cart_qty(pid, new_qty)
        total += product["price"] * qty

    shipping = 120 if total > 0 else 0
    st.sidebar.markdown(f"**Subtotal:** {format_currency(total)}")
    st.sidebar.markdown(f"**Shipping:** {format_currency(shipping)}")
    st.sidebar.markdown(f"**Total:** {format_currency(total + shipping)}")

    if st.sidebar.button("Clear Cart"):
        clear_cart()

    if st.sidebar.button("Checkout"):
        st.session_state.show_checkout = True
        st.rerun()

# Product display
filtered_products = [
    p for p in PRODUCTS
    if search_query.lower() in p["title"].lower()
    or search_query.lower() in p["description"].lower()
]

for product in filtered_products:
    st.subheader(product["title"])
    st.write(product["description"])
    st.write(f"Price: {format_currency(product['price'])}")
    if st.button("Add to Cart", key=f"add_{product['id']}"):
        add_to_cart(product["id"])

# Checkout form
if st.session_state.show_checkout:
    st.subheader("Checkout")
    with st.form("checkout_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        address = st.text_area("Shipping Address")
        submitted = st.form_submit_button("Place Order")
        if submitted:
            total = sum(
                next((p["price"] for p in PRODUCTS if p["id"] == pid), 0) * qty
                for pid, qty in st.session_state.cart.items()
            )
            shipping = 120 if total > 0 else 0
            st.session_state.order_completed = {
                "id": f"ORD-{abs(hash(str(st.session_state.cart))) % 100000}",
                "customer": {"name": name, "email": email, "address": address},
                "items": st.session_state.cart.copy(),
                "total": total + shipping,
            }
            clear_cart()
            st.session_state.show_checkout = False
            st.rerun()

# Order confirmation
if st.session_state.order_completed:
    st.success(f"✅ Order Confirmed! ID: {st.session_state.order_completed['id']}")
    st.write(f"Total Paid: {format_currency(st.session_state.order_completed['total'])}")
