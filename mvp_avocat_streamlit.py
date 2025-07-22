# mvp_avocat_streamlit.py

import streamlit as st
import pandas as pd
from pathlib import Path

# Calculer automatiquement le dossier où réside ce script
BASE_DIR = Path(__file__).parent

@st.cache_data
def load_data():
    clients   = pd.read_csv(BASE_DIR / "clients.csv",   dtype=str)
    contacts  = pd.read_csv(BASE_DIR / "contacts.csv",  dtype=str)
    dossiers  = pd.read_csv(BASE_DIR / "dossiers.csv",  dtype=str)
    docs      = pd.read_csv(BASE_DIR / "documents.csv", dtype=str)
    factures  = pd.read_csv(BASE_DIR / "factures.csv",  dtype=str)
    temps     = pd.read_csv(BASE_DIR / "temps.csv",     dtype=str)
    return clients, contacts, dossiers, docs, factures, temps

def main():
    st.title("👩‍⚖️ Vue 360° d'un dossier juridique")

    # Charge les données
    clients, contacts, dossiers, docs, factures, temps = load_data()

    # --- Suite de votre app ---
    # Sélection du dossier
    dossier_id = st.selectbox(
        "Sélectionnez un dossier",
        options=dossiers["id_dossier"].tolist()
    )

    # Récupérer les infos client
    dossier = dossiers.loc[dossiers["id_dossier"] == dossier_id].iloc[0]
    client_id = dossier["id_client"]
    client_info = clients.loc[clients["id_client"] == client_id].iloc[0]

    st.subheader("👤 Informations client")
    st.write(f"**Raison sociale  :** {client_info['raison_sociale']}")
    st.write(f"**Secteur         :** {client_info['secteur']}")
    st.write(f"**Forme juridique :** {client_info['forme_juridique']}")

    # Récupérer et afficher les contacts
    st.subheader("📇 Contacts impliqués")
    sheet = contacts.loc[contacts["id_dossier"] == dossier_id]
    st.table(sheet[["nom","prenom","fonction","email"]])

    # ... etc. pour les autres tableaux

if __name__ == "__main__":
    main()
