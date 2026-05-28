from fastapi import FastAPI
import pandas as pd
import joblib

# ======================================
# APP
# ======================================

app = FastAPI()

# ======================================
# MODELO
# ======================================

modelo = joblib.load(
    "modelo_pizza.pkl"
)

# ======================================
# HOME
# ======================================

@app.get("/")
def home():

    return {
        "mensagem": "🍕 Pizza AI API"
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

    # ======================================
    # FEATURES EXTRAS
    # ======================================

    nova_pizza["complexidade"] = (
        nova_pizza["diametro"] *
        nova_pizza["ingredientes"]
    )

    nova_pizza["premium"] = (
        (
            nova_pizza["diametro"] >= 30
        ) &
        (
            nova_pizza["borda"] == 1
        )
    ).astype(int)

    # ======================================
    # PREVISÃO
    # ======================================

    dados_para_previsao = nova_pizza[["diametro", "ingredientes", "borda"]]
    preco = modelo.predict(
        dados_para_previsao
    )[0]

    return {
        "preco_previsto": round(
            float(preco),
            2
        )
    }