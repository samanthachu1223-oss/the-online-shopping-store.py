import streamlit as st

# -----------------------------
# Bubble Tea Shop - Complete Version
# -----------------------------

PRODUCTS = [
    {"id": "p1", "title": "Bubble Milk Tea", "description": "Classic favorite with chewy tapioca pearls", "price": 60, "emoji": "🧋"},
    {"id": "p2", "title": "Yakult Green Tea", "description": "Refreshing green tea with tangy Yakult", "price": 55, "emoji": "🍵"},
    {"id": "p3", "title": "Matcha Latte", "description": "Rich matcha flavor with creamy milk", "price": 70, "emoji": "🍵"},
    {"id": "p4", "title": "Oolong Milk Tea", "description": "Perfect blend of oolong tea and fresh milk", "price": 65, "emoji": "🥛"},
    {"id": "p5", "title": "Winter Melon Lemon", "description": "Traditional winter melon with fresh lemon", "price": 50, "emoji": "🍋"},
]

SIZE_OPTIONS = {
    "Medium": 0,
    "Large": 10,
}

# -----------------------------
# Session State Initialization
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {(pid, size): qty}
if "show_checkout" not in st.session_state:
    st.session_state.show_checkout = False
if "order_completed" not in st.session_state:
    st.session_state.order_completed = None

# -----------------------------
# Helper Functions
# -----------------------------
def format_currency(amount):
    return f"NT$ {amount}"

def add_to_cart(pid, size, qty=1):
    key = (pid, size)
    st.session_state.cart[key] = st.session_state.cart.get(key, 0) + qty
    st.rerun()

def update_cart_qty(key, qty):
    if qty <= 0:
        st.session_state.cart.pop(key, None)
    else:
        st.session_state.cart[key] = qty
    st.rerun()

def clear_cart():
    st.session_state.cart = {}
    st.rerun()

def reset_order():
    st.session_state.order_completed = None
    st.session_state.show_checkout = False
    st.rerun()

# -----------------------------
# UI Layout
# -----------------------------
st.set_page_config(page_title="Bubble Tea Shop", page_icon="🧋")
st.title("🧋 Bubble Tea Shop")

# Sidebar - Shopping Cart
search_query = st.sidebar.text_input("🔍 Search drinks", "")

st.sidebar.subheader("🛒 Shopping Cart")

if not st.session_state.cart:
    st.sidebar.write("Your cart is empty")
else:
    total = 0
    cart_snapshot = list(st.session_state.cart.items())

    for (pid, size), qty in cart_snapshot:
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            continue
        
        size_price = SIZE_OPTIONS.get(size, 0)
        item_price = product["price"] + size_price
        
        st.sidebar.write(f"{product['emoji']} **{product['title']}** ({size})")
        st.sidebar.write(f"{format_currency(item_price)} × {qty} = {format_currency(item_price * qty)}")

        new_qty = st.sidebar.number_input(
            f"Quantity",
            min_value=0,
            value=qty,
            key=f"qty_{pid}_{size}"
        )
        if new_qty != qty:
            update_cart_qty((pid, size), new_qty)
        
        total += item_price * qty
        st.sidebar.divider()

    shipping = 60 if total > 0 and total < 200 else 0
    st.sidebar.markdown(f"**Subtotal:** {format_currency(total)}")
    if shipping > 0:
        st.sidebar.markdown(f"**Shipping:** {format_currency(shipping)} (Free over NT$200)")
    else:
        st.sidebar.markdown(f"**Shipping:** Free 🎉")
    st.sidebar.markdown(f"### **Total:** {format_currency(total + shipping)}")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Clear Cart", use_container_width=True):
            clear_cart()
    with col2:
        if st.button("Checkout", use_container_width=True, type="primary"):
            st.session_state.show_checkout = True
            st.rerun()

# -----------------------------
# Product Display
# -----------------------------
st.subheader("☕ Menu")

filtered_products = [
    p for p in PRODUCTS
    if search_query.lower() in p["title"].lower()
    or search_query.lower() in p["description"].lower()
]

for product in filtered_products:
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"## {product['emoji']}")
        with col2:
            st.markdown(f"### {product['title']}")
            st.write(product["description"])
            st.write(f"💰 Price: {format_currency(product['price'])} and up")
            
            size_col, btn_col = st.columns([2, 1])
            with size_col:
                size = st.selectbox(
                    "Select size",
                    options=list(SIZE_OPTIONS.keys()),
                    key=f"size_{product['id']}",
                    label_visibility="collapsed"
                )
                size_price = SIZE_OPTIONS[size]
                if size_price > 0:
                    st.caption(f"({size} +{format_currency(size_price)})")
            
            with btn_col:
                if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True):
                    add_to_cart(product["id"], size)
                    st.success("Added!")
        
        st.divider()

# -----------------------------
# Checkout Form
# -----------------------------
if st.session_state.show_checkout:
    if not st.session_state.cart:
        st.warning("Your cart is empty")
        st.session_state.show_checkout = False
    else:
        st.subheader("📝 Checkout Information")
        with st.form("checkout_form"):
            name = st.text_input("Name *")
            phone = st.text_input("Phone *")
            address = st.text_area("Delivery Address *")
            notes = st.text_area("Notes (sugar level, ice level, etc.)", placeholder="e.g., Half sugar, less ice")
            
            submitted = st.form_submit_button("Place Order", type="primary")
            
            if submitted:
                if not name or not phone or not address:
                    st.error("Please fill in all required fields")
                else:
                    total = sum(
                        (next((p["price"] for p in PRODUCTS if p["id"] == pid), 0) + SIZE_OPTIONS.get(size, 0)) * qty
                        for (pid, size), qty in st.session_state.cart.items()
                    )
                    shipping = 60 if total > 0 and total < 200 else 0
                    
                    st.session_state.order_completed = {
                        "id": f"ORD-{abs(hash(str(st.session_state.cart))) % 100000}",
                        "customer": {"name": name, "phone": phone, "address": address, "notes": notes},
                        "items": st.session_state.cart.copy(),
                        "total": total + shipping,
                    }
                    clear_cart()
                    st.session_state.show_checkout = False
                    st.rerun()

# -----------------------------
# Order Confirmation
# -----------------------------
if st.session_state.order_completed:
    order = st.session_state.order_completed
    st.success(f"✅ Order Confirmed! Order ID: {order['id']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {order['customer']['name']}")
        st.write(f"**Phone:** {order['customer']['phone']}")
    with col2:
        st.write(f"**Address:** {order['customer']['address']}")
        if order['customer']['notes']:
            st.write(f"**Notes:** {order['customer']['notes']}")
    
    st.divider()
    st.subheader("🧾 Order Details")
    
    for (pid, size), qty in order["items"].items():
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if product:
            size_price = SIZE_OPTIONS.get(size, 0)
            item_price = product["price"] + size_price
            st.write(f"{product['emoji']} {product['title']} ({size}) × {qty} = {format_currency(item_price * qty)}")
    
    st.divider()
    st.markdown(f"### 💰 Total Amount: {format_currency(order['total'])}")
    st.info("⏰ Estimated delivery time: 30-40 minutes. Thank you for your patience!")
    
    if st.button("Return to Shop", type="primary"):
        reset_order()
