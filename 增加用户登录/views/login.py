import streamlit as st

st.title("🔒 System Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", type="primary"):
    # Simple demo authentication logic
    if username == "admin" and password == "admin123":
        st.session_state.logged_in = True
        st.session_state.user_role = "Admin"
        st.success("Logged in as Admin!")
        st.rerun()
    elif username == "staff" and password == "staff123":
        st.session_state.logged_in = True
        st.session_state.user_role = "Staff"
        st.success("Logged in as Staff!")
        st.rerun()
    else:
        st.error("Invalid credentials (Use admin/admin123 or staff/staff123)")
