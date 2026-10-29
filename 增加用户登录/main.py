import streamlit as st

# 1. Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# 2. Define all available pages
page_login = st.Page("views/login.py", title="Login", icon="🔒")
page_dashboard = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
page_sales = st.Page("views/sales.py", title="Sales Report", icon="📈")
page_inventory = st.Page("views/inventory.py", title="Inventory Management", icon="📦")
page_settings = st.Page("views/settings.py", title="App Settings", icon="⚙️")

# 3. Dynamic Navigation Logic based on Roles
if not st.session_state.logged_in:
    # If not logged in, they can ONLY see the login page
    pages_to_show = [page_login]
else:
    # Define accessible pages based on role strings
    role = st.session_state.user_role
    
    # "Staff" group setup
    core_apps = [page_dashboard, page_sales]
    if role == "Admin":
        # Admins get extra pages added to the "Core Apps" list
        core_apps.append(page_inventory)
    
    # Structure the sidebar navigation groups dictionary
    pages_to_show = {
        "Core Apps": core_apps
    }
    
    # If Admin, inject an entire extra section header into the sidebar dictionary
    if role == "Admin":
        pages_to_show["System & Controls"] = [page_settings]

# 4. Initialize Navigation Layout
navigation_menu = st.navigation(pages_to_show)

# 5. Optional: Add a Logout button at the bottom of the sidebar if authenticated
if st.session_state.logged_in:
    with st.sidebar:
        st.write(f"👤 Logged in as: **{st.session_state.user_role}**")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()

# 6. Execute the app
navigation_menu.run()
