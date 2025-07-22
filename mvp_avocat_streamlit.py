import os
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------
# Debug sidebar : voir les fichiers dispo
# -------------------------------------------------------------------
st.sidebar.header("🔍 Debug : fichiers existants")
for f in os.listdir("."):
    st.sidebar.write(f)

# -------------------------------------------------------------------
# Les chemins de vos CSV
# -------------------------------------------------------------------
FILES = {
    "clients":   "clients.csv",
    "contacts":  "contacts.csv",
    "dossiers":  "dossiers.csv",
    "documents": "documents.csv",
    "factures":  "factures.csv",
    "temps":     "temps.csv",
}

# -------------------------------------------------------------------
# Chargement avec vérif d’existence
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    dfs = {}
    for name, path in FILES.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier '{path}' est introuvable !")
        dfs[name] = pd.read_csv(path, dtype=str)
    return dfs

# -------------------------------------------------------------------
#  Main
# -------------------------------------------------------------------
def main():
    st.set_page_config(page_title="360° Dossier juridique", layout="wide")
    st.title("🔍 Vue 360° d'un dossier juridique")

    # 1) Chargement
    try:
        dfs = load_data()
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {e}")
        st.stop()

    clients   = dfs["clients"]
    contacts  = dfs["contacts"]
    dossiers  = dfs["dossiers"]
    documents = dfs["documents"]
    factures  = dfs["factures"]
    temps     = dfs["temps"]

    # 2) Vérifier les colonnes principales
    required = {
        "clients":   "id_client",
        "dossiers":  "id_dossier",
    }
    for key, col in required.items():
        if col not in dfs[key].columns:
            st.error(f"❌ Colonne '{col}' absente de {key}.csv (colonnes dispo : {dfs[key].columns.tolist()})")
            st.stop()

    # 3) Choix du dossier
    dossier_id = st.selectbox(
        "Choisissez un dossier",
        options=dossiers["id_dossier"].tolist()
    )

    # 4) Récupérer la ligne dossier
    sel = dossiers[dossiers["id_dossier"] == dossier_id]
    if sel.empty:
        st.warning("⚠️ Aucun dossier trouvé pour cet ID.")
        st.stop()
    dossier = sel.iloc[0]

    # 5) Afficher info client
    client_col = "id_client"
    if client_col not in dossier.index:
        st.error(f"❌ Le dossier n'a pas de colonne '{client_col}'.")
        st.stop()

    client_sel = clients[clients[client_col] == dossier[client_col]]
    if client_sel.empty:
        st.warning("⚠️ Pas de client lié à ce dossier.")
    else:
        client = client_sel.iloc[0]
        with st.expander("👤 Infos client", True):
            # Adaptez les noms de colonnes réelles
            for field in ["raison_sociale", "secteur", "forme_juridique"]:
                if field in client.index:
                    st.write(f"**{field.replace('_',' ').title()} :** {client[field]}")
                else:
                    st.write(f"**{field} :** (colonne absente)")

    # 6) Infos dossier
    with st.expander("📁 Infos dossier", True):
        for field in ["libelle_dossier", "date_ouverture", "etat"]:
            val = dossier[field] if field in dossier.index else "–"
            st.write(f"**{field.replace('_',' ').title()} :** {val}")

    # 7) Contacts
    with st.expander("👥 Contacts impliqués", False):
        if "id_dossier" not in contacts.columns:
            st.error("❌ Pas de colonne 'id_dossier' dans contacts.csv")
        else:
            st.dataframe(contacts[contacts["id_dossier"] == dossier_id])

    # 8) Documents
    with st.expander("📄 Documents", False):
        if "id_dossier" not in documents.columns:
            st.error("❌ Pas de colonne 'id_dossier' dans documents.csv")
        else:
            st.dataframe(documents[documents["id_dossier"] == dossier_id])

    # 9) Factures
    with st.expander("💶 Factures", False):
        if "id_dossier" not in factures.columns:
            st.error("❌ Pas de colonne 'id_dossier' dans factures.csv")
        else:
            st.dataframe(factures[factures["id_dossier"] == dossier_id])

    # 10) Temps passé
    with st.expander("⏱️ Temps passé", False):
        if "id_dossier" not in temps.columns:
            st.error("❌ Pas de colonne 'id_dossier' dans temps.csv")
        else:
            st.dataframe(temps[temps["id_dossier"] == dossier_id])

if __name__ == "__main__":
    main()
