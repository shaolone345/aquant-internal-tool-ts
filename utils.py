import streamlit as st

# Hardcoded usernames and passwords for demonstration purposes
usernames = {
    "aungkyaw": "Aquant123!",
    "douglasmurillo": "Aquant123!",
    "user3": "password3"
}

def login():
    """Login page"""
    st.title("Login Page")

    # User input
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if username in usernames and usernames[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password")

def check_login():
    """Check if the user is logged in"""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
        return False
    return True

def logout():
    """Logout function"""
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()
