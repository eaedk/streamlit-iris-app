import streamlit as st
import pandas as pd
import os


# PAGE CONFIG : Must be the first line after the importation section
st.set_page_config(
    page_title="[Demo] Iris Classification App", page_icon="💐", layout="centered")

# Setup variables and constants
DIRPATH = os.path.dirname(os.path.realpath(__file__))
tmp_df_fp = os.path.join(DIRPATH, "assets", "tmp", "history.csv")
init_df = pd.DataFrame(
    {"petal_length": [], "petal_width": [],
     "sepal_length": [], "sepal_width": [], }
)

# FUNCTIONS


def convert_df(df):
    "Convert a dataframe so that it will be downloadable"
    return df.to_csv(index=False).encode('utf-8')


def setup(fp):
    "Setup the required elements like files, models, global variables, etc"

    # history frame
    if not os.path.exists(fp):
        df_history = init_df.copy()
    else:
        df_history = pd.read_csv(fp)

    df_history.to_csv(fp, index=False)

    return df_history


# Setup execution
try:
    df_history
except:
    df_history = setup(tmp_df_fp)

# APP Interface

# Title
st.title("💐 [Demo] Iris Classification App")

# Sidebar
st.sidebar.write(f"Demo app")
st.sidebar.write(
    f"This app shows a simple demo of a Streamlit app for Iris flower classification.")

# Main page

# Form
form = st.form(key="information", clear_on_submit=True)
with form:

    # An editable dataframe
    edited_df = st.experimental_data_editor(init_df, num_rows="dynamic",)

    submitted = st.form_submit_button(label="Submit")

    if submitted:
        try:
            st.success("Thanks!")
            st.balloons()

            df_history = pd.concat([df_history, edited_df],
                                   ignore_index=True).convert_dtypes()
            df_history.to_csv(tmp_df_fp, index=False)

        except:
            st.error(
                "Oops something went wrong, contact the client service or the admin!")

# Expander
expander = st.expander("Check the history")
with expander:

    if submitted:
        st.dataframe(df_history)
        st.download_button(
            "Download this table as CSV",
            convert_df(df_history),
            "prediction_history.csv",
            "text/csv",
            key='download-csv'
        )
