import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    layout = 'wide',
    page_title = 'Malaysia Population Visualisation', 
)

def parse_age_col(age_range):
    if '+' in age_range:
        return int(age_range.replace('+', ''))
    elif len(age_range.split('-')) == 2:
        ages = [int(s) for s in age_range.split('-')]
        return sum(ages)/2
    else:
        return None

#-------- plot Age distribution by Ethnicity
@st.cache_data
def get_latest_ethnicity_age_fig(raw_df):
    latest_eth_age_df = raw_df[
        (pd.to_datetime(raw_df['date']).dt.year == 2023) &
        (raw_df['sex'] == 'both') &
        (raw_df['age'] != 'overall')
    ].groupby(by=['ethnicity', 'age']).agg({'population':'sum'}).reset_index()

    latest_eth_pop_df = latest_eth_age_df.groupby(by=['ethnicity']).agg({'population':'sum'}).reset_index()

    latest_eth_age_df = latest_eth_age_df.merge(
        latest_eth_pop_df, how='left', on = 'ethnicity',
        suffixes = ('_by_age', '_total')
    )

    latest_eth_age_df['proportion'] = latest_eth_age_df['population_by_age'].div(latest_eth_age_df['population_total'])
    

    latest_eth_age_df['age_midr'] = latest_eth_age_df['age'].apply(parse_age_col)
    latest_eth_age_df.sort_values(by=['ethnicity', 'age_midr'], inplace=True)

    fig = px.histogram(
        latest_eth_age_df, x = 'ethnicity', y = 'proportion',
        color = 'age', barmode='group',
        title = 'Age distribution in Malaysia (by Ethnicity)'
    )

    fig.update_xaxes(title_text = 'Ethnicity')
    fig.update_yaxes(title_text = "Proportion within Ethnic")
    fig.update_layout(yaxis_range = [0.0, 0.25], yaxis_tickformat='.0%')

    return fig

ethnicity_age_hist = get_latest_ethnicity_age_fig(st.session_state['raw_df'])


#-------- plot Ethnicity distribution by State
@st.cache_data
def get_latest_state_eth_fig(raw_df):
    latest_state_eth_df = raw_df[
        (pd.to_datetime(raw_df['date']).dt.year == 2023) &
        (raw_df['sex'] == 'both') &
        (raw_df['age'] == 'overall') &
        (raw_df['ethnicity'] != 'overall')
    ].groupby(by=['state', 'ethnicity']).agg({'population':'sum'}).reset_index()

    latest_state_pop_df = latest_state_eth_df.groupby(by=['state']).agg({'population':'sum'}).reset_index()

    latest_state_eth_df = latest_state_eth_df.merge(
        latest_state_pop_df, how='left', on = 'state',
        suffixes = ('_by_eth', '_total')
    )

    latest_state_eth_df['proportion'] = latest_state_eth_df['population_by_eth'].div(latest_state_eth_df['population_total'])

    fig = px.histogram(
        latest_state_eth_df, x = 'state', y = 'proportion',
        color = 'ethnicity', barmode='group',
        title = 'Ethnicity distribution in Malaysia (by State)'
    )

    fig.update_xaxes(title_text = 'State')
    fig.update_yaxes(title_text = 'Proportion in State')
    fig.update_layout(yaxis_range = [0.0, 0.8], yaxis_tickformat='.0%')

    return fig

state_ethnicity_hist = get_latest_state_eth_fig(st.session_state['raw_df'])

#------------ streamlit content

st.title("As of 2023 Jan")
st.markdown('This section visualise the latest data, which is on 2023 Jan.')

st.plotly_chart(ethnicity_age_hist)
st.plotly_chart(state_ethnicity_hist)