import streamlit as st
import pandas as pd

# Chargement des fichiers CSV
clients = pd.read_csv("clients.csv")
contacts = pd.read_csv("contacts.csv")
documents = pd.read_csv("documents.csv")
dossiers = pd.read_csv("dossiers.csv")
factures = pd.read_csv("factures.csv")
temps = pd.read_csv("temps.csv")

st.set_page_config(page_title="Vue 360 d'un dossier juridique", layout="wide")
st.title("Vue 360 d'un dossier juridique")

# Sélection d'un dossier
dossier_selectionne = st.selectbox("Sélectionnez un dossier :", 
                                   dossiers["titre"] + " - " + dossiers["reference_interne"])

# Identifier l'ID du dossier sélectionné
dossier_id = dossiers[dossiers["titre"] + " - " + dossiers["reference_interne"] == dossier_selectionne]["dossier_id"].values[0]
dossier_info = dossiers[dossiers["dossier_id"] == dossier_id].iloc[0]

# Affichage des infos client
client_info = clients[clients["client_id"] == dossier_info["id_client"]].iloc[0]
st.subheader("Informations client")
st.write(f"**Raison sociale :** {client_info.get('raison_sociale', 'Non renseigné')}")
st.write(f"**Secteur :** {client_info.get('secteur', 'Non renseigné')} | **Forme juridique :** {client_info.get('forme_juridique', 'Non renseigné')}")

# Contacts liés au dossier
st.subheader("Contacts impliqués")
contacts_dossier = contacts[contacts["id_dossier"] == dossier_id]
if not contacts_dossier.empty:
    st.dataframe(contacts_dossier[["civilite", "nom", "prenom", "fonction", "email"]])
else:
    st.info("Aucun contact trouvé pour ce dossier.")

# Documents liés
st.subheader("Documents associés")
documents_dossier = documents[documents["id_dossier"] == dossier_id]
if not documents_dossier.empty:
    st.dataframe(documents_dossier[["type_document", "titre", "date", "auteur"]])
else:
    st.info("Aucun document associé à ce dossier.")

# Temps passé
st.subheader("Temps passé sur le dossier")
temps_dossier = temps[temps["id_dossier"] == dossier_id]
if not temps_dossier.empty:
    temps_resume = temps_dossier.groupby("nom_intervenant")["heures"].sum().reset_index()
    st.dataframe(temps_resume.rename(columns={"nom_intervenant": "Intervenant", "heures": "Total heures"}))
else:
    st.info("Aucune donnée de temps trouvée.")

# Factures
st.subheader("Facturation")
factures_dossier = factures[factures["id_dossier"] == dossier_id]
if not factures_dossier.empty:
    st.dataframe(factures_dossier[["date_emission", "montant", "etat"]])
else:
    st.info("Aucune facture disponible pour ce dossier.")

st.success("Vue du dossier générée avec succès.")
