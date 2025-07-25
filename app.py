import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Titre de l'application
st.title("Dashboard des Transactions")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("Transactions_data_complet.csv")
    df['TransactionStartTime'] = pd.to_datetime(df['TransactionStartTime'])
    df['year'] = df['TransactionStartTime'].dt.year
    df['month'] = df['TransactionStartTime'].dt.month
    df['day'] = df['TransactionStartTime'].dt.day
    df['hour'] = df['TransactionStartTime'].dt.hour
    df['AbsAmount'] = df['Amount'].abs()
    return df

df = load_data()

# Filtrage dans la sidebar
st.sidebar.header("Filtres")

categories = df['ProductCategory'].unique()
selected_categories = st.sidebar.multiselect(
    "Type de transaction",
    options=categories,
    default=categories
)

df_filtered = df[df['ProductCategory'].isin(selected_categories)]

# Affichage d'un échantillon
st.subheader("Aperçu des données filtrées")
st.dataframe(df_filtered.head())

# Graphique 1 : Répartition des montants
st.subheader("Distribution des montants")
fig1 = px.histogram(df_filtered, x="Amount", nbins=50, title="Histogramme des montants")
st.plotly_chart(fig1)

# Graphique 2 : Montants par date
st.subheader("Évolution des montants dans le temps")
fig2 = px.line(df_filtered.sort_values("TransactionStartTime"), 
               x="TransactionStartTime", y="Amount", color="ProductCategory", 
               title="Montants par date")
st.plotly_chart(fig2)

# Graphique 3 : Nombre de transactions par catégorie
st.subheader("Nombre de transactions par catégorie")
# On compte les catégories et on renomme les colonnes
df_cat = df_filtered['ProductCategory'].value_counts().reset_index()
df_cat.columns = ['Catégorie', 'Nombre']

# On crée le graphique
fig3 = px.bar(
    df_cat,
    x='Catégorie',
    y='Nombre',
    labels={"Catégorie": "Catégorie", "Nombre": "Nombre de transactions"},
    title="Répartition des transactions par catégorie"
)
st.plotly_chart(fig3)

# Graphique 4 : Boxplot des montants par stratégie de prix
st.subheader("Boxplot des montants par stratégie de tarification")
fig4, ax = plt.subplots()
sns.boxplot(x='PricingStrategy', y='AbsAmount', data=df_filtered, ax=ax)
st.pyplot(fig4)

# Footer
st.markdown("---")
st.caption("Projet exam-python • Streamlit • by Cheikh Omar")
