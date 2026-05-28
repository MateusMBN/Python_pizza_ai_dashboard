import streamlit as st
import requests
import pandas as pd

# ======================================
# CONFIG
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
    format_func=lambda x: (
        "Sim" if x == 1 else "Não"
    )
)

# ======================================
# BOTÃO
# ======================================

if st.button("🤖 Fazer previsão"):

    # ======================================
    # URL API
    # ======================================

    url = (
        f"http://127.0.0.1:8000/predict"
        f"?diametro={diametro}"
        f"&ingredientes={ingredientes}"
        f"&borda={borda}"
    )

    # ======================================
    # REQUEST
    # ======================================

    dados = None

    try:

        resposta = requests.get(
            url,
            timeout=10
        )

        resposta.raise_for_status()

        dados = resposta.json()

    except requests.exceptions.RequestException as exc:

        st.error(
            f"Erro ao chamar API: {exc}"
        )

        st.write(
            "Verifique se o FastAPI está rodando."
        )

    except ValueError:

        st.error(
            "Resposta inválida da API."
        )

        st.write(
            "Resposta recebida:",
            resposta.text
        )

    # ======================================
    # RESULTADO
    # ======================================

    if dados is not None:

        preco = dados.get(
            "preco_previsto"
        )

        if preco is None:

            st.error(
                "Campo 'preco_previsto' não encontrado."
            )

            st.write(dados)

        else:

            # ======================================
            # SUCESSO
            # ======================================

            st.success(
                f"🍕 Preço previsto: R$ {preco}"
            )

            st.balloons()

            # ======================================
            # HISTÓRICO
            # ======================================

            st.session_state.historico.append({

                "diametro": diametro,

                "ingredientes": ingredientes,

                "borda": (
                    "Sim"
                    if borda == 1
                    else "Não"
                ),

                "preco": preco

            })

# ======================================
# DASHBOARD
# ======================================

if st.session_state.historico:

    st.divider()

    st.subheader(
        "📊 Histórico de Previsões"
    )

    # ======================================
    # DATAFRAME
    # ======================================

    df_historico = pd.DataFrame(
        st.session_state.historico
    )

    # ======================================
    # ÍNDICE COMEÇANDO EM 1
    # ======================================

    df_historico.index = (
        df_historico.index + 1
    )

    df_historico.index.name = "Pedido"

    # ======================================
    # TABELA
    # ======================================

    st.dataframe(
        df_historico,
        use_container_width=True
    )

    # ======================================
    # MÉTRICAS
    # ======================================

    st.subheader("📈 Métricas")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🍕 Preço Médio",
        f'R$ {round(df_historico["preco"].mean(), 2)}'
    )

    col2.metric(
        "📈 Maior Preço",
        f'R$ {round(df_historico["preco"].max(), 2)}'
    )

    col3.metric(
        "📉 Menor Preço",
        f'R$ {round(df_historico["preco"].min(), 2)}'
    )

    # ======================================
    # GRÁFICO DE LINHA
    # ======================================

    st.subheader(
        "📈 Evolução dos Preços"
    )

    st.line_chart(
        df_historico["preco"]
    )

    # ======================================
    # GRÁFICO DISPERSÃO
    # ======================================

    st.subheader(
        "🧀 Ingredientes x Preço"
    )

    st.scatter_chart(
        data=df_historico,
        x="ingredientes",
        y="preco"
    )