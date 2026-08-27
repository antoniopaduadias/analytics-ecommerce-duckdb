import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Analytics Hub", layout="wide", page_icon="🚚")
st.title("🚚 Operações de E-commerce & Logística Hub")
st.markdown("Painel de alta performance conectado nativamente ao **DuckDB**.")

@st.cache_resource
def obter_conexao():
    return duckdb.connect('ecommerce_analitico.db', read_only=True)

con = obter_conexao()
st.sidebar.header("🎯 Filtros Operacionais")

cidades_brutas = con.execute("SELECT DISTINCT regiao_destino FROM vendas_logistica ORDER BY 1").fetchall()
cidades_disponiveis = [c[0] for c in cidades_brutas]
cidade_selecionada = st.sidebar.selectbox("Filtrar por Região de Destino:", ["Todas"] + cidades_disponiveis)

status_brutos = con.execute("SELECT DISTINCT status_entrega FROM vendas_logistica ORDER BY 1").fetchall()
status_disponiveis = [s[0] for s in status_brutos]
status_selecionado = st.sidebar.multiselect("Filtrar por Status do Pedido:", status_disponiveis, default=status_disponiveis)

if not status_selecionado:
    st.warning("Por favor, selecione pelo menos um status na barra lateral.")
    st.stop()

query = "SELECT * FROM vendas_logistica WHERE status_entrega IN (?" + ",?" * (len(status_selecionado) - 1) + ")"
params = list(status_selecionado)

if cidade_selecionada != "Todas":
    query += " AND regiao_destino = ?"
    params.append(cidade_selecionada)

df_filtrado = con.execute(query, params).df()

total_vendas = df_filtrado['valor_venda'].sum()
total_pedidos = len(df_filtrado)
ticket_medio = df_filtrado['valor_venda'].mean() if total_pedidos > 0 else 0
taxa_atraso = (len(df_filtrado[df_filtrado['status_entrega'] == 'Atrasado']) / total_pedidos * 100) if total_pedidos > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Faturamento Filtrado", f"R$ {total_vendas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
kpi2.metric("Volume de Pedidos", f"{total_pedidos:,}".replace(",", "."))
kpi3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
kpi4.metric("Taxa de Atraso Logístico", f"{taxa_atraso:.1f}%")

st.markdown("---")
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("📈 Faturamento por Região")
    df_regiao = df_filtrado.groupby('regiao_destino')['valor_venda'].sum().reset_index().sort_values(by='valor_venda', ascending=False)
    fig_barra = px.bar(df_regiao, x='regiao_destino', y='valor_venda', labels={'regiao_destino': 'Cidade', 'valor_venda': 'Total (R$)'}, color='valor_venda', color_continuous_scale='Blues')
    st.plotly_chart(fig_barra, use_container_width=True)

with col_dir:
    st.subheader("📊 Saúde das Entregas (Status)")
    df_status = df_filtrado['status_entrega'].value_counts().reset_index()
    fig_pizza = px.pie(df_status, names='status_entrega', values='count', color='status_entrega',
                       color_discrete_map={'Entregue':'#2ca02c', 'Em trânsito':'#1f77b4', 'Atrasado':'#d62728', 'Cancelado':'#7f7f7f'})
    st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("---")
st.subheader("🧮 Simulador de Impacto de Custo de Frete Terceirizado")
ajuste_frete = st.slider("Aumento percentual no custo do frete (%):", min_value=0, max_value=50, value=10, step=5)

custo_frete_original = df_filtrado['custo_frete'].sum()
novo_custo_frete = custo_frete_original * (1 + (ajuste_frete / 100))
impacto_lucro = novo_custo_frete - custo_frete_original

sim1, sim2 = st.columns(2)
sim1.metric("Custo de Frete Projetado", f"R$ {novo_custo_frete:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
sim2.metric("Redução na Margem de Lucro", f"- R$ {impacto_lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.sidebar.download_button(
    label="📥 Exportar Dados Filtrados (CSV)",
    data=df_filtrado.to_csv(index=False),
    file_name=f"data_logistica.csv",
    mime="text/csv"
)
