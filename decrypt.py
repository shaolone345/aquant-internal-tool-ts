import streamlit as st
import os
import zipfile
import pikepdf
from pathlib import Path
from tkinter import Tk, filedialog

def select_folders():
    """Opens a dialog to select folders and returns a list of selected folders."""
    root = Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Make sure the dialog is in front
    folders = filedialog.askdirectory(mustexist=True, title="Select Folder", multiple=True)
    return list(folders)

def run():
    st.title("PDF Decryptor")

    # Button to select folders
    if st.button("Select Folders"):
        folders = select_folders()
        if folders:
            st.session_state['selected_folders'] = folders
            st.success(f"Selected {len(folders)} folders.")
        else:
            st.error("No folders selected.")

    if 'selected_folders' in st.session_state:
        st.write("Selected Folders:")
        for folder in st.session_state['selected_folders']:
            st.write(folder)

        # Find all PDF files in the selected folders
        pdf_files = []
        for folder in st.session_state['selected_folders']:
            for root, _, files in os.walk(folder):
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
                st.error("No PDF files found in the selected folders.")

if __name__ == "__main__":
    run()

