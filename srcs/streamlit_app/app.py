# srcs/streamlit_app/app.py
import sys
import streamlit as st
import pandas as pd

from elasticsearch import Elasticsearch
sys.path.append('srcs')
from streamlit_app import utils, templates

INDEX = 'qp-name'
DOMAIN = '0.0.0.0'
es = Elasticsearch(host=DOMAIN)

# -- Set page config
apptitle = 'Jobs for You'

st.set_page_config(
    page_title=apptitle,  layout = 'wide',
    menu_items={
        'About': '# Confused where to work? Use this app to find out!'
        #'Get Help': 'mailto:kapadia.ka@northeastern.edu'
        }
) #TODO page_icon and menu_items

# Title the app
logo_url = 'https://cdn3.vectorstock.com/i/1000x1000/50/27/job-search-recruitment-hiring-employment-vector-21795027.jpg'
st.image(logo_url, width=100)
st.title(apptitle)

# Define the education levels
education_level_def = { 'Education Level':['Unable to read or write', 'No formal education', 'Primary Education Completed',
     'Middle Education Completed', 'Secondary Education Completed', 'Higher Secondary Education Completed',
     'Non-technical Diploma Completed', 'Technical Diploma Completed', 'ITI Cleared', 'Non-STEM Graduate', 
     'STEM Graduate', 'Masters Completed', 'PhD Completed', 'Other'],
     'Description':['please select this if the person cannot read or write', 'can read and write but do not have a formal education',
     'cleared class 5','cleared class 8', 'cleared class 10', 'cleared class 12','completed diploma in a non-technical field',
     'completed diploma in a technical field','completed Industrial Training Institute vocational course', 
     'completed a Bachelor degree in a field other than Science, Technology, Engineering or Math',
     'completed a Bachelor degree in Science, Technology, Engineering or Math', 'completed a Master degree in any field',
     'completed a PhD degree in any field', 'Other']
}
education_level_def = pd.DataFrame(education_level_def)

sector_def = {'Sector':['Aerospace & Aviation', 'Agriculture',
       'Apparel, Made-Ups & Home Furnishing', 'Automotive',
       'Beauty & Wellness', 'Banking, Financial Services and Insurance',
       'Capital Goods', 'Construction', 'Domestic Worker',
       'Electronics & Hardware', 'Food Processing',
       'Furniture & Fittings', 'Gems & Jewellery', 'Green Jobs',
       'Handicrafts & Carpets', 'Healthcare', 'Hydrocarbons',
       'Infrastructure Equipment',
       'Instrumentation, Automation, Surveillance and Communication',
       'Iron & Steel', 'IT-ITES', 'Leather', 'Life Sciences', 'Logistics',
       'Management and Entrepreneurship & Professional',
       'Media & Entertainment', 'Mining', 'Paints & Coatings ',
       'Plumbing', 'Power', 'Retail', 'Rubber', 'Sports',
       'Strategic Manufacturing', 'Telecom ', 'Textiles & Handlooms',
       'Tourism & Hospitality', 'People with Disability*']
}
sector_def = pd.DataFrame(sector_def)

# Part 1 Get Details expander
get_details_expander = st.expander("Enter Details", expanded=False)
with get_details_expander:
    # Request Input using form
    input_form = st.form("input_form")
    first_name = input_form.text_input(label='First Name', value= 'Jane')
    last_name = input_form.text_input(label='Last Name', value= 'Doe')
    email_address = input_form.text_input(label='Email Address', value= 'janedoe@gmail.com')
    birth_date = input_form.date_input(label='Birth Date')
    submit_input_form = input_form.form_submit_button("Submit")

if submit_input_form:
    st.sidebar.title("{} {}".format(first_name, last_name))    
    st.sidebar.subheader(email_address)
    age = utils.calculateAge(birth_date)
    st.sidebar.write("Age: {} years".format(age))
    #TODO collapse the expander after submission

get_education_expander = st.expander("Provide your highest level of education", expanded=False)
with get_education_expander:
    # Request educational qualification using form
    education_form = st.form("education_form")
    education_level = education_form.selectbox(
     'Please select the highest level of your education(Refer to the table below):', education_level_def['Education Level'])
    education_form.dataframe(education_level_def)
    #education_form.text_input(label='Please specify your Specialization:')
    #education_form.text_input(label='If Other, please specify:')
    submit_education_form = education_form.form_submit_button("Submit")

if submit_education_form:
    st.sidebar.write("Education: {}".format(education_level))

get_sector_expander = st.expander("Select the industry sector", expanded=False)
with get_sector_expander:
    # Request sector using form
    sector_form= st.form("sector_selected")
    sector_selected = sector_form.radio(
        'Please select the sector you are interested to work in:', sector_def)
    submit_sector_form = sector_form.form_submit_button("Submit")

if submit_sector_form:
    st.sidebar.write("Sector:{}".format(sector_selected))

get_occupations_expander = st.expander("Check out these occupations", expanded=True)
with get_occupations_expander:
    results = utils.index_search(education_level, sector_selected)
    total_hits = len(results['hits']['hits'])
    placeholder = st.empty()
    # show number of results and time taken
    with placeholder.container():
        st.write(templates.number_of_results(total_hits, results['took'] / 1000), unsafe_allow_html=True)
        # search results
        for i in range(len(results['hits']['hits'])):
            result = results['hits']['hits'][i]
            res = result['_source']['QP Name']
            st.write(templates.search_result(i, res), unsafe_allow_html=True)

