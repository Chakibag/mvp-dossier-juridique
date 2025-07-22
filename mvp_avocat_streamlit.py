import streamlit as st
import pandas as pd
from pathlib import Path

# --- Chargement des fichiers CSV ---
@st.cache_data
def load_data():
    base = Path(__file__).parent
    dossiers  = pd.read_csv(base / "dossiers.csv",  dtype={"id": str})
    clients   = pd.read_csv(base / "clients.csv",   dtype={"client_id": str})
    contacts  = pd.read_csv(base / "contacts.csv",  dtype={"contact_id": str, "client_id": str})
    documents = pd.read_csv(base / "documents.csv", dtype={"document_id": str, "id_dossier": str})
    factures  = pd.read_csv(base / "factures.csv",  dtype={"facture_id": str, "id_dossier": str})
    temps     = pd.read_csv(base / "temps.csv",     dtype={"temps_id": str,   "id_dossier": str})
    return dossiers, clients, contacts, documents, factures, temps

dossiers, clients, contacts, documents, factures, temps = load_data()

def main():
    st.set_page_config(page_title="Vue 360° d'un dossier juridique", layout="wide")
    st.title("🔍 Vue 360° d'un dossier juridique")

    # --- Sélection du dossier ---
    choix_dossier = st.sidebar.selectbox(
        "Choisissez un dossier",
        options = dossiers["id"].tolist(),
        format_func = lambda x: dossiers.loc[dossiers["id"] == x, "reference_interne"].iat[0]
    )

    # On récupère le dossier complet
    dossier = dossiers.loc[dossiers["id"] == choix_dossier]
    if dossier.empty:
        st.error("Dossier introuvable.")
        return

    # --- Informations générales du dossier ---
    st.subheader("📂 Informations générales du dossier")
    st.dataframe(dossier, use_container_width=True)

    # --- Client associé ---
    id_client = dossier["id_client"].iat[0]
    client = clients.loc[clients["client_id"] == id_client]
    st.subheader("👤 Client associé")
    st.dataframe(client, use_container_width=True)

    # --- Contacts du client ---
    st.subheader("📇 Contacts du client")
    ctcs = contacts.loc[contacts["client_id"] == id_client]
    st.dataframe(ctcs, use_container_width=True)

    # --- Documents du dossier ---
    st.subheader("📄 Documents du dossier")
    docs = documents.loc[documents["id_dossier"] == choix_dossier]
    if docs.empty:
        st.info("Aucun document trouvé pour ce dossier.")
    else:
        st.dataframe(docs, use_container_width=True)

    # --- Factures du dossier ---
    st.subheader("💶 Factures du dossier")
    facs = factures.loc[factures["id_dossier"] == choix_dossier]
    if facs.empty:
        st.info("Aucune facture trouvée pour ce dossier.")
    else:
        st.dataframe(facs, use_container_width=True)

    # --- Temps passés sur le dossier ---
    st.subheader("⏱️ Temps passés sur le dossier")
    tps = temps.loc[temps["id_dossier"] == choix_dossier]
    if tps.empty:
        st.info("Aucun relevé de temps trouvé pour ce dossier.")
    else:
        st.dataframe(tps, use_container_width=True)

if __name__ == "__main__":
    main()
