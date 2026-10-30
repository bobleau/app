import streamlit as st

# 1. Define all the pages, point them to their file paths, and assign icons
page_app = st.Page("views/app.py", title="app", icon="📊", default=True)
page_app_json = st.Page("views/app_json.py", title="app_json", icon="📊")
page_students = st.Page("views/students.py", title="学生身高", icon="📊")
page_dashboard = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
page_sales = st.Page("views/sales.py", title="Sales Report", icon="📈")
page_inventory = st.Page("views/inventory.py", title="Inventory Management", icon="📦")
page_settings = st.Page("views/settings.py", title="App Settings", icon="⚙️")

# 2. Group multiple pages into sections using a dictionary
# The keys ("Core Apps", "System") become headers in the left sidebar
navigation_menu = st.navigation({
    "Core Apps": [
        page_app,
        page_app_json,
        page_students,
        page_dashboard, 
        page_sales, 
        page_inventory
    ],
    "System & Controls": [
        page_settings
    ]
})

# 3. Optional: Add global branding or dynamic titles to the sidebar
st.sidebar.markdown("## 🏢 Enterprise Portal")
st.sidebar.divider()

# 4. Execute the navigation logic to render the selected page on the right
navigation_menu.run()
