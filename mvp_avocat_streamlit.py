import streamlit as st
import pandas as pd
from datetime import datetime

# — Chemins vers vos CSV (modifiez si besoin) —
CLIENTS_CSV   = "/mnt/data/clients.csv"
CONTACTS_CSV  = "/mnt/data/contacts.csv"
DOSSIERS_CSV  = "/mnt/data/dossiers.csv"
DOCUMENTS_CSV = "/mnt/data/documents.csv"
FACTURES_CSV  = "/mnt/data/factures.csv"
TEMPS_CSV     = "/mnt/data/temps.csv"

@st.cache_data
def load_data():
    clients   = pd.read_csv(CLIENTS_CSV)
    contacts  = pd.read_csv(CONTACTS_CSV)
    dossiers  = pd.read_csv(DOSSIERS_CSV)
    docs      = pd.read_csv(DOCUMENTS_CSV)
    factures  = pd.read_csv(FACTURES_CSV)
    temps     = pd.read_csv(TEMPS_CSV)
    return clients, contacts, dossiers, docs, factures, temps

clients, contacts, dossiers, docs, factures, temps = load_data()

st.set_page_config(page_title="Vue 360° Dossier juridique", layout="wide")
st.title("Vue 360° d'un dossier juridique")

# --- Sélecteur de dossier ---
# On affiche dans le selectbox la colonne 'reference_interne' + 'titre'
dossiers["label"] = dossiers["reference_interne"] + " – " + dossiers["titre"]
choix = st.selectbox("Choisissez un dossier", dossiers["label"].tolist())

# Réccupérer l'ID du dossier choisi
dossier_id = dossiers.loc[dossiers["label"] == choix, "dossier_id"].iloc[0]
id_client  = dossiers.loc[dossiers["dossier_id"] == dossier_id, "id_client"].iloc[0]

# --- Infos client ---
client_info = clients.loc[clients["id_client"] == id_client].squeeze()
st.header("👤 Informations client")
st.write(f"**Raison sociale :** {client_info.get('raison_sociale', '–')}")
st.write(f"**Secteur :** {client_info.get('secteur', '–')}")
st.write(f"**Forme juridique :** {client_info.get('forme_juridique', '–')}")

# --- Contacts impliqués (via le client) ---
st.header("📇 Contacts impliqués")
contacts_dossier = contacts.loc[contacts["id_client"] == id_client]
if not contacts_dossier.empty:
    st.table(
        contacts_dossier[["civilite", "nom", "prenom", "fonction", "email", "telephone"]]
        .rename(columns={
            "civilite": "Civilité", "nom": "Nom", "prenom": "Prénom",
            "fonction": "Fonction", "email": "Email", "telephone": "Tél."
        })
    )
else:
    st.write("_Aucun contact enregistré pour ce client._")

# --- Documents associés au dossier ---
st.header("📄 Documents du dossier")
docs_dossier = docs.loc[docs["dossier_id"] == dossier_id]
if not docs_dossier.empty:
    st.table(
        docs_dossier[["type_document", "nom_fichier", "date_upload"]]
        .rename(columns={
            "type_document": "Type", "nom_fichier": "Fichier", "date_upload": "Date d'envoi"
        })
    )
else:
    st.write("_Aucun document uploadé pour ce dossier._")

# --- Factures ---
st.header("💰 Factures liées")
factures_dossier = factures.loc[factures["dossier_id"] == dossier_id]
if not factures_dossier.empty:
    st.table(
        factures_dossier[["numero_facture", "date_facture", "montant", "statut"]]
        .rename(columns={
            "numero_facture": "N° Facture", "date_facture": "Date",
            "montant": "Montant (€)", "statut": "Statut"
        })
    )
else:
    st.write("_Pas de factures pour ce dossier._")

# --- Feuille de temps ---
st.header("⏱️ Temps passés")
temps_dossier = temps.loc[temps["dossier_id"] == dossier_id]
if not temps_dossier.empty:
    # On additionne les durées par utilisateur
    summary = (
        temps_dossier
        .groupby(["utilisateur"])
        .agg(total_minutes=("duree_minutes", "sum"))
        .reset_index()
    )
    # Affichage simple
    st.table(summary.rename(columns={
        "utilisateur": "Utilisateur", "total_minutes": "Temps total (min)"
    }))
else:
    st.write("_Aucun enregistrement de temps pour ce dossier._")

# --- Statut du dossier et résumé ---
st.header("🔎 Résumé du dossier")
d = dossiers.loc[dossiers["dossier_id"] == dossier_id].squeeze()
col1, col2, col3 = st.columns(3)
col1.metric("État", d.get("etat", "–"))
col2.metric("Ouverture", d.get("date_ouverture", "–"))
col3.metric("Clôture", d.get("date_cloture", "–"))

# Optionnel : calcul de la durée depuis l'ouverture
if pd.notna(d.get("date_ouverture")):
    dt0 = pd.to_datetime(d["date_ouverture"])
    delta = datetime.today() - dt0
    st.write(f"Ce dossier a été ouvert il y a {delta.days} jours.")

