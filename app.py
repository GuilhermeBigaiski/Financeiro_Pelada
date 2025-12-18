import streamlit as st
from datetime import date
import requests
import os

# Carregando os secrets do Streamlit Cloud (armazenado via Settings > Secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ----- Funções auxiliares -----
@st.cache_data
def get_tipos():
    url = f"{SUPABASE_URL}/fin_tipo?select=id,nome"
    res = requests.get(url, headers=headers)
    return res.json()

@st.cache_data
def get_descricoes():
    url = f"{SUPABASE_URL}/fin_descricao?select=id,descricao,tipo_id"
    res = requests.get(url, headers=headers)
    return res.json()

# ----- Título -----
st.title("💰 Registro Financeiro - Pelada Quinta")

with st.form(key="finance_form"):
    data = st.date_input("📅 Data", value=date.today())

    # Obtem tipos e descrições
    tipos = get_tipos()
    descricoes = get_descricoes()

    tipo_opcoes = {t["nome"]: t["id"] for t in tipos}
    tipo_nome = st.selectbox("🧾 Tipo", list(tipo_opcoes.keys()))
    tipo_id = tipo_opcoes[tipo_nome]

    # Filtra descrições conforme o tipo escolhido
    descricoes_filtradas = [d for d in descricoes if d["tipo_id"] == tipo_id]
    descricao_opcoes = {d["descricao"]: d["id"] for d in descricoes_filtradas}

    descricao_nome = st.selectbox("📄 Descrição", list(descricao_opcoes.keys()))
    descricao_id = descricao_opcoes[descricao_nome]

    valor_str = st.text_input("💸 Valor (R$)", placeholder="Ex: 25,00 ou 25.00")

    submit = st.form_submit_button("Registrar")

# ----- Envio -----
if submit:
    try:
        # Troca vírgula por ponto se houver e tenta converter
        valor = float(valor_str.replace(",", "."))
        payload = {
            "data": str(data),
            "descricao_id": descricao_id,
            "valor": valor
        }

        url_insert = f"{SUPABASE_URL}/fin_lancamento"
        response = requests.post(url_insert, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            st.success("✅ Registro salvo com sucesso!")
        else:
            st.error(f"Erro ao registrar: {response.text}")

    except ValueError:
        st.error("⚠️ Valor inválido. Use ponto ou vírgula como separador decimal.")
