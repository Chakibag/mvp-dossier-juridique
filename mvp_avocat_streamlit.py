import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    # On suppose que les CSV sont dans le même dossier que ce script
    base = os.getcwd()
    clients   = pd.read_csv(os.path.join(base, "clients.csv"))
    contacts  = pd.read_csv(os.path.join(base, "contacts.csv"))
    dossiers  = pd.read_csv(os.path.join(base, "dossiers.csv"))
    documents = pd.read_csv(os.path.join(base, "documents.csv"))
    factures  = pd.read_csv(os.path.join(base, "factures.csv"))
    temps     = pd.read_csv(os.path.join(base, "temps.csv"))

    # Harmonisation des noms de colonnes pour les clés
    # Dans clients.csv la clé s'appelle "client_id"
    clients = clients.rename(columns={"client_id": "id_client"})
    # Dans dossiers.csv la clé client est "id_client" et la pk dossier est "dossier_id"
    # dans contacts.csv la fk client est "id_client"
    # dans documents/factures/temps la fk dossier est "id_dossier"
    # on les laisse tels quels

    return clients, contacts, dossiers, documents, factures, temps


def main():
    st.set_page_config(page_title="360° d'un dossier", layout="wide")
    st.title("🔍 Vue 360° d'un dossier juridique")

    clients, contacts, dossiers, documents, factures, temps = load_data()

    # Choix du dossier dans la sidebar
    dossier_ids = dossiers["dossier_id"].astype(str).tolist()
    dossier_sel = st.sidebar.selectbox("Choisissez un dossier", dossier_ids)

    # Récupérer la ligne du dossier
    # -- on convertit en str car selectbox renvoie du texte
    dossier = dossiers.loc[dossiers["dossier_id"].astype(str) == dossier_sel]
    if dossier.empty:
        st.error(f"Le dossier `{dossier_sel}` n'existe pas.")
        return
    # Comme c'est un DataFrame à 1 ligne, on squeeze en Series
    dossier = dossier.squeeze()

    # 1) Afficher les infos du dossier
    st.subheader("📁 Informations générales du dossier")
    st.write(dossier.to_frame().T)

    # 2) Le client lié
    st.subheader("👤 Client associé")
    id_client = dossier["id_client"]
    client = clients.loc[clients["id_client"] == id_client]
    if client.empty:
        st.warning("Aucun client trouvé pour ce dossier.")
    else:
        st.write(client.squeeze().to_frame().T)

    # 3) Les contacts (avocat(s), etc.) du client
    st.subheader("📇 Contacts du client")
    contacts_client = contacts.loc[contacts["id_client"] == id_client]
    if contacts_client.empty:
        st.info("Pas de contacts enregistrés pour ce client.")
    else:
        st.dataframe(contacts_client)

    # 4) Les documents attachés au dossier
    st.subheader("📄 Documents du dossier")
    docs = documents.loc[documents["dossier_id"] == int(dossier_sel)]
    if docs.empty:
        st.info("Pas de documents pour ce dossier.")
    else:
        st.dataframe(docs)

    # 5) Les factures associées
    st.subheader("💶 Factures liées")
    fac = factures.loc[factures["id_dossier"] == int(dossier_sel)]
    if fac.empty:
        st.info("Pas de factures pour ce dossier.")
    else:
        st.dataframe(fac)

    # 6) Les temps passés (suivi temps)
    st.subheader("⏱️ Temps passés sur le dossier")
    tps = temps.loc[temps["id_dossier"] == int(dossier_sel)]
    if tps.empty:
        st.info("Aucun enregistrement de temps pour ce dossier.")
    else:
        st.dataframe(tps)

if __name__ == "__main__":
    main()
