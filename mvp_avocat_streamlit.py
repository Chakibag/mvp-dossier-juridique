# mvp_avocat_streamlit.py

import pandas as pd
import streamlit as st

# --- Chemins vers vos CSV à la racine du dépôt ---
CLIENTS_CSV   = "clients.csv"
CONTACTS_CSV  = "contacts.csv"
DOCUMENTS_CSV = "documents.csv"
DOSSIERS_CSV  = "dossiers.csv"
FACTURES_CSV  = "factures.csv"
TEMPS_CSV     = "temps.csv"


@st.cache_data
def load_data():
    """Charge et retourne tous les jeux de données."""
    clients   = pd.read_csv(CLIENTS_CSV,   dtype=str)
    contacts  = pd.read_csv(CONTACTS_CSV,  dtype=str)
    dossiers  = pd.read_csv(DOSSIERS_CSV,  dtype=str)
    documents = pd.read_csv(DOCUMENTS_CSV, dtype=str)
    factures  = pd.read_csv(FACTURES_CSV,  dtype=str)
    temps     = pd.read_csv(TEMPS_CSV,     dtype=str)
    return clients, contacts, dossiers, documents, factures, temps


def main():
    st.set_page_config(page_title="360° Dossier juridique", layout="wide")
    st.title("🔍 Vue 360° d'un dossier juridique")

    # 1️⃣ Chargement des données
    clients, contacts, dossiers, documents, factures, temps = load_data()

    # 2️⃣ Sélection du dossier
    dossier_id = st.selectbox(
        "Choisissez un dossier",
        options=dossiers["dossier_id"].tolist()
    )

    # 3️⃣ Filtrer les informations du dossier sélectionné
    dossier = dossiers.loc[dossiers["dossier_id"] == dossier_id].squeeze()

    # 4️⃣ Affichage des infos client
    client = clients.loc[clients["client_id"] == dossier["client_id"]].squeeze()
    with st.expander("👤 Informations client", expanded=True):
        st.write(f"**Raison sociale :** {client['raison_sociale']}")
        st.write(f"**Secteur :** {client['secteur']}")
        st.write(f"**Forme juridique :** {client['forme_juridique']}")

    # 5️⃣ Affichage du résumé du dossier
    with st.expander("📁 Informations dossier", expanded=True):
        st.write(f"**Libellé du dossier :** {dossier['libelle_dossier']}")
        st.write(f"**Date d'ouverture :** {dossier.get('date_ouverture', 'N/A')}")
        st.write(f"**État :** {dossier.get('etat', 'N/A')}")

    # 6️⃣ Co
