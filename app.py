import streamlit as st
import requests
import pandas as pd

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================

st.set_page_config(
    page_title="Pizza AI",
    page_icon="🍕",
    layout="centered"
)

# ======================================
# HISTÓRICO
# ======================================

if "historico" not in st.session_state:
    st.session_state.historico = []

# ======================================
# CABEÇALHO
# ======================================

st.title("🍕 Pizza AI")

st.markdown("""
### Descubra o preço estimado da sua pizza

Nossa Inteligência Artificial analisa as características da pizza e estima um valor com base nos dados utilizados no treinamento do modelo.

Preencha as informações abaixo e clique em **Calcular Preço**.
""")

st.info(
    "💡 Exemplo: Pizza de 35 cm, 5 ingredientes e borda recheada."
)

st.divider()

# ======================================
# FORMULÁRIO
# ======================================

st.subheader("📝 Monte sua pizza")

col1, col2 = st.columns(2)

with col1:
    diametro = st.slider(
        "📏 Tamanho da pizza (cm)",
        min_value=20,
        max_value=50,
        value=35
    )

with col2:
    ingredientes = st.slider(
        "🧀 Quantidade de ingredientes",
        min_value=1,
        max_value=10,
        value=5
    )

borda = st.radio(
    "🥖 Borda recheada?",
    ["Não", "Sim"],
    horizontal=True
)

borda_valor = 1 if borda == "Sim" else 0

st.divider()

# ======================================
# BOTÃO
# ======================================

if st.button(
    "🍕 Calcular Preço",
    use_container_width=True
):

    # URL DA API
    url = (
        f"https://python-pizza-ai-dashboard.onrender.com/predict"
        f"?diametro={diametro}"
        f"&ingredientes={ingredientes}"
        f"&borda={borda_valor}"
    )

    try:

        with st.spinner("🤖 Calculando preço da pizza..."):

            resposta = requests.get(
                url,
                timeout=20
            )

            resposta.raise_for_status()

            dados = resposta.json()

            preco = dados["preco_previsto"]

        st.success("Previsão realizada com sucesso!")

        # ======================================
        # RESULTADO
        # ======================================

        st.metric(
            label="💰 Preço estimado",
            value=f"R$ {preco:.2f}"
        )

        st.divider()

        # ======================================
        # RESUMO
        # ======================================

        st.subheader("📋 Resumo da Pizza")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📏 Tamanho",
                f"{diametro} cm"
            )

        with col2:
            st.metric(
                "🧀 Ingredientes",
                ingredientes
            )

        with col3:
            st.metric(
                "🥖 Borda",
                borda
            )

        # ======================================
        # HISTÓRICO
        # ======================================

        st.session_state.historico.append({
            "Tamanho (cm)": diametro,
            "Ingredientes": ingredientes,
            "Borda": borda,
            "Preço (R$)": round(preco, 2)
        })

        st.balloons()

    except requests.exceptions.RequestException as erro:

        st.error(
            "❌ Não foi possível conectar à API."
        )

        st.write(erro)

# ======================================
# HISTÓRICO DE CONSULTAS
# ======================================

if len(st.session_state.historico) > 0:

    st.divider()

    st.subheader("📊 Histórico de Simulações")

    df_historico = pd.DataFrame(
        st.session_state.historico
    )

    df_historico.index = (
        df_historico.index + 1
    )

    df_historico.index.name = "Pedido"

    st.dataframe(
        df_historico,
        use_container_width=True
    )

    st.caption(
        f"Total de simulações: {len(df_historico)}"
    )