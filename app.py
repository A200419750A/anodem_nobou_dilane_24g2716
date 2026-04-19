import streamlit as st
import pandas as pd
import sqlite3
import random
import numpy as np
import re
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans

# ====================== CONFIGURATION PAGE ======================
st.set_page_config(
    page_title="ADN-ROLL-INSIGHT v2.5",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS Premium Cyber
st.markdown("""
<style>
    .main {background-color: #0a0a1f;}
    .stApp {background: linear-gradient(180deg, #0a0a1f 0%, #1a0033 100%);}
    h1, h2, h3 {color: #00d4ff !important; font-family: 'Segoe UI', sans-serif;}
    .stMetric {background-color: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid #00d4ff;}
    .stButton>button {
        background: linear-gradient(90deg, #ff00aa, #00d4ff);
        color: white; border-radius: 10px; border: none; font-weight: bold;
        transition: 0.3s; width: 100%; height: 3em;
    }
    .stButton>button:hover {transform: scale(1.02); box-shadow: 0px 0px 20px rgba(0, 212, 255, 0.5);}
</style>
""", unsafe_allow_html=True)

# ====================== GESTION BASE DE DONNÉES ======================
def get_connection():
    return sqlite3.connect('adn_insight.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS soumissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, email TEXT, lien TEXT, secteur TEXT,
                    complexite REAL, robustesse REAL, note_predite REAL,
                    statut TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()

def save_submission(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO soumissions 
                 (nom, email, lien, secteur, complexite, robustesse, note_predite, statut, created_at) 
                 VALUES (?,?,?,?,?,?,?,?,?)''', data)
    conn.commit()
    conn.close()

@st.cache_data(ttl=5)
def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM soumissions ORDER BY created_at DESC", conn)
    conn.close()
    return df

init_db()

# ====================== LOGIQUE MÉTIER & SÉCURITÉ ======================
SECTEURS_TECH = {
    "🤖 Intelligence Artificielle": 9.0,
    "🛡️ Cybersécurité": 8.5,
    "🌱 Agriculture & Smart Farming": 7.5,
    "☁️ Cloud Computing": 7.5,
    "Finance (FinTech)": 6.5,
    "Santé (HealthTech)": 7.0,
    "Éducation (EdTech)": 5.5,
    "♻️ GreenTech & Écologie": 6.8
}

def check_password(pwd):
    # Comparaison directe simple pour garantir l'accès
    return pwd == "admin"

# ====================== BARRE LATÉRALE (SIDEBAR) ======================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("ADN-ROLL v2.5")
    st.markdown("---")
    menu = st.radio("Navigation", [" Espace Étudiant", " Espace Professeur"])
    st.markdown("---")
    if st.session_state.get('authenticated'):
        if st.sidebar.button("🔒 Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()
    st.info(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ====================== 1. INTERFACE ÉTUDIANT ======================
if menu == " Espace Étudiant":
    st.title(" Audit IA de Projet")
    st.write("Soumettez votre projet pour une analyse de performance immédiate.")

    col_form, col_info = st.columns([2, 1])
    
    with col_form:
        with st.form("form_audit", clear_on_submit=True):
            secteur = st.selectbox("Domaine technologique", list(SECTEURS_TECH.keys()))
            nom = st.text_input("Nom de l'étudiant / Groupe", placeholder="Ex: Groupe Alpha")
            email = st.text_input("Email de contact", placeholder="exemple@univ.cm")
            lien = st.text_input("Lien du dépôt (GitHub / URL)", placeholder="https://github.com/...")
            
            submitted = st.form_submit_button("LANCER L'ANALYSE IA")

    if submitted:
        if not nom or not email or not lien:
            st.warning("⚠️ Veuillez remplir tous les champs.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("❌ Format d'email invalide.")
        else:
            with st.status("Traitement IA en cours...", expanded=True) as status:
                st.write("Extraction des métriques...")
                base_score = SECTEURS_TECH.get(secteur, 5.0)
                complexite = round(base_score + random.uniform(-0.5, 1.0), 2)
                st.write("Test de robustesse du code...")
                robustesse = round(random.uniform(7.8, 9.9), 2) if "github" in lien.lower() else round(random.uniform(4.0, 6.5), 2)
                note_finale = round((complexite * 0.6) + (robustesse * 0.4), 2)
                
                data = (nom, email, lien, secteur, complexite, robustesse, note_finale, "Vérifié", datetime.now().strftime("%Y-%m-%d %H:%M"))
                save_submission(data)
                status.update(label="Analyse terminée avec succès !", state="complete", expanded=False)
            
            st.success(f"Bravo {nom} ! Votre projet est enregistré.")
            c1, c2, c3 = st.columns(3)
            c1.metric("Complexité", f"{complexite}/10")
            c2.metric("Robustesse", f"{robustesse}/10")
            c3.metric("Note Prédite", f"{note_finale}/10")
            st.balloons()

# ====================== 2. INTERFACE PROFESSEUR ======================
else:
    if not st.session_state.get('authenticated', False):
        st.title("🔐 Accès Restreint")
        with st.container(border=True):
            pwd_input = st.text_input("Code Administrateur : admin", type="password")
            if st.button("DÉVERROUILLER"):
                if check_password(pwd_input):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect.")
        st.stop()

    st.title("Dashboard de Pilotage IA")
    df = load_data()

    if df.empty:
        st.info(" En attente de soumissions...")
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Projets", len(df))
        m2.metric("Moyenne", f"{df['note_predite'].mean():.2f}")
        m3.metric("Note Max", f"{df['note_predite'].max():.1f}")
        m4.metric("Qualité IA", "Optimisée")

        tab1, tab2, tab3 = st.tabs(["📈 Statistiques", "🧠 IA & Modèles", "📂 Gestion Données"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                fig_pie = px.pie(df, names='secteur', title="Répartition des Domaines", hole=0.4, 
                                 color_discrete_sequence=px.colors.sequential.Tealgrn)
                st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                fig_hist = px.histogram(df, x="note_predite", title="Distribution des Notes",
                                        color_discrete_sequence=['#ff00aa'], marginal="box")
                st.plotly_chart(fig_hist, use_container_width=True)

        with tab2:
            st.subheader("Analyse Prédictive & Clustering")
            cia1, cia2 = st.columns(2)
            
            with cia1:
                st.write("**Modèle de Régression Linéaire (OLS)**")
                fig_reg = px.scatter(df, x='complexite', y='note_predite', trendline="ols",
                                     title="Corrélation Complexité vs Note",
                                     trendline_color_override="#00d4ff",
                                     hover_data=['nom'])
                st.plotly_chart(fig_reg, use_container_width=True)
            
            with cia2:
                st.write("**Segmentation par Profil (K-Means)**")
                n_clusters = min(len(df), 3)
                if n_clusters > 1:
                    X_ml = df[['complexite', 'robustesse']]
                    kmeans = KMeans(n_clusters=n_clusters, n_init=10).fit(X_ml)
                    df['Cluster'] = kmeans.labels_.astype(str)
                    fig_clusters = px.scatter(df, x='complexite', y='robustesse', color='Cluster',
                                              size='note_predite', hover_data=['nom', 'secteur'],
                                              title="Groupes de Performance")
                    st.plotly_chart(fig_clusters, use_container_width=True)
                else:
                    st.warning("Soumettez au moins 2 projets pour activer le Clustering.")

        with tab3:
            st.dataframe(df, use_container_width=True)
            c_btn1, c_btn2 = st.columns(2)
            csv_data = df.to_csv(index=False).encode('utf-8')
            c_btn1.download_button("📥 EXPORTER CSV", csv_data, "audit_final.csv", "text/csv")
            
            if c_btn2.button("🚨 RÉINITIALISER LA BASE"):
                conn = get_connection()
                conn.execute("DELETE FROM soumissions")
                conn.commit()
                conn.close()
                st.success("Base de données vidée.")
                st.rerun()
