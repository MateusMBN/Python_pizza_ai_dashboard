from fastapi import FastAPI
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

# ======================================
# APP
# ======================================

app = FastAPI()

# ======================================
# DADOS
# ======================================

df = pd.read_csv("pizzas.csv")

x = df[[
    "diametro",
    "ingredientes",
    "borda"
]]

y = df["preco"]

# ======================================
# MODELO
# ======================================

modelo = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

modelo.fit(x, y)

# ======================================
# ROTA PRINCIPAL
# ======================================

@app.get("/")
def home():

    return {
        "mensagem": "🍕 Pizza AI API funcionando!"
    }

# ======================================
# PREVISÃO
# ======================================

@app.get("/predict")
def predict(
    diametro: int,
    ingredientes: int,
    borda: int
):

    nova_pizza = pd.DataFrame({
        "diametro": [diametro],
        "ingredientes": [ingredientes],
        "borda": [borda]
    })

    preco = modelo.predict(nova_pizza)[0]

    return {
        "preco_previsto": round(float(preco), 2)
    }