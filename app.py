import pandas as pd
import plotly.express as px

# Charger le CSV local (dans le même dossier que app.py)
df = pd.read_csv("ventes.csv")

# Nettoyage : retire la ligne "produit / prix / qte / region" si elle a été importée comme une ligne
df = df[df["produit"].notna()]
df = df[df["produit"] != "produit"]
df = df[df["region"].notna()]
df = df[df["region"] != "region"]

# Conversion en numérique
df["prix"] = pd.to_numeric(df["prix"], errors="coerce")
df["qte"] = pd.to_numeric(df["qte"], errors="coerce")

# Calcul du CA
df["chiffre_affaires"] = df["prix"] * df["qte"]

# 1) Ventes par produit (quantité)
ventes_par_produit = (
    df.groupby("produit", as_index=False)["qte"]
    .sum()
    .sort_values("qte", ascending=False)
)

fig1 = px.bar(
    ventes_par_produit,
    x="produit",
    y="qte",
    title="Ventes par produit (quantité totale)",
    labels={"qte": "Quantité vendue", "produit": "Produit"}
)
fig1.write_html("ventes_par_produit.html")

# 2) Chiffre d'affaires par produit
ca_par_produit = (
    df.groupby("produit", as_index=False)["chiffre_affaires"]
    .sum()
    .sort_values("chiffre_affaires", ascending=False)
)

fig2 = px.bar(
    ca_par_produit,
    x="produit",
    y="chiffre_affaires",
    title="Chiffre d'affaires par produit",
    labels={"chiffre_affaires": "Chiffre d'affaires (€)", "produit": "Produit"}
)
fig2.write_html("ca_par_produit.html")

print("✅ OK : ventes_par_produit.html et ca_par_produit.html générés")

# 3) Chiffre d'affaires par région

ca_par_region = df.groupby("region")["chiffre_affaires"].sum().reset_index()

fig_region = px.bar(
    ca_par_region,
    x="region",
    y="chiffre_affaires",
    title="Chiffre d'affaires par région"
)

fig_region.write_html("ca_par_region.html")