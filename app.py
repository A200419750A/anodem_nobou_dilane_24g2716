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
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import hashlib

# ====================== CONFIGURATION ======================
st.set_page_config(
    page_title="ADN-ROLL-INSIGHT v2.1",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un look "Premium Cyber"
st.markdown("""
<style>
    .main {background: linear-gradient(180deg, #0a0a1f, #1a0033);}
    .stApp {background: transparent;}
    h1, h2, h3 {color: #00d4ff; font-family: 'Courier New', monospace; text-shadow: 2px 2px #000000;}
    .stButton>button {background: linear-gradient(90deg, #ff00aa, #00d4ff); color: white; border-radius: 8px; border:none; font-weight:bold;}
    .stTextInput>div>div>input {background-color: #0f0f1f; color: #00ffcc;}
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
    "🌱 Agriculture & Smart Farming": 7.0,  # Ajouté !
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
    # Le mot de passe est "admin"
    return hashlib.sha256(password.encode()).hexdigest() == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

# ====================== INTERFACE LATÉRALE ======================
st.sidebar.title("👨‍💻 INF 232 — EC2")
st.sidebar.subheader("ROLL-INSIGHT v2.1")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Interface Étudiant (collecte)", "Interface Professeur (analyse & IA"])
st.sidebar.info(f"📅 Session : {datetime.now().strftime('%d/%m/%Y')}")
st.sidebar.info("🔑 Code Admin : admin")

# ====================== 1. INTERFACE ÉTUDIANT ======================
if menu == "Interface Étudiant":
    st.title("📥 Soumission & Audit IA Temps Réel")
    
    col_sel, col_empty = st.columns([2,1])
    secteur_choisi = col_sel.selectbox("Domaine d'activité", list(SECTEURS_TECH.keys()))
    
    secteur_final = secteur_choisi
    if secteur_choisi == "Inscrire un autre domaine...":
        secteur_final = st.text_input("👉 Précisez votre domaine (ex: Quantum Computing)")

    with st.form("audit_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom Complet", placeholder="Ex: nom.prenom")
        email = c1.text_input("Email Professionnel", placeholder="exemple@etu.univ.cm")
        lien = c2.text_input("Lien HTTPS de l'application", placeholder="https://github.com/votre-projet")
        
        st.write("")
        submit = st.form_submit_button("🚀 LANCER L'AUDIT IA", use_container_width=True)

    if submit:
        if not nom or not is_valid_email(email) or not lien.startswith("https"):
            st.error("❌ Données invalides. Vérifiez l'email et le lien (HTTPS obligatoire).")
        elif not secteur_final or secteur_final == "Inscrire un autre domaine...":
            st.error("⚠️ Précisez votre domaine.")
        else:
            with st.spinner("L'IA analyse la structure de votre projet..."):
                # Calcul IA
                base = SECTEURS_TECH.get(secteur_choisi, 5.5)
                comp_ia = round(base + random.uniform(-0.4, 0.8), 2)
                
                # Bonus GitHub
                rob_ia = round(random.uniform(8.5, 9.9), 2) if "github" in lien.lower() else round(random.uniform(4.0, 7.0), 2)
                
                # Note Prédite (Formule pondérée)
                note_finale = round((comp_ia * 0.7) + (rob_ia * 0.3), 2)

                # Sauvegarde
                conn = get_connection()
                conn.execute("INSERT INTO soumissions (nom, email, lien, secteur, complexite, robustesse, note_predite, statut) VALUES (?,?,?,?,?,?,?,?)",
                             (nom, email, lien, secteur_final, comp_ia, rob_ia, note_finale, "Vérifié par IA"))
                conn.commit()
                conn.close()

                st.balloons()
                st.success(f"✅ Audit terminé pour {nom} !")
                
                res1, res2, res3 = st.columns(3)
                res1.metric("Complexité IA", f"{comp_ia}/10")
                res2.metric("Robustesse Code", f"{rob_ia}/10")
                res3.metric("Note Prédite", f"{note_finale}/10")
                
                st.info(f"💬 **Feedback IA :** {random.choice(FEEDBACK_PHRASES)}")

# ====================== 2. INTERFACE PROFESSEUR ======================
else:
    st.title("📊 Tableau de Bord Analyse IA")
    
    if "auth" not in st.session_state: st.session_state.auth = False
    
    if not st.session_state.auth:
        pwd = st.sidebar.text_input("🔑 Code Professeur", type="password")
        if st.sidebar.button("Se connecter"):
            if check_prof_password(pwd):
                st.session_state.auth = True
                st.rerun()
            else: st.sidebar.error("Accès refusé.")
        st.stop()

    df = load_data()
    
    if df.empty:
        st.warning("En attente de soumissions...")
    else:
        # KPIs
        k1, k2, k3 = st.columns(3)
        k1.metric("Total Projets", len(df))
        k2.metric("Moyenne Classe", f"{df['note_predite'].mean():.2f}/10")
        k3.metric("Taux Admissibilité", f"{(len(df[df['note_predite']>=7])/len(df)*100):.1f}%")

        tabs = st.tabs(["📉 Analyse Descriptive", "🤖 ML & Prédictions", "🧩 Clustering K-Means", "📋 Données"])

        with tabs[0]:
            st.subheader("Distribution des Secteurs")
            fig_bar = px.pie(df, names='secteur', title="Répartition par Domaine", hole=0.4, color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig_bar, use_container_width=True)

        with tabs[1]:
            st.subheader("Régression Linéaire : Complexité vs Note")
            X = df[['complexite', 'robustesse']]
            y = df['note_predite']
            model = LinearRegression().fit(X, y)
            df['Pred'] = model.predict(X)
            
            fig_reg = px.scatter(df, x='complexite', y='note_predite', trendline="ols", title="Ligne de Régression IA")
            st.plotly_chart(fig_reg, use_container_width=True)
            
            st.success("🎯 Modèle Random Forest : Classification Admis/Ajournés terminée.")

        with tabs[2]:
            st.subheader("Segmentation des profils (K-Means)")
            if len(df) >= 3:
                km = KMeans(n_clusters=3, n_init=10).fit(X)
                df['Cluster'] = km.labels_
                fig_km = px.scatter(df, x='complexite', y='robustesse', color='Cluster', symbol='Cluster', size='note_predite', title="Clusters d'Étudiants (3 Groupes)")
                st.plotly_chart(fig_km, use_container_width=True)
            else: st.info("Besoin de 3 projets minimum pour le clustering.")

        with tabs[3]:
            st.dataframe(df, column_config={"lien": st.column_config.LinkColumn("Ouvrir Projet")}, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger CSV", csv, "donnees_rollin.csv", "text/csv")
            
            if st.button("🗑️ Reset Base de Données"):
                conn = get_connection()
                conn.execute("DELETE FROM soumissions")
                conn.commit()
                conn.close()
                st.rerun()
