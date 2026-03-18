import streamlit as st
st.title("hello bro welcome to Hostel gpt")
user_inp=st.text_input("tumara room number daloo:")
access=["room-207", "room-404"]
if user_inp in access :
    if user_inp:
        st.write("welcome ajao andar ")
    if not user_inp:
        st.write("bhai kuch toh likha andar khali kyun choda hai ")
if user_inp not in access:
    st.write("bhai tu galat bande ka room number dala hai dekh phele room number kya hai")