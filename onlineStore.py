import streamlit as st

# -----------------------------
# Bubble Tea Shop - Complete Version
# -----------------------------

PRODUCTS = [
    {"id": "p1", "title": "Bubble Milk Tea", "description": "Classic favorite with chewy tapioca pearls", "price": 60, "emoji": "🧋", "category": "tea"},
    {"id": "p2", "title": "Yakult Green Tea", "description": "Refreshing green tea with tangy Yakult", "price": 55, "emoji": "🍵", "category": "tea"},
    {"id": "p3", "title": "Matcha Latte", "description": "Rich matcha flavor with creamy milk", "price": 70, "emoji": "🍵", "category": "latte"},
    {"id": "p4", "title": "Oolong Milk Tea", "description": "Perfect blend of oolong tea and fresh milk", "price": 65, "emoji": "🥛", "category": "tea"},
    {"id": "p5", "title": "Winter Melon Lemon", "description": "Traditional winter melon with fresh lemon", "price": 50, "emoji": "🍋", "category": "fruit"},
    {"id": "p6", "title": "Taro Milk Tea", "description": "Creamy taro blended with milk tea", "price": 65, "emoji": "🟣", "category": "tea"},
    {"id": "p7", "title": "Brown Sugar Boba", "description": "Sweet brown sugar syrup with fresh milk and boba", "price": 75, "emoji": "🧋", "category": "special"},
    {"id": "p8", "title": "Thai Milk Tea", "description": "Rich and creamy Thai-style tea", "price": 60, "emoji": "🧡", "category": "tea"},
    {"id": "p9", "title": "Mango Smoothie", "description": "Fresh mango blended into a creamy smoothie", "price": 80, "emoji": "🥭", "category": "fruit"},
    {"id": "p10", "title": "Strawberry Milk Tea", "description": "Sweet strawberry flavor with milk tea", "price": 70, "emoji": "🍓", "category": "fruit"},
    {"id": "p11", "title": "Caramel Latte", "description": "Smooth coffee with sweet caramel", "price": 75, "emoji": "☕", "category": "latte"},
    {"id": "p12", "title": "Lemon Green Tea", "description": "Refreshing green tea with fresh lemon", "price": 50, "emoji": "🍋", "category": "tea"},
    {"id": "p13", "title": "Honey Milk Tea", "description": "Natural honey sweetness with milk tea", "price": 65, "emoji": "🍯", "category": "tea"},
    {"id": "p14", "title": "Passion Fruit Tea", "description": "Tropical passion fruit with green tea", "price": 60, "emoji": "🟠", "category": "fruit"},
    {"id": "p15", "title": "Coconut Smoothie", "description": "Creamy coconut blended smoothie", "price": 75, "emoji": "🥥", "category": "fruit"},
    {"id": "p16", "title": "Black Tea Latte", "description": "Classic black tea with steamed milk", "price": 65, "emoji": "☕", "category": "latte"},
    {"id": "p17", "title": "Peach Oolong Tea", "description": "Fragrant oolong with sweet peach", "price": 60, "emoji": "🍑", "category": "tea"},
    {"id": "p18", "title": "Hazelnut Latte", "description": "Nutty hazelnut flavor with espresso", "price": 80, "emoji": "🌰", "category": "latte"},
    {"id": "p19", "title": "Rose Milk Tea", "description": "Delicate rose flavor with milk tea", "price": 70, "emoji": "🌹", "category": "tea"},
    {"id": "p20", "title": "Watermelon Juice", "description": "Fresh watermelon juice, perfect for summer", "price": 55, "emoji": "🍉", "category": "fruit"},
    {"id": "p21", "title": "Chocolate Milk Tea", "description": "Rich chocolate combined with milk tea", "price": 70, "emoji": "🍫", "category": "tea"},
    {"id": "p22", "title": "Vanilla Latte", "description": "Smooth vanilla with rich espresso", "price": 75, "emoji": "☕", "category": "latte"},
    {"id": "p23", "title": "Lychee Tea", "description": "Sweet lychee with jasmine green tea", "price": 60, "emoji": "🍇", "category": "tea"},
    {"id": "p24", "title": "Pineapple Smoothie", "description": "Tropical pineapple blended smoothie", "price": 75, "emoji": "🍍", "category": "fruit"},
    {"id": "p25", "title": "Earl Grey Milk Tea", "description": "Aromatic Earl Grey with creamy milk", "price": 65, "emoji": "☕", "category": "tea"},
    {"id": "p26", "title": "Kiwi Fruit Tea", "description": "Tangy kiwi with green tea", "price": 60, "emoji": "🥝", "category": "fruit"},
    {"id": "p27", "title": "Mocha Latte", "description": "Espresso with chocolate and steamed milk", "price": 80, "emoji": "☕", "category": "latte"},
    {"id": "p28", "title": "Almond Milk Tea", "description": "Nutty almond flavor with milk tea", "price": 70, "emoji": "🥜", "category": "tea"},
    {"id": "p29", "title": "Blueberry Smoothie", "description": "Antioxidant-rich blueberry smoothie", "price": 80, "emoji": "🫐", "category": "fruit"},
    {"id": "p30", "title": "Jasmine Green Tea", "description": "Fragrant jasmine flowers with green tea", "price": 50, "emoji": "🌸", "category": "tea"},
]

SIZE_OPTIONS = {
    "Medium": 0,
    "Large": 10,
}

SUGAR_OPTIONS = ["Regular", "Less Sugar", "Half Sugar", "Slightly Sweet", "No Sugar"]
ICE_OPTIONS = ["Regular Ice", "Less Ice", "No Ice", "Hot"]

