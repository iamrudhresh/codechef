import streamlit as st
import pandas as pd


st.write('# **Leetcode Data Fetch**')

file = st.file_uploader('Drop the Data here')


filtered_data = file.copy()
    
departments = ["All"] + list(file['Department'].unique())
sections = ["All"] + list(file['Section'].unique())
years = ["All"] + list(file['Year'].unique())
domains = ["All"] + list(file['Domain'].unique())

year = st.selectbox('Year', years, index=0)
department = st.selectbox('Department', departments, index=0)
domain = st.selectbox('Domain', domains, index=0)
section = st.selectbox('Section' , sections, index=0)


# if year:
#     if year != 'All':
#         filtered_data = filtered_data[filtered_data['Year'] == year]

# if department:
#     if department != 'All':
#         filtered_data = filtered_data[filtered_data['Department'] == department]
    
# if section:
#     if section != 'All':
#         filtered_data = filtered_data[filtered_data['Section'] == section]
                
# if domain:
#     if domain != 'All':
#         filtered_data = filtered_data[filtered_data['Domain'] == domain]


# if st.button('Fetch'):
#     df = filtered_data
  
#     data = []
#     error_fetching = []

#     for ind, row in df.iterrows():
#         name = str(row['Name']).strip()
#         regno = str(row['Reg Number']).strip()
#         year = str(row['Year']).strip()
#         dept = str(row['Department']).strip()
#         section = str(row['Section']).strip()
#         domain = str(row['Domain']).strip()
#         mail = str(row['Mail ID']).strip()
#         phone = str(row['Mobile Number']).strip()
#         user = str(row['Username']).strip()
        
#         problemsDict, flag = returnQuery(user, name, regno, year, dept, section, domain, mail, phone)
        
        if flag:
            data.append(problemsDict)
        else:
            error_fetching.append(problemsDict)
            print(f'{user} not found')

    dataframe = pd.DataFrame()

    if data:    
        dataframe = pd.DataFrame(data)
        dataframe.set_index('Name', inplace=True)
        
    if error_fetching:
        error = pd.DataFrame(error_fetching)
        error.set_index('Name', inplace=True)
        st.write('## **Failed to Fetch**')
        st.write(error)
    
    
    st.session_state['data'] = dataframe
    st.write(st.session_state.get('data'))


if  file.empty:
    st.session_state['data'] = pd.DataFrame()
