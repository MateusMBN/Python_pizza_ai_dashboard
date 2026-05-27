import streamlit as st
import requests

# ======================================
# CONFIG
# ======================================

st.set_page_config(
    page_title="🍕 Pizza AI",
    page_icon="🍕",
    layout="centered"
)

# ======================================
# TÍTULO
# ======================================

st.title("🍕 Pizza AI Dashboard")

st.markdown(
    "Dashboard conectado com FastAPI 🤖"
)

# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("⚙️ Configurações")

diametro = st.sidebar.slider(
    "🍕 Diâmetro",
    20,
    50,
    35
)

ingredientes = st.sidebar.slider(
    "🧀 Ingredientes",
    1,
    10,
    5
)

borda = st.sidebar.selectbox(
    "🥖 Borda recheada?",
    [0, 1],
    format_func=lambda x: "Sim" if x == 1 else "Não"
)

# ======================================
# BOTÃO
# ======================================

if st.button("🤖 Fazer previsão"):

    # URL da API
    url = (
        f"http://127.0.0.1:8000/predict"
        f"?diametro={diametro}"
        f"&ingredientes={ingredientes}"
        f"&borda={borda}"
    )

    # Requisição
    resposta = requests.get(url)

    # JSON
    dados = resposta.json()

    # Resultado
    preco = dados["preco_previsto"]

    st.success(
        f"🍕 Preço previsto: R$ {preco}"
    )

    st.balloons()