# -----------------------------
# Session State Initialization
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {(pid, size, sugar, ice): qty}
if "show_checkout" not in st.session_state:
    st.session_state.show_checkout = False
if "order_completed" not in st.session_state:
    st.session_state.order_completed = None

# -----------------------------
# Helper Functions
# -----------------------------
def format_currency(amount):
    return f"NT$ {amount}"

def add_to_cart(pid, size, sugar, ice, qty=1):
    key = (pid, size, sugar, ice)
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

# Sidebar - Category Filter and Search
st.sidebar.subheader("🔍 Filter & Search")

category_filter = st.sidebar.radio(
    "Category",
    options=["All", "Tea", "Latte", "Fruit", "Special"],
    index=0
)

search_query = st.sidebar.text_input("Search drinks", "")

st.sidebar.divider()
st.sidebar.subheader("🛒 Shopping Cart")

if not st.session_state.cart:
    st.sidebar.write("Your cart is empty")
else:
    total = 0
    cart_snapshot = list(st.session_state.cart.items())

    for (pid, size, sugar, ice), qty in cart_snapshot:
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            continue
        
        size_price = SIZE_OPTIONS.get(size, 0)
        item_price = product["price"] + size_price
        
        st.sidebar.write(f"{product['emoji']} **{product['title']}**")
        st.sidebar.caption(f"{size} | {sugar} | {ice}")
        st.sidebar.write(f"{format_currency(item_price)} × {qty} = {format_currency(item_price * qty)}")

        new_qty = st.sidebar.number_input(
            f"Quantity",
            min_value=0,
            value=qty,
            key=f"qty_{pid}_{size}_{sugar}_{ice}"
        )
        if new_qty != qty:
            update_cart_qty((pid, size, sugar, ice), new_qty)
        
        total += item_price * qty
        st.sidebar.divider()

    st.sidebar.markdown(f"### **Total:** {format_currency(total)}")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Clear Cart", use_container_width=True):
            clear_cart()
    with col2:
        if st.button("Checkout", use_container_width=True, type="primary"):
            st.session_state.show_checkout = True
            st.rerun()

# -----------------------------
# Product Display with Category Tabs
# -----------------------------
# Only show menu if not in checkout mode
if not st.session_state.show_checkout:
    st.subheader("☕ Menu")

    # Filter products by category and search
    filtered_products = [
        p for p in PRODUCTS
        if (category_filter == "All" or p["category"] == category_filter.lower())
        and (search_query.lower() in p["title"].lower() or search_query.lower() in p["description"].lower())
    ]

    # Show category count
    if category_filter != "All":
        st.caption(f"Showing {len(filtered_products)} drinks in {category_filter} category")
    else:
        st.caption(f"Showing all {len(filtered_products)} drinks")

    if not filtered_products:
        st.info("No drinks found. Try a different search or category!")
    else:
        for product in filtered_products:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"## {product['emoji']}")
                with col2:
                    st.markdown(f"### {product['title']}")
                    st.caption(f"🏷️ {product['category'].title()}")
                    st.write(product["description"])
                    st.write(f"💰 Price: {format_currency(product['price'])} and up")
                    
                    # Create three columns for size, sugar, and ice
                    size_col, sugar_col, ice_col = st.columns(3)
                    
                    with size_col:
                        size = st.selectbox(
                            "Size",
                            options=list(SIZE_OPTIONS.keys()),
                            key=f"size_{product['id']}"
                        )
                        size_price = SIZE_OPTIONS[size]
                        if size_price > 0:
                            st.caption(f"+{format_currency(size_price)}")
                    
                    with sugar_col:
                        sugar = st.selectbox(
                            "Sugar Level",
                            options=SUGAR_OPTIONS,
                            key=f"sugar_{product['id']}"
                        )
                    
                    with ice_col:
                        # Only tea and latte categories can have Hot option
                        if product["category"] in ["tea", "latte"]:
                            ice_options = ICE_OPTIONS
                        else:
                            ice_options = [opt for opt in ICE_OPTIONS if opt != "Hot"]
                        
                        ice = st.selectbox(
                            "Ice Level",
                            options=ice_options,
                            key=f"ice_{product['id']}"
                        )
                    
                    if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True):
                        add_to_cart(product["id"], size, sugar, ice)
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
            
            submitted = st.form_submit_button("Place Order", type="primary")
            
            if submitted:
                if not name or not phone:
                    st.error("Please fill in all required fields")
                else:
                    total = sum(
                        (next((p["price"] for p in PRODUCTS if p["id"] == pid), 0) + SIZE_OPTIONS.get(size, 0)) * qty
                        for (pid, size, sugar, ice), qty in st.session_state.cart.items()
                    )
                    
                    st.session_state.order_completed = {
                        "id": f"ORD-{abs(hash(str(st.session_state.cart))) % 100000}",
                        "customer": {"name": name, "phone": phone},
                        "items": st.session_state.cart.copy(),
                        "total": total,
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
    
    st.write(f"**Name:** {order['customer']['name']}")
    st.write(f"**Phone:** {order['customer']['phone']}")
    
    st.divider()
    st.subheader("🧾 Order Details")
    
    for (pid, size, sugar, ice), qty in order["items"].items():
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if product:
            size_price = SIZE_OPTIONS.get(size, 0)
            item_price = product["price"] + size_price
            st.write(f"{product['emoji']} {product['title']} ({size} | {sugar} | {ice}) × {qty} = {format_currency(item_price * qty)}")
    
    st.divider()
    st.markdown(f"### 💰 Total Amount: {format_currency(order['total'])}")
    st.info("⏰ Thank you for your order! Please proceed to the counter for pickup.")
    
    if st.button("Return to Shop", type="primary"):
        reset_order()
