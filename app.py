import streamlit as st
import pandas as pd

st.title("Debug")

df = pd.read_excel("fleet_data.xlsx")

st.write("Column names:")
for col in df.columns:
    st.write(repr(col))

st.dataframe(df)
