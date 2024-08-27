import streamlit as st
import os
import zipfile
import pikepdf

def run():
    st.title("PDF Decryptor")

    # File uploader for ZIP files containing PDFs
    uploaded_zip = st.file_uploader(
        "Upload a ZIP file containing encrypted PDFs. Please compress your encrypted files into a ZIP file before uploading.", 
        type=["zip"]
    )

    if uploaded_zip is not None:
        # Ensure that the uploaded file is indeed a ZIP file
        if uploaded_zip.name.endswith(".zip"):
            # Create temporary directories for uploaded and decrypted PDFs
            uploaded_dir = "uploaded_pdfs"
            decrypted_dir = "decrypted_pdfs"

            # Extract ZIP file
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                zip_ref.extractall(uploaded_dir)
                st.write("ZIP file extracted successfully.")

            # Find all PDF files in the extracted folder
            pdf_files = [
                os.path.join(root, file)
                for root, _, files in os.walk(uploaded_dir)
                for file in files if file.endswith(".pdf")
            ]
            
            st.write(f"Found {len(pdf_files)} PDF files in the uploaded ZIP file.")

            if pdf_files and st.button("Decrypt PDFs"):
                # Create output directory for decrypted files
                os.makedirs(decrypted_dir, exist_ok=True)

                decrypted_files = []

                for file_path in pdf_files:
                    output_filename = os.path.join(decrypted_dir, 'decrypted_' + os.path.basename(file_path))

                    try:
                        # Decrypt the PDF using pikepdf
                        with pikepdf.open(file_path) as pdf:
                            pdf.save(output_filename)
                        decrypted_files.append(output_filename)
                        st.write(f"Decrypted: {os.path.basename(file_path)}")
                    except Exception as e:
                        st.error(f"Failed to decrypt {os.path.basename(file_path)}: {e}")

                if decrypted_files:
                    # Create a ZIP file of the decrypted PDFs
                    zip_filename = 'decrypted_pdfs.zip'
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        for filename in decrypted_files:
                            zipf.write(filename, os.path.basename(filename))

                    # Offer the decrypted ZIP file for download
                    with open(zip_filename, "rb") as fp:
                        st.download_button(
                            label="Download Decrypted PDFs",
                            data=fp,
                            file_name=zip_filename,
                            mime="application/zip"
                        )
                else:
                    st.error("No files were decrypted. Please check if the PDFs are properly encrypted.")
        else:
            st.error("The uploaded file is not a ZIP file. Please upload a valid ZIP file.")

if __name__ == "__main__":
    run()
