# Analytics E-commerce Dashboard 📊🛒

Este projeto consiste em um ecossistema analítico completo para monitoramento e análise de métricas operacionais de um e-commerce. A aplicação transforma dados brutos simulados em insights visuais em tempo real por meio de um dashboard interativo.

🔗 **Acesse a aplicação em produção:** [Link do Dashboard no Streamlit](https://streamlit.app)

## 🚀 Arquitetura e Componentes do Projeto

O projeto foi dividido em três etapas principais que refletem um pipeline real de engenharia e análise de dados:

1. **`gerar_dados.py`**: Script em Python responsável pela geração automatizada de dados transacionais fictícios e realistas (pedidos, clientes, regiões de destino e status logísticos).
2. **`ecommerce_analitico.db`**: Banco de dados relacional que armazena os dados gerados, estruturado para permitir consultas rápidas e organizadas de Business Intelligence.
3. **`app.py`**: Interface web interativa desenvolvida com Streamlit que se conecta à camada de dados para construir os indicadores visuais.

## 📈 Funcionalidades do Dashboard

* **Faturamento por Região**: Gráficos dinâmicos que consolidam e segmentam a receita financeira por destino.
* **Saúde das Entregas**: Gráfico de pizza que monitora a eficiência logística (pedidos entregues, em trânsito, atrasados e cancelados).
* **Filtros Operacionais Integrados**: Barra lateral interativa para refinar os dados por região geográfica e status simultaneamente.
* **Exportação de Dados**: Funcionalidade nativa para baixar a tabela de dados filtrada diretamente em formato CSV.

## 🛠️ Tecnologias Utilizadas

* **Python 3**: Linguagem base para manipulação lógica e scripts.
* **Streamlit**: Framework ágil para o desenvolvimento e publicação da interface web.
* **DuckDB / SQLite**: Motores de banco de dados utilizados para o processamento otimizado de consultas analíticas.
* **Pandas**: Biblioteca para tratamento, limpeza e estruturação dos dados brutos.

## 🔧 Como Executar o Projeto Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com
   cd analytics-ecommerce-duckdb
   ```

2. Instale as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Gere a base de dados (opcional, caso queira atualizar os registros):
   ```bash
   python gerar_dados.py
   ```

4. Execute a aplicação Streamlit:
   ```bash
   streamlit run app.py
   ```

---
Desenvolvido por [Antônio Pádua Dias](https://github.com).
