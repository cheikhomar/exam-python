import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Chargement des données
df = pd.read_csv('Transactions_data_complet.csv')

st.title("Dashboard des Transactions")

# Sidebar
st.sidebar.header("Filtrage")
type_transaction = st.sidebar.multiselect("Type de transaction", df['type'].unique(), default=df['type'].unique())

# Filtrage
filtered_df = df[df['type'].isin(type_transaction)]

st.subheader("Aperçu des données")
st.write(filtered_df.head())

st.subheader("Distribution des montants")
fig1 = px.histogram(filtered_df, x="montant")
st.plotly_chart(fig1)

st.subheader("Montants par date")
fig2 = px.line(filtered_df, x="date", y="montant", color="type")
st.plotly_chart(fig2)