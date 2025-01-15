import streamlit as st
import pandas as pd
from googletrans import Translator
from io import BytesIO
from datetime import datetime

# Initialize the translator
translator = Translator()

# Title of the app
st.title("Excel Column Translator App")

# File upload
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)

    # Display the uploaded file's content
    st.write("Uploaded File Preview:")
    st.dataframe(df)

    # Check if the target column exists
    target_column = st.sidebar.text_input("Column to Translate (e.g., 'VC_NARRATION')", "VC_NARRATION")
    if target_column not in df.columns:
        st.error(f"Column '{target_column}' not found in the uploaded file.")
    else:
        # Select source and target languages
        st.sidebar.title("Translation Settings")
        source_lang = st.sidebar.text_input("Source Language (e.g., 'auto' for auto-detect)", "auto")
        target_lang = st.sidebar.text_input("Target Language (e.g., 'en' for English)", "en")

        # Translate button
        if st.button("Translate"):
            try:
                # Translate only the target column
                df[target_column] = df[target_column].apply(
                    lambda x: translator.translate(str(x), src=source_lang, dest=target_lang).text
                    if isinstance(x, str) else x
                )

                # Display the translated DataFrame
                st.write("Translated File Preview:")
                st.dataframe(df)

                # Generate dynamic file name
                now = datetime.now()
                file_name = f"DNTRANS_{now.strftime('%Y%m%d_%H%M')}.xlsx"

                # Save the translated file to a BytesIO object
                output = BytesIO()
                df.to_excel(output, index=False, engine="openpyxl")
                output.seek(0)

                # Provide download button
                st.download_button(
                    label="Download Translated File",
                    data=output,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Translation failed: {e}")

# Footer
st.sidebar.info("Powered by Google Translate and Streamlit")
