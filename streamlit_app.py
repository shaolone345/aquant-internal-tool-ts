import streamlit as st
import decrypt
import app2
import app3
from utils import check_login, logout

def main():
    if check_login():
        st.sidebar.title("Navigation")
        app_choice = st.sidebar.radio("Choose an app:", ("Decrypt", "App 2", "App 3"))
        
        # Adding the logout button in the sidebar
        logout()

         # Check if logout was triggered
        if st.session_state.get('logout'):
            st.session_state['logout'] = False
          

        if app_choice == "Decrypt PDFs":
            decrypt.run()
        elif app_choice == "App 2":
            app2.run()
        elif app_choice == "App 3":
            app3.run()

if __name__ == "__main__":
    main()
