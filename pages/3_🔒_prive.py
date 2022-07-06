import streamlit as st

import csv
from config import LOCAL_CSV

st.write(st.experimental_user)


daily_message = st.text_area('Mot du jour', '''''')


st.write('Resultat:', daily_message)

feeling_message = st.text_area('Sentiment', '''''')


st.write('Resultat:', feeling_message)


if st.button('Message ok'):
    with open(LOCAL_CSV, 'a', newline='') as csvfile:
        fieldnames = ['daily_message', 'feeling_message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'daily_message': daily_message, 'feeling_message': feeling_message})
    st.write('on csv')
else:
    st.write('waiting')
