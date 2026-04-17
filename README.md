💎 ADN-ROLL-INSIGHT v2.1
Système Intelligent d'Audit et d'Analyse de Projets (INF 232 - EC2)

📌 Présentation du Projet
ADN-ROLL-INSIGHT est une application web développée avec Streamlit permettant d'automatiser la collecte et l'évaluation de projets étudiants via des algorithmes de Machine Learning.

L'outil se divise en deux volets :

Interface Étudiant : Soumission sécurisée et audit instantané de la complexité et de la robustesse du code par une IA.

Interface Professeur : Tableau de bord analytique incluant du clustering (segmentation de niveau) et de la régression (prédiction de performance).

🚀 Fonctionnalités Clés
👨‍🎓 Côté Étudiant
Audit IA en Temps Réel : Calcul automatique d'un score de complexité basé sur le secteur d'activité (incluant l'Agriculture, l'IA, la Cybersécurité, etc.).

Analyse de Robustesse : Détection automatique des plateformes de versioning (GitHub/GitLab) pour valoriser la qualité du déploiement.

Feedback Dynamique : Retour instantané généré par l'IA sur la viabilité du projet.

👨‍🏫 Côté Professeur (Accès Sécurisé)
Analyse Descriptive : Visualisation interactive de la répartition des domaines via Plotly.

Machine Learning Supervisé : Régression linéaire multiple pour corréler la complexité technique et la note finale.

Clustering K-Means : Segmentation automatique des étudiants en 3 profils distincts (Experts, Intermédiaires, Débutants).

Gestion des Données : Exportation des résultats en CSV et gestion de la base de données SQLite.

🛠 Installation & Configuration
Le projet utilise une version portable de Python pour garantir la stabilité de l'environnement.

1. Prérequis
Assurez-vous que les bibliothèques suivantes sont présentes (voir requirements.txt) :

streamlit, pandas, plotly, scikit-learn, statsmodels.

2. Lancement de l'application
Ouvrez un terminal dans le dossier du projet et exécutez la commande suivante :

PowerShell
.\logiciel_python\python.exe -m streamlit run app.py
📊 Architecture Technique
Backend : Python 3.x & SQLite3.

Frontend : Streamlit (UI/UX Custom CSS).

Moteur Data : * Scikit-Learn : KMeans & LinearRegression.

Plotly : Graphiques dynamiques et interactifs.

Statsmodels : Calcul des lignes de tendance (OLS).

🔐 Sécurité
L'accès aux données sensibles de l'interface Professeur est protégé par un hachage SHA-256.

Code d'accès par défaut : admin

📁 Structure du Dossier
app.py : Code source principal de l'application.

adn_insight.db : Base de données locale SQLite.

logiciel_python/ : Environnement Python portable.

requirements.txt : Liste des dépendances logicielles.

Développé dans le cadre de l'UE INF 232 — EC2. © 2026 - Système d'Audit ADN-ROLL-INSIGHT

