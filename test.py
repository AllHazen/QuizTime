import streamlit as st

st.title("Tes Suara 🎵")

with open("happy_happy_cat.mp3", "rb") as f:
    st.audio(f.read(), format="audio/mp3")
