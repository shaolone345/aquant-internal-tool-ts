import streamlit as st
import decrypt.py
import app2
import app3
from utils import check_login

def main():
    if check_login():
        st.sidebar.title("Navigation")
        app_choice = st.sidebar.radio("Choose an app:", ("Decrypt", "App 2", "App 3"))

        if app_choice == "Decrypt":
            decrypt.run()
        elif app_choice == "App 2":
            app2.run()
        elif app_choice == "App 3":
            app3.run()

if __name__ == "__main__":
    main()
