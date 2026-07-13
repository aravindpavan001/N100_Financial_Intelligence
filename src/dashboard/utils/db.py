import streamlit as st


@st.cache_data(ttl=600)
def get_companies():
    return []


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    return None


@st.cache_data(ttl=600)
def get_pl(ticker):
    return None


@st.cache_data(ttl=600)
def get_bs(ticker):
    return None


@st.cache_data(ttl=600)
def get_cf(ticker):
    return None


@st.cache_data(ttl=600)
def get_sectors():
    return []


@st.cache_data(ttl=600)
def get_peers(group_name):
    return []


@st.cache_data(ttl=600)
def get_valuation(ticker):
    return None