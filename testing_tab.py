import pandas as pd 
import streamlit as st

option = st.selectbox("first BPI select Oprion", ('Ipam', 'gnbdu', 'cucp'))

st.write('selected : ', option)
