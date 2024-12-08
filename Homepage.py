import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

# set streamlit config
st.set_page_config(
    layout = 'wide',
    page_title = 'Malaysia Population Visualisation', 
)



# read data
@st.cache_data
def get_raw_df(file_path):
    print('Reading raw parquet file...')
    df = pd.read_parquet(file_path)
    df['date'] = pd.to_datetime(df['date']).dt.date

    # filter data > 1990 which contains most granular data
    processed_df = df[df['date'] > datetime.date(1990,12,31)].copy()

    def parse_age_col(age_range):
        if '+' in age_range:
            return int(age_range.replace('+', ''))
        elif len(age_range.split('-')) == 2:
            ages = [int(s) for s in age_range.split('-')]
            return sum(ages)/2
        else:
            return None
        
    processed_df['age_midr'] = processed_df['age'].apply(
        lambda x: parse_age_col(x)
    )

    return processed_df

if 'raw_df' not in st.session_state:
    PARQUET_NAME = "population_state.parquet"
    raw_df = get_raw_df(PARQUET_NAME)
    st.session_state['raw_df'] = raw_df

@st.cache_data
def get_data_min_max_year():
    data_year_list = pd.to_datetime(st.session_state['raw_df']['date']).dt.year.astype(int)
    min_year = data_year_list.min()
    max_year = data_year_list.max()

    return min_year, max_year



#------------ streamlit content
st.title('Introduction')

DATA_SOURCE_URL = 'https://data.gov.my/data-catalogue/population_state'
st.markdown(f"This is a visualisation of Malaysia Population data obtained from [here]({DATA_SOURCE_URL}) using the Streamlit library in Python.")
st.markdown("Only data from year 1991 onwards are used as they have a more standardised data category (refer to link above for more details).")
st.markdown("A sneakpeak of the data is as below. 10 random rows that fits the filter are shown.")

# User filter
cols_list_r1 = st.columns([0.2, 0.8])

with cols_list_r1[0]:
    min_year, max_year = get_data_min_max_year()

    selected_date = st.slider(
        "Year",
        min_year, max_year,
        (min_year, max_year)
    )

with cols_list_r1[1]:
    selected_states = st.multiselect(
        "State",
        st.session_state['raw_df']['state'].unique().tolist(),
        st.session_state['raw_df']['state'].unique().tolist()
    )



cols_list_r2 = st.columns([0.2, 0.5, 0.3])
with cols_list_r2[0]:


    selected_sexs = st.multiselect(
        "Sex",
        st.session_state['raw_df']['sex'].unique().tolist(),
        st.session_state['raw_df']['sex'].unique().tolist()
    )

with cols_list_r2[1]:
    selected_ages = st.multiselect(
        "Age Range",
        st.session_state['raw_df']['age'].unique().tolist(),
        st.session_state['raw_df']['age'].unique().tolist()
    )

with cols_list_r2[2]:
    selected_ethnicities = st.multiselect(
        "Ethnicity",
        st.session_state['raw_df']['ethnicity'].unique().tolist(),
        st.session_state['raw_df']['ethnicity'].unique().tolist()
    )

filtered_df = st.session_state['raw_df'][
    (pd.to_datetime(st.session_state['raw_df']['date']).dt.year.between(selected_date[0], selected_date[1])) &
    (st.session_state['raw_df']['state'].isin(selected_states)) &
    (st.session_state['raw_df']['sex'].isin(selected_sexs)) &
    (st.session_state['raw_df']['age'].isin(selected_ages)) &
    (st.session_state['raw_df']['ethnicity'].isin(selected_ethnicities))
]
filtered_df = filtered_df.rename(columns = {
    'date': 'Date',
    'state': 'State',
    'sex': 'Sex',
    'age': 'Age',
    'ethnicity': 'Ethnicity',
    'population': "Population ('000)"
}).drop(columns=['age_midr'])

st.dataframe(filtered_df.sample(min(10, len(filtered_df))), width=None, hide_index=True)


REPO_URL = 'https://github.com/LiTianYeoh/streamlit_malaysia_population'
st.markdown(f"A link to my GitHub repo can be found [here]({REPO_URL}).")