import datetime
import streamlit as st
import plotly.express as px

st.set_page_config(
    layout = 'wide',
    page_title = 'Malaysia Population Visualisation', 
)

#----------- Plot population growth by state
@st.cache_data
def get_state_ts_fig(raw_df):

    state_pop_ts_df = raw_df[
        (raw_df['sex']=='both') &
        (raw_df['age']=='overall') &
        (raw_df['ethnicity']=='overall')
    ]

    fig = px.bar(
        state_pop_ts_df, x='date', y='population', color='state',
        title = 'Population Growth in Malaysia (by State)'
    )

    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = "Population ('000)")

    return fig

state_overall_pop_ts_fig = get_state_ts_fig(st.session_state['raw_df'])



#------------ Plot population growth by ethnicity
@st.cache_data
def get_ethnicity_ts_fig(raw_df):

    ethnicity_pop_ts_df = raw_df[
        (raw_df['sex']=='both') &
        (raw_df['age']=='overall') &
        (raw_df['ethnicity']!='overall')
    ].groupby(by=['date', 'ethnicity']).agg({'population':'sum'}).reset_index()

    fig = px.bar(
        ethnicity_pop_ts_df, x='date', y='population', color='ethnicity',
        title='Population Growth in Malaysia (by Ethnicity)'
    )

    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = "Population ('000)")

    return fig

ethnicity_pop_ts_fig = get_ethnicity_ts_fig(st.session_state['raw_df'])

#------------ Plot male-female ratio by ethnicity
@st.cache_data
def get_mfRatio_state_ts_fig(raw_df):

    mfRatio_ts_df = raw_df[
        (raw_df['sex'] != 'both') &
        (raw_df['age'] == 'overall') &
        (raw_df['ethnicity'] == 'overall')
    ].pivot_table(
        index=['date', 'state'], columns='sex', values='population'
    ).reset_index()

    mfRatio_ts_df['mfRatio'] = mfRatio_ts_df['male'].div(mfRatio_ts_df['female'])

    fig = px.line(
        mfRatio_ts_df, x='date', y='mfRatio', color='state',
        title='Male/Female Ratio in Malaysia (by State)'
    )

    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = 'M/F Ratio')
    fig.update_layout(yaxis_range = [0.8, 2.5])

    return fig

mfRatio_state_fig = get_mfRatio_state_ts_fig(st.session_state['raw_df'])

#------------ Plot male-female ratio by ethnicity
@st.cache_data
def get_mfRatio_ethnicity_ts_fig(raw_df):

    mfRatio_ts_df = raw_df[
        (raw_df['sex'] != 'both') &
        (raw_df['age'] == 'overall')
    ].pivot_table(
        index=['date', 'ethnicity'], columns='sex', values='population', aggfunc='sum'
    ).reset_index()

    mfRatio_ts_df['mfRatio'] = mfRatio_ts_df['male'].div(mfRatio_ts_df['female'])

    fig = px.line(
        mfRatio_ts_df, x='date', y='mfRatio', color='ethnicity',
        title='Male/Female Ratio in Malaysia (by Ethnicity)'
    )

    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = 'M/F Ratio')
    fig.update_layout(yaxis_range = [0.8, 2.5])

    return fig

mfRatio_ethnicity_fig = get_mfRatio_ethnicity_ts_fig(st.session_state['raw_df'])


#------------ Plot average age
@st.cache_data
def get_avgAge_ethnicity_ts_fig(raw_df):

    avgAge_ts_df = raw_df[
        (raw_df['sex'] == 'both') &
        (raw_df['age'] != 'overall')
    ].groupby(by=['date', 'ethnicity', 'age_midr']).agg({'population':'sum'}).reset_index()

    avgAge_ts_df['age_pop'] = avgAge_ts_df['age_midr'] * avgAge_ts_df['population']
    eth_pop_ts_df = avgAge_ts_df.groupby(by=['date', 'ethnicity']).agg(
        {
            'population':'sum',
            'age_pop': 'sum'
        }
    ).reset_index()

    eth_pop_ts_df['age_avg'] = eth_pop_ts_df['age_pop'].div(eth_pop_ts_df['population'])

    fig = px.line(
        eth_pop_ts_df, x='date', y='age_avg', color='ethnicity',
        title='Average Age in Malaysia (by Ethnicity)'
    )

    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = 'Average Age')

    return fig

avgAge_ethnicity_fig = get_avgAge_ethnicity_ts_fig(st.session_state['raw_df'])

#------------ streamlit content

st.title('Time Series Graphs')
st.markdown('This section visualise how the data changes over time from 1991 to 2023.')

# Create two columns in the layout
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(state_overall_pop_ts_fig)
    st.plotly_chart(mfRatio_state_fig)

with col2:
    st.plotly_chart(ethnicity_pop_ts_fig)
    st.plotly_chart(mfRatio_ethnicity_fig)

st.plotly_chart(avgAge_ethnicity_fig)