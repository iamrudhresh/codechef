import streamlit as st
import pandas as pd
from Endpoints import returnQuery

st.write('# **Leetcode Data Fetch**')

file = st.file_uploader('Drop the Data here')

if file:
    df = pd.read_csv(file)
    users = list(df['Username'].str.strip())
    
    data = []
    error_fetching = []
    
    for ind, user in enumerate(users):
        name = str(df['Name'][ind]).strip()
        regno = str(df['Reg Number'][ind]).strip()
        year = str(df['Year'][ind]).strip()
        dept = str(df['Department'][ind]).strip()
        section = str(df['Section'][ind]).strip()
        domain = str(df['Domain'][ind]).strip()
        mail = str(df['Mail ID'][ind]).strip()
        phone = str(df['Mobile Number'][ind]).strip()
        
        problemsDict, flag = returnQuery(user, name, regno, year, dept, section, domain, mail, phone)
        
        if flag:
            data.append(problemsDict)
        else:
            error_fetching.append(problemsDict)
            print(f'{user} not found')
    if data:
        dataframe = pd.DataFrame(data)
        dataframe.set_index('Name', inplace=True)
    
    if error_fetching:
        error = pd.DataFrame(error_fetching)
        error.set_index('Name', inplace=True)
        st.write('## **Incorrect Credentials**')
        st.write(error)
    if data:
        st.session_state['data'] = dataframe
        st.write(st.session_state.get('data'))
    else:
        st.session_state['data'] = pd.DataFrame()

if not file:
    st.session_state['data'] = pd.DataFrame()
