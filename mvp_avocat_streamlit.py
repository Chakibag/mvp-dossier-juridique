import streamlit as st
import pandas as pd

# Chargement des fichiers CSV
clients = pd.read_csv("clients.csv")
contacts = pd.read_csv("contacts.csv")
documents = pd.read_csv("documents.csv")
dossiers = pd.read_csv("dossiers.csv")
factures = pd.read_csv("factures.csv")
temps = pd.read_csv("temps.csv")

st.set_page_config(page_title="Vue 360° d'un dossier juridique", layout="wide")
st.title("📂 Vue 360° d'un dossier juridique")

# Sélection d'un dossier
dossier_selectionne = st.selectbox("Sélectionnez un dossier :", 
                                   dossiers["titre"] + " - " + dossiers["reference_interne"])

# Identifier l'ID du dossier sélectionné
dossier_id = dossiers[dossiers["titre"] + " - " + dossiers["reference_interne"] == dossier_selectionne]["dossier_id"].values[0]
dossier_info = dossiers[dossiers["dossier_id"] == dossier_id].iloc[0]

# Affichage des infos client
client_info = clients[clients["client_id"] == dossier_info["id_client"]].iloc[0]
st.subheader("👥 Informations client")
st.write(f"**Raison sociale :** {client_info['raison_sociale']}")
st.write(f"**Secteur :** {client_info['secteur']} | **Forme juridique :** {client_info['forme_juridique']}")

# Contacts liés au dossier
st.subheader("👤 Contacts impliqués")
contacts_dossier = contacts[contacts["id_dossier"] == dossier_id]
st.dataframe(contacts_dossier[["civilite", "nom", "prenom", "fonction", "email"]])

# Documents liés
st.subheader("📄 Documents associés")
documents_dossier = documents[documents["id_dossier"] == dossier_id]
st.dataframe(documents_dossier[["type_document", "titre", "date", "auteur"]])

# Temps passé
st.subheader("⏱️ Temps passé sur le dossier")
temps_dossier = temps[temps["id_dossier"] == dossier_id]
temps_resume = temps_dossier.groupby("nom_intervenant")["heures"].sum().reset_index()
st.dataframe(temps_resume.rename(columns={"nom_intervenant": "Intervenant", "heures": "Total heures"}))

# Factures
st.subheader("💳 Facturation")
factures_dossier = factures[factures["id_dossier"] == dossier_id]
st.dataframe(factures_dossier[["date_emission", "montant", "etat"]])

st.success("Vue du dossier générée avec succès.")
