import streamlit as st
import os
import zipfile
import pikepdf

def run():
    st.title("PDF Decryptor")

    # File uploader for ZIP files containing PDFs
    uploaded_zip = st.file_uploader("Upload ZIP file containing encrypted PDFs You can only upload zip files for now so please compress your encrypted files into a zip.", type=["zip"])

    if uploaded_zip is not None:
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall('uploaded_pdfs')

        # Find all PDF files in the extracted folder
        pdf_files = []
        for root, _, files in os.walk('uploaded_pdfs'):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))

        st.write(f"Found {len(pdf_files)} PDF files.")

        if st.button("Decrypt PDFs"):
            if pdf_files:
                output_folder = 'decrypted_pdfs'

                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                decrypted_files = []

                for file_path in pdf_files:
                    input_filename = file_path
                    output_filename = os.path.join(output_folder, 'decrypted_' + os.path.basename(file_path))

                    # Decrypt the PDF using pikepdf
                    with pikepdf.open(input_filename) as pdf:
                        pdf.save(output_filename)

                    decrypted_files.append(output_filename)

                # Create a ZIP file of the decrypted PDFs
                zip_filename = 'decrypted_pdfs.zip'
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for filename in decrypted_files:
                        zipf.write(filename, os.path.basename(filename))

                with open(zip_filename, "rb") as fp:
                    st.download_button(
                        label="Download Decrypted PDFs",
                        data=fp,
                        file_name=zip_filename,
                        mime="application/zip"
                    )
            else:
                st.error("No PDF files found in the uploaded ZIP.")

if __name__ == "__main__":
    run()
