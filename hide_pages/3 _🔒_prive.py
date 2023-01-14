import streamlit as st
from datetime import datetime

import csv
from config import LOCAL_CSV

mdp = st.text_area("mdp")

if mdp == st.secrets["private_password"]:

    title = st.text_area('Titre', '''''')

    st.write('Resultat:', title)

    message = st.text_area('Message', '''''')


    st.write('Resultat:', message)


    if st.button('Message ok'):
        with open(LOCAL_CSV, 'a', newline='') as csvfile:
            fieldnames = ['datetime', 'title', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'datetime': datetime.utcnow().isoformat(), 'title': title, 'message': message})
        st.write('on csv')
    else:
        st.write('waiting')
else:
   st.write('mauvais mdp')
