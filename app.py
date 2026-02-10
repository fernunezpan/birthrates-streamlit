import streamlit as st
import pandas as pd

st.title("Birthrates Over Time")

df = pd.read_csv("fertility_worldbank.csv")

st.write(df.head())