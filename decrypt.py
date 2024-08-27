def run():
    st.title("PDF Decryptor")

    # Simplified UI for Debugging
    st.write("Upload a ZIP file to start.")
    uploaded_zip = st.file_uploader("Upload ZIP", type=["zip"])

    if uploaded_zip is not None:
        st.write("ZIP file uploaded.")
        # Further processing...

if __name__ == "__main__":
    run()
