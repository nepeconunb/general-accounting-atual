import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="General Accounting Lab",
    page_icon="📚",
    layout="wide",
)

st.title("📚 General Accounting Lab")
st.write(
    """
    Ambiente interativo para estudar **Contabilidade Geral**:  
    lançamentos de contas patrimoniais e de resultado, **Balancete**, **Balanço** e **DRE**.
    """
)

# -----------------------------------------------------------------------------
# PLANO DE CONTAS SIMPLIFICADO
# -----------------------------------------------------------------------------
plano_contas_data = [
    # código, nome, grupo, natureza (D/C)
    ("1.1.1", "Caixa", "Ativo", "D"),
    ("1.1.2", "Bancos Conta Movimento", "Ativo", "D"),
    ("1.1.3", "Clientes", "Ativo", "D"),
    ("1.1.4", "Estoques", "Ativo", "D"),

    ("2.1.1", "Fornecedores", "Passivo", "C"),
    ("2.1.2", "Empréstimos a Pagar", "Passivo", "C"),

    ("2.3.1", "Capital Social", "Patrimônio Líquido", "C"),
    ("2.3.2", "Lucros Acumulados", "Patrimônio Líquido", "C"),

    ("3.1.1", "Receita de Vendas", "Receita", "C"),
    ("3.1.2", "Receita de Serviços", "Receita", "C"),

    ("4.1.1", "Custo das Mercadorias Vendidas", "Despesa", "D"),
    ("4.1.2", "Despesas Administrativas", "D

