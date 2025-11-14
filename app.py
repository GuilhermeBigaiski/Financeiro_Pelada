import streamlit as st
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from datetime import date

# ---------------------------
#  POOL DE CONEXÕES
# ---------------------------
@st.cache_resource
def get_pool():
    return SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        host="aws-1-us-east-2.pooler.supabase.com",
        database="postgres",
        user="postgres.xcogxppribxdhehmcdlb",
        password=st.secrets["db_password"],
        port=5432,
        sslmode='require'
    )

def run_query(query, params=None, fetch=True):
    pool = get_pool()
    conn = pool.getconn()
    cur = conn.cursor()

    cur.execute(query, params or ())
    result = cur.fetchall() if fetch else None

    conn.commit()
    cur.close()
    pool.putconn(conn)

    return result


# ---------------------------
#        INTERFACE
# ---------------------------

st.title("💰 Registro Financeiro")

# ---- TIPOS (mensalidade, receita, despesa) ----
tipos = run_query("SELECT id, tipo FROM fin_tipo ORDER BY tipo")
tipo_escolhido = st.selectbox("Selecione o tipo:", tipos, format_func=lambda x: x[1])

tipo_nome = tipo_escolhido[1].lower()   # para lógica abaixo


# ---- Se for DESPESA ou RECEITA → mostrar descrição ----
descricao_id = None
jogador_id = None

if tipo_nome in ["despesa", "receita"]:
    descricoes = run_query("SELECT id, descricao FROM fin_descricao ORDER BY descricao")
    desc_escolhida = st.selectbox(
        "Selecione a descrição:",
        descricoes,
        format_func=lambda x: x[1]
    )
    descricao_id = desc_escolhida[0]


# ---- Se for MENSALIDADE → mostrar dropdown de jogador ----
if tipo_nome == "mensalidade":
    jogadores = run_query("SELECT id, nome FROM jogadores ORDER BY nome")
    jogador_escolhido = st.selectbox(
        "Selecione o jogador:",
        jogadores,
        format_func=lambda x: x[1]
    )
    jogador_id = jogador_escolhido[0]


# ---- Data ----
data_registro = st.date_input("Data:", value=date.today())

# ---- Valor ----
valor = st.number_input("Valor (R$):", min_value=0.0, step=0.01, format="%.2f")


# ---- Botão ENVIAR ----
if st.button("Registrar"):

    if valor <= 0:
        st.error("⚠ Valor inválido.")
        st.stop()

    # INSERIR FINANCEIRO
    run_query("""
        INSERT INTO financeiro (tipo_id, descricao_id, jogador_id, data, valor)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        tipo_escolhido[0],
        descricao_id,
        jogador_id,
        data_registro,
        valor
    ), fetch=False)

    st.success("✅ Registro inserido com sucesso!")