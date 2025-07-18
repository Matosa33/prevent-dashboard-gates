#!/usr/bin/env python3
"""
PREVENT Dashboard - Version Production Sécurisée
Dashboard avec chargement depuis Google Drive
Aucune donnée sensible dans le code
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import json
import io
from datetime import datetime
import requests
import warnings
warnings.filterwarnings('ignore')

# Configuration Streamlit
st.set_page_config(
    page_title="PREVENT Program Dashboard",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction d'authentification
def check_password():
    """Vérifie le mot de passe pour l'accès au dashboard"""
    
    def password_entered():
        if st.session_state["password"] == st.secrets["passwords"]["gates_foundation"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Interface de connexion
    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 15px; margin: 2rem 0;'>
            <h1 style='color: white; margin: 0;'>🐔 PREVENT Program Dashboard</h1>
            <h3 style='color: white; margin: 0.5rem 0;'>Gates Foundation - Secure Access</h3>
            <p style='color: white; margin: 0; opacity: 0.9;'>Accès sécurisé aux données du programme PREVENT</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "🔐 Mot de passe Gates Foundation", 
            type="password", 
            on_change=password_entered, 
            key="password",
            help="Contactez l'administrateur pour obtenir le mot de passe"
        )
        
        st.markdown("---")
        st.markdown("**PREVENT Program Analysis** - Secured by CEVA for Gates Foundation")
        st.markdown("*Données chargées de manière sécurisée depuis Google Drive*")
        return False
        
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 15px; margin: 2rem 0;'>
            <h1 style='color: white; margin: 0;'>🐔 PREVENT Program Dashboard</h1>
            <h3 style='color: white; margin: 0.5rem 0;'>Gates Foundation - Secure Access</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "🔐 Mot de passe Gates Foundation", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("❌ Mot de passe incorrect. Veuillez réessayer.")
        return False
    else:
        return True

# Fonction de chargement des données sécurisé
@st.cache_data
def load_data():
    """Charge les données depuis Google Drive de manière sécurisée"""
    try:
        # Récupérer l'URL depuis les secrets
        if "data_urls" not in st.secrets or "farm_visits_url" not in st.secrets["data_urls"]:
            st.error("❌ Configuration des données manquante. Contactez l'administrateur.")
            return None
        
        data_url = st.secrets["data_urls"]["farm_visits_url"]
        
        # Télécharger le fichier
        with st.spinner("🔄 Chargement sécurisé des données depuis Google Drive..."):
            response = requests.get(data_url)
            response.raise_for_status()
            
            # Charger le fichier Excel
            df = pd.read_excel(io.BytesIO(response.content), sheet_name="Farm visits PREVENT")
        
        # Nettoyer les données
        df['date_visite'] = pd.to_datetime(df['Date of the visit'], errors='coerce')
        df = df[df['date_visite'].notna()]
        df['annee'] = df['date_visite'].dt.year
        df['mois'] = df['date_visite'].dt.month
        df['trimestre'] = df['date_visite'].dt.to_period('Q')
        
        return df
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur de connexion Google Drive: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
        return None

@st.cache_data
def load_results():
    """Charge les résultats des analyses depuis Google Drive"""
    if "data_urls" not in st.secrets:
        return {}
    
    results = {}
    
    # Mapping des fichiers de résultats
    result_files = {
        'sanitaire': 'results_sanitaire',
        'zootechnique': 'results_zootechnique', 
        'portee': 'results_portee',
        'synthese': 'results_synthese'
    }
    
    for key, secret_key in result_files.items():
        if secret_key in st.secrets["data_urls"]:
            try:
                response = requests.get(st.secrets["data_urls"][secret_key])
                response.raise_for_status()
                results[key] = response.json()
            except Exception as e:
                st.warning(f"⚠️ Impossible de charger {key}: {str(e)}")
    
    return results

# Fonction pour créer les métriques principales
def create_main_metrics(df):
    """Calcule les métriques principales validées"""
    if df is None:
        return {
            'pays_couverts': 0,
            'visites_totales': 0,
            'croissance_factor': 0,
            'reduction_mortalite': 0,
            'reduction_antibiotiques': 0,
            'bilan_global': 'Données non disponibles'
        }
    
    # Calculs validés
    pays_couverts = df['Country'].nunique()
    visites_totales = len(df)
    
    # Croissance 2022-2024
    visits_2022 = len(df[df['annee'] == 2022])
    visits_2024 = len(df[df['annee'] == 2024])
    croissance_factor = visits_2024 / visits_2022 if visits_2022 > 0 else 0
    
    # Réduction mortalité
    data_2022 = df[df['annee'] == 2022]
    data_2024 = df[df['annee'] == 2024]
    
    mort_2022 = pd.to_numeric(data_2022['% Mortality W1'], errors='coerce').mean()
    mort_2024 = pd.to_numeric(data_2024['% Mortality W1'], errors='coerce').mean()
    
    reduction_mortalite = ((mort_2022 - mort_2024) / mort_2022 * 100) if mort_2022 > 0 else 0
    
    # Réduction antibiotiques
    atb_2022 = data_2022['ATB W1YES/NO'].str.strip().str.upper().map({'YES': 1, 'NO': 0}).mean()
    atb_2024 = data_2024['ATB W1YES/NO'].str.strip().str.upper().map({'YES': 1, 'NO': 0}).mean()
    
    reduction_antibiotiques = ((atb_2022 - atb_2024) / atb_2022 * 100) if atb_2022 > 0 else 0
    
    return {
        'pays_couverts': pays_couverts,
        'visites_totales': visites_totales,
        'croissance_factor': croissance_factor,
        'reduction_mortalite': reduction_mortalite,
        'reduction_antibiotiques': reduction_antibiotiques,
        'bilan_global': 'Positif' if reduction_mortalite > 0 else 'Stable'
    }

# Fonctions de création des graphiques
def create_mortality_chart(df):
    """Crée le graphique de mortalité"""
    try:
        mortality_data = []
        for year in [2022, 2023, 2024]:
            year_data = df[df['annee'] == year]
            mortality_w1 = pd.to_numeric(year_data['% Mortality W1'], errors='coerce').mean()
            mortality_w2 = pd.to_numeric(year_data['% Mortality W2'], errors='coerce').mean()
            
            if not pd.isna(mortality_w1):
                mortality_data.append({
                    'Année': year, 
                    'Mortalité W1 (%)': mortality_w1 * 100,
                    'Mortalité W2 (%)': mortality_w2 * 100 if not pd.isna(mortality_w2) else None
                })
        
        if not mortality_data:
            return None
        
        mort_df = pd.DataFrame(mortality_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=mort_df['Année'],
            y=mort_df['Mortalité W1 (%)'],
            mode='lines+markers',
            name='Mortalité W1',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10)
        ))
        
        if mort_df['Mortalité W2 (%)'].notna().any():
            fig.add_trace(go.Scatter(
                x=mort_df['Année'],
                y=mort_df['Mortalité W2 (%)'],
                mode='lines+markers',
                name='Mortalité W2',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            title='Évolution de la Mortalité par Année',
            title_x=0.5,
            height=400,
            xaxis_title="Année",
            yaxis_title="Mortalité (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Ajouter source
        fig.add_annotation(
            text="Source: Farm_Visits.xlsx - Colonnes: % Mortality W1, % Mortality W2",
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            font=dict(size=10, color="gray")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur création graphique mortalité: {str(e)}")
        return None

def create_antibiotic_chart(df):
    """Crée le graphique d'usage des antibiotiques"""
    try:
        antibiotic_data = []
        for year in [2022, 2023, 2024]:
            year_data = df[df['annee'] == year]
            
            atb_w1 = year_data['ATB W1YES/NO'].str.strip().str.upper().map({'YES': 1, 'NO': 0}).mean()
            atb_w2 = year_data['ATB W2 YES/NO'].str.strip().str.upper().map({'YES': 1, 'NO': 0}).mean()
            
            if not pd.isna(atb_w1):
                antibiotic_data.append({
                    'Année': year,
                    'ATB W1 (%)': atb_w1 * 100,
                    'ATB W2 (%)': atb_w2 * 100 if not pd.isna(atb_w2) else None
                })
        
        if not antibiotic_data:
            return None
        
        atb_df = pd.DataFrame(antibiotic_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=atb_df['Année'],
            y=atb_df['ATB W1 (%)'],
            mode='lines+markers',
            name='Antibiotiques W1',
            line=dict(color='#d62728', width=3),
            marker=dict(size=10)
        ))
        
        if atb_df['ATB W2 (%)'].notna().any():
            fig.add_trace(go.Scatter(
                x=atb_df['Année'],
                y=atb_df['ATB W2 (%)'],
                mode='lines+markers',
                name='Antibiotiques W2',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            title='Évolution de l\'Usage des Antibiotiques',
            title_x=0.5,
            height=400,
            xaxis_title="Année",
            yaxis_title="Usage Antibiotiques (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Ajouter source
        fig.add_annotation(
            text="Source: Farm_Visits.xlsx - Colonnes: ATB W1YES/NO, ATB W2 YES/NO",
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            font=dict(size=10, color="gray")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur création graphique antibiotiques: {str(e)}")
        return None

def create_geographic_chart(df):
    """Crée le graphique de distribution géographique"""
    try:
        country_counts = df['Country'].value_counts().head(10)
        
        fig = px.bar(
            x=country_counts.index,
            y=country_counts.values,
            title='Distribution des Visites par Pays (Top 10)',
            labels={'x': 'Pays', 'y': 'Nombre de Visites'},
            color=country_counts.values,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            title_x=0.5,
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        
        # Ajouter source
        fig.add_annotation(
            text="Source: Farm_Visits.xlsx - Colonnes: Country, Date of the visit",
            xref="paper", yref="paper",
            x=0, y=-0.25,
            showarrow=False,
            font=dict(size=10, color="gray")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur création graphique géographique: {str(e)}")
        return None

def create_temporal_chart(df):
    """Crée le graphique d'évolution temporelle"""
    try:
        monthly_data = df.groupby(['annee', 'mois']).size().reset_index(name='visites')
        monthly_data['date'] = pd.to_datetime(monthly_data['annee'].astype(str) + '-' + monthly_data['mois'].astype(str) + '-01')
        
        fig = px.line(
            monthly_data,
            x='date',
            y='visites',
            title='Évolution Mensuelle des Visites',
            markers=True,
            color_discrete_sequence=['#2ca02c']
        )
        
        fig.update_layout(
            title_x=0.5,
            height=400,
            xaxis_title="Date",
            yaxis_title="Nombre de Visites"
        )
        
        # Ajouter source
        fig.add_annotation(
            text="Source: Farm_Visits.xlsx - Colonnes: Date of the visit",
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            font=dict(size=10, color="gray")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur création graphique temporel: {str(e)}")
        return None

# Interface principale
def main():
    """Interface principale du dashboard"""
    
    # Vérification mot de passe
    if not check_password():
        st.stop()
    
    # Header sécurisé
    st.markdown("""
    <div style='background: linear-gradient(90deg, #1f77b4, #ff7f0e); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; text-align: center; margin: 0;'>🐔 PREVENT Program Dashboard</h1>
        <p style='color: white; text-align: center; margin: 0;'>Gates Foundation - Secure Analytics Platform</p>
        <p style='color: white; text-align: center; margin: 0; font-size: 0.9em; opacity: 0.9;'>🔒 Données chargées de manière sécurisée depuis Google Drive</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton de déconnexion
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🔓 Déconnexion", type="secondary"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Chargement des données
    with st.spinner("🔄 Chargement sécurisé des données..."):
        df = load_data()
        results = load_results()
    
    if df is None:
        st.error("❌ Impossible de charger les données. Contactez l'administrateur.")
        st.stop()
    
    # Métriques principales
    metrics = create_main_metrics(df)
    
    # Affichage des métriques
    st.markdown("## 📊 Vue d'ensemble du Programme PREVENT")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🌍 Pays couverts", 
            metrics['pays_couverts'],
            help="Nombre de pays africains couverts par le programme"
        )
    
    with col2:
        st.metric(
            "🏥 Visites réalisées", 
            f"{metrics['visites_totales']:,}",
            help="Nombre total de visites de fermes effectuées"
        )
    
    with col3:
        st.metric(
            "📈 Croissance", 
            f"{metrics['croissance_factor']:.1f}x",
            help="Facteur de croissance 2022-2024"
        )
    
    with col4:
        st.metric(
            "🩺 Réduction Mortalité", 
            f"{metrics['reduction_mortalite']:.1f}%",
            help="Réduction de la mortalité W1 (2022-2024)"
        )
    
    with col5:
        st.metric(
            "💊 Réduction ATB", 
            f"{metrics['reduction_antibiotiques']:.1f}%",
            help="Réduction usage antibiotiques W1 (2022-2024)"
        )
    
    # Onglets principaux
    tabs = st.tabs([
        "📊 Impact Sanitaire", 
        "🗺️ Portée Géographique", 
        "📈 Évolution Temporelle",
        "🔍 Sécurité & Traçabilité"
    ])
    
    with tabs[0]:
        st.markdown("### 📊 Impact Sanitaire")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Évolution de la Mortalité")
            fig_mortality = create_mortality_chart(df)
            if fig_mortality:
                st.plotly_chart(fig_mortality, use_container_width=True)
        
        with col2:
            st.markdown("#### Évolution des Antibiotiques")
            fig_antibiotic = create_antibiotic_chart(df)
            if fig_antibiotic:
                st.plotly_chart(fig_antibiotic, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### 🗺️ Portée Géographique")
        
        fig_geo = create_geographic_chart(df)
        if fig_geo:
            st.plotly_chart(fig_geo, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### 📈 Évolution Temporelle")
        
        fig_temporal = create_temporal_chart(df)
        if fig_temporal:
            st.plotly_chart(fig_temporal, use_container_width=True)
    
    with tabs[3]:
        st.markdown("### 🔍 Informations Sécurité & Traçabilité")
        
        # Informations de sécurité
        st.success("🔒 Connexion sécurisée établie")
        st.info("📊 Données chargées de manière sécurisée depuis Google Drive")
        st.info("🔐 Aucune donnée sensible stockée dans le code source")
        
        # Statistiques techniques
        with st.expander("📋 Statistiques Techniques"):
            st.write("**Données chargées:**")
            st.write(f"- Lignes: {len(df):,}")
            st.write(f"- Colonnes: {len(df.columns)}")
            st.write(f"- Période: {df['date_visite'].min().strftime('%Y-%m-%d')} à {df['date_visite'].max().strftime('%Y-%m-%d')}")
            st.write(f"- Pays: {df['Country'].nunique()}")
            st.write(f"- Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Traçabilité
        with st.expander("🔍 Traçabilité des Données"):
            st.write("**Sources de données:**")
            st.write("- **Données principales**: Google Drive (Farm_Visits.xlsx)")
            st.write("- **Fichiers JSON**: Google Drive (résultats d'analyses)")
            st.write("- **Sécurité**: Authentification par mot de passe")
            st.write("- **Chiffrement**: HTTPS pour tous les transferts")
            st.write("- **Accès**: Contrôlé par URL + authentification")
    
    # Footer sécurisé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;'>
        <p><strong>🔒 PREVENT Program Dashboard - Secured Access</strong></p>
        <p>Generated by CEVA for Gates Foundation | Last updated: {}</p>
        <p>🔐 Données chargées de manière sécurisée depuis Google Drive</p>
        <p>⚠️ Données confidentielles - Usage autorisé uniquement</p>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

if __name__ == "__main__":
    main()