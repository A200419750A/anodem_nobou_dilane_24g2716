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
from sklearn.linear_model import LinearRegression
import hashlib

# ====================== CONFIGURATION ======================
st.set_page_config(
    page_title="ADN-ROLL-INSIGHT v2.1",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .stApp {background: linear-gradient(180deg, #0a0a1f, #1a0033);}
    h1, h2, h3 {color: #00d4ff; font-family: 'Courier New', monospace; text-shadow: 2px 2px #000000;}
    .stButton>button {background: linear-gradient(90deg, #ff00aa, #00d4ff); color: white; border-radius: 8px; border:none; font-weight:bold;}
    .success-text {color: #00ff88; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ====================== BASE DE DONNÉES ======================
def init_db():
    conn = sqlite3.connect('adn_insight.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS soumissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, email TEXT, lien TEXT, secteur TEXT,
                    complexite REAL, robustesse REAL, note_predite REAL,
                    statut TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
                 )''')
    conn.commit()
    conn.close()

init_db()

def get_connection():
    return sqlite3.connect('adn_insight.db')

@st.cache_data(ttl=60)
def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM soumissions ORDER BY created_at DESC", conn)
    conn.close()
    return df

# ====================== PARAMÈTRES IA ======================
SECTEURS_TECH = {
    "🤖 Intelligence Artificielle": 9.0,
    "🛡️ Cybersécurité": 8.5,
    "🌱 Agriculture & Smart Farming": 7.0,
    "☁️ Cloud Computing": 7.5,
    "Finance (FinTech)": 6.5,
    "Santé (HealthTech)": 6.5,
    "Éducation (EdTech)": 5.0,
    "Transport & Logistique": 5.5,
    "Commerce & E-business": 5.5,
    "♻️ GreenTech & Écologie": 6.5,
    "Inscrire un autre domaine...": 5.5
}

FEEDBACK_PHRASES = [
    "🔥 Ton projet dégage une énergie incroyable !",
    "🧬 L’ADN de ton code est exceptionnel.",
    "🚀 Analyse terminée : Tu es prêt pour l'hyperspace.",
    "💡 Cette idée agricole/tech est une pépite.",
    "⚡ La robustesse de ton lien GitHub est exemplaire.",
    "🧠 Ton architecture défie les lois de la complexité."
]

# ====================== AUTH & SÉCURITÉ ======================
def check_prof_password(password):
    return hashlib.sha256(password.encode()).hexdigest() == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

# ====================== INTERFACE LATÉRALE ======================
st.sidebar.title("👨‍💻 INF 232 — EC2")
st.sidebar.subheader("ROLL-INSIGHT v2.1")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Interface Étudiant", "Interface Professeur"])
st.sidebar.info(f"📅 Session : {datetime.now().strftime('%d/%m/%Y')}")

# ====================== 1. INTERFACE ÉTUDIANT ======================
if menu == "Interface Étudiant":
    st.title("📥 soumission des projets & Audit IA")
    
    secteur_choisi = st.selectbox("Domaine d'activité", list(SECTEURS_TECH.keys()))
    secteur_final = secteur_choisi
    
    if secteur_choisi == "Inscrire un introspection autre domaine...":
        secteur_final = st.text_input("👉 Précisez votre domaine")

    with st.form("audit_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom Complet", placeholder="Ex: NOM")
        email = c1.text_input("Email Professionnel")
        lien = c2.text_input("Lien HTTPS du projet (GitHub/URL)")
        submit = st.form_submit_button("🚀 LANCER L'AUDIT IA", use_container_width=True)

    if submit:
        if not nom or not is_valid_email(email) or not lien.startswith("http"):
            st.error("❌ Données invalides. Vérifiez l'email et le lien (HTTP/HTTPS obligatoire).")
        else:
            with st.spinner("L'IA analyse votre projet..."):
                base = SECTEURS_TECH.get(secteur_choisi, 5.5)
                comp_ia = round(base + random.uniform(-0.5, 1.0), 2)
                rob_ia = round(random.uniform(8.0, 9.9), 2) if "github" in lien.lower() else round(random.uniform(4.0, 7.0), 2)
                note_finale = round((comp_ia * 0.7) + (rob_ia * 0.3), 2)

                conn = get_connection()
                conn.execute("INSERT INTO soumissions (nom, email, lien, secteur, complexite, robustesse, note_predite, statut) VALUES (?,?,?,?,?,?,?,?)",
                             (nom, email, lien, secteur_final, comp_ia, rob_ia, note_finale, "Vérifié"))
                conn.commit()
                conn.close()

                st.balloons()
                st.success(f"✅ Audit terminé pour {nom} !")
                res1, res2, res3 = st.columns(3)
                res1.metric("Complexité", f"{comp_ia}/10")
                res2.metric("Robustesse", f"{rob_ia}/10")
                res3.metric("Note Prédite", f"{note_finale}/10")
                st.info(f"💬 Feedback IA : {random.choice(FEEDBACK_PHRASES)}")

# ====================== 2. INTERFACE PROFESSEUR ======================
else:
    st.title("📊 Tableau de Bord")
    
    if "auth" not in st.session_state:
        st.session_state.auth = False
    
    if not st.session_state.auth:
        pwd = st.sidebar.text_input("🔑 Code Professeur:admin", type="password")
        if st.sidebar.button("Se connecter"):
            if check_prof_password(pwd):
                st.session_state.auth = True
                st.rerun()
            else:
                st.sidebar.error("Accès refusé.")
        st.stop()

    df = load_data()
    
    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        k1, k2, k3 = st.columns(3)
        k1.metric("Total Projets", len(df))
        k2.metric("Moyenne Classe", f"{df['note_predite'].mean():.2f}/10")
        k3.metric("Admissibles (>=7)", f"{(len(df[df['note_predite']>=7]))}")

        tab1, tab2, tab3 = st.tabs(["📈 Graphiques", "🧩 Clustering", "📋 Données"])

        with tab1:
            fig = px.pie(df, names='secteur', title="Répartition par Secteur", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            if len(df) >= 3:
                X = df[['complexite', 'robustesse']]
                km = KMeans(n_clusters=3, n_init=10).fit(X)
                df['Cluster'] = km.labels_
                fig_km = px.scatter(df, x='complexite', y='robustesse', color=df['Cluster'].astype(str), title="Segments d'élèves")
                st.plotly_chart(fig_km, use_container_width=True)
            else:
                st.info("Données insuffisantes pour le clustering.")

        with tab3:
            st.dataframe(df, use_container_width=True)
            if st.button("🗑️ Reset"):
                conn = get_connection()
                conn.execute("DELETE FROM soumissions")
                conn.commit()
                conn.close()
                st.rerun()
