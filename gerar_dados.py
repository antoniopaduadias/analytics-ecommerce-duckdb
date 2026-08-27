import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("⏳ Gerando dados de e-commerce e logística...")
np.random.seed(42)
n_pedidos = 25000

data_inicial = datetime(2026, 3, 1)
datas = [data_inicial + timedelta(minutes=int(np.random.randint(0, 260000))) for _ in range(n_pedidos)]

cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Salvador', 'Recife']
p_cidades = [0.4, 0.15, 0.15, 0.1, 0.08, 0.07, 0.05]

status_lista = ['Entregue', 'Em trânsito', 'Cancelado', 'Atrasado']
p_status = [0.85, 0.08, 0.03, 0.04]

df = pd.DataFrame({
    'id_pedido': range(10001, 10001 + n_pedidos),
    'data_compra': datas,
    'regiao_destino': np.random.choice(cidades, size=n_pedidos, p=p_cidades),
    'valor_venda': np.round(np.random.exponential(scale=150, size=n_pedidos) + 20, 2),
    'custo_frete': np.round(np.random.normal(loc=25, scale=8, size=n_pedidos), 2),
    'status_entrega': np.random.choice(status_lista, size=n_pedidos, p=p_status),
    'dias_para_entrega': np.random.randint(1, 15, size=n_pedidos)
})

df['custo_frete'] = df['custo_frete'].clip(lower=5)
df.loc[df['status_entrega'] == 'Atrasado', 'dias_para_entrega'] += 7

con = duckdb.connect('ecommerce_analitico.db')
con.execute("CREATE OR REPLACE TABLE vendas_logistica AS SELECT * FROM df")
con.close()
print("✅ Banco 'ecommerce_analitico.db' criado com sucesso!")
