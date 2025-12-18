import streamlit as st
from supabase import create_client
from datetime import datetime

# Conexão com Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_API_KEY"]
supabase = create_client(url, key)

st.title("💰 Registro Financeiro da Pelada")

# Carrega dados
tipos_data = supabase.table("fin_tipo").select("id", "tipo").execute().data
descricoes_data = supabase.table("fin_descricao").select("id", "descricao", "tipo_id").execute().data
jogadores_data = supabase.table("jogadores").select("id", "nome").execute().data

# Converte para dicionários
tipos = {item["tipo"]: item["id"] for item in tipos_data}
jogadores = {item["nome"]: item["id"] for item in jogadores_data}

# Formulário
with st.form("form_financeiro"):
    tipo_nome = st.selectbox("📌 Tipo", list(tipos.keys()))
    tipo_id = tipos[tipo_nome]

    # Filtra as descrições pelo tipo selecionado
    descricoes_filtradas = {
        item["descricao"]: item["id"]
        for item in descricoes_data if item["tipo_id"] == tipo_id
    }

    descricao_nome = st.selectbox("📝 Descrição", list(descricoes_filtradas.keys()))
    jogador_nome = st.selectbox("👤 Jogador", list(jogadores.keys()))
    data = st.date_input("📅 Data da Transação", datetime.today())
    valor = st.number_input("💵 Valor (R$)", min_value=0.0, step=1.0, format="%.2f")

    submitted = st.form_submit_button("Registrar")

    if submitted:
        response = supabase.table("financeiro").insert({
            "tipo_id": tipo_id,
            "descricao_id": descricoes_filtradas[descricao_nome],
            "jogador_id": jogadores[jogador_nome],
            "data": str(data),
            "valor": valor
        }).execute()

        if hasattr(response, "data") and response.data:
            st.success("✅ Transação registrada com sucesso!")
        else:
            st.error("❌ Erro ao registrar a transação.")
            st.write(response)
