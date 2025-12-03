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
    ("4.1.2", "Despesas Administrativas", "Despesa", "D"),
    ("4.1.3", "Despesas de Vendas", "Despesa", "D"),
]

plano_df = pd.DataFrame(
    plano_contas_data,
    columns=["Código", "Conta", "Grupo", "Natureza"]
)

# Inicializa DataFrame de lançamentos na sessão, se ainda não existir
if "lancamentos" not in st.session_state:
    st.session_state["lancamentos"] = pd.DataFrame(
        columns=[
            "Data", "Histórico",
            "Código Débito", "Conta Débito",
            "Código Crédito", "Conta Crédito",
            "Valor"
        ]
    )

tabs = st.tabs([
    "📘 Plano de Contas",
    "📒 Lançamentos",
    "📊 Balancete",
    "🏛️ Balanço Patrimonial",
    "📄 DRE"
])

# -----------------------------------------------------------------------------
# TAB 1 – PLANO DE CONTAS
# -----------------------------------------------------------------------------
with tabs[0]:
    st.subheader("📘 Plano de Contas Simplificado")
    st.dataframe(plano_df, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2 – LANÇAMENTOS
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("📒 Registro de Lançamentos Contábeis")

    col_esq, col_dir = st.columns(2)

    with col_esq:
        data_lanc = st.date_input("Data do lançamento", value=date.today())
        historico = st.text_input("Histórico", value="")

    with col_dir:
        contas_opcoes = plano_df["Código"] + " - " + plano_df["Conta"]

        conta_debito = st.selectbox(
            "Conta de Débito",
            options=contas_opcoes,
            index=0,
        )
        conta_credito = st.selectbox(
            "Conta de Crédito",
            options=contas_opcoes,
            index=4,
        )
        valor = st.number_input(
            "Valor (R$)",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

    if st.button("➕ Adicionar lançamento"):
        if valor <= 0:
            st.warning("Informe um valor maior que zero.")
        elif conta_debito == conta_credito:
            st.warning("Conta de débito e crédito não podem ser iguais.")
        else:
            cod_deb, nome_deb = conta_debito.split(" - ", 1)
            cod_cred, nome_cred = conta_credito.split(" - ", 1)

            novo_lanc = pd.DataFrame([{
                "Data": data_lanc,
                "Histórico": historico,
                "Código Débito": cod_deb,
                "Conta Débito": nome_deb,
                "Código Crédito": cod_cred,
                "Conta Crédito": nome_cred,
                "Valor": valor,
            }])

            st.session_state["lancamentos"] = pd.concat(
                [st.session_state["lancamentos"], novo_lanc],
                ignore_index=True
            )

            st.success("Lançamento incluído com sucesso!")

    st.markdown("### 🧾 Lançamentos registrados")
    if st.session_state["lancamentos"].empty:
        st.info("Nenhum lançamento registrado ainda.")
    else:
        st.dataframe(st.session_state["lancamentos"], use_container_width=True)

        if st.button("🗑️ Limpar todos os lançamentos"):
            st.session_state["lancamentos"] = st.session_state["lancamentos"].iloc[0:0]
            st.warning("Todos os lançamentos foram apagados.")

# -----------------------------------------------------------------------------
# Função auxiliar: gera balancete
# -----------------------------------------------------------------------------
def gerar_balancete(lanc_df: pd.DataFrame) -> pd.DataFrame:
    if lanc_df.empty:
        return pd.DataFrame()

    # Tabela com todas as movimentações por conta
    mov_linhas = []
    for _, row in lanc_df.iterrows():
        mov_linhas.append({
            "Código": row["Código Débito"],
            "Tipo": "D",
            "Valor": row["Valor"],
        })
        mov_linhas.append({
            "Código": row["Código Crédito"],
            "Tipo": "C",
            "Valor": row["Valor"],
        })

    mov_df = pd.DataFrame(mov_linhas)

    # Soma débitos e créditos por conta
    debitos = mov_df[mov_df["Tipo"] == "D"].groupby("Código")["Valor"].sum()
    creditos = mov_df[mov_df["Tipo"] == "C"].groupby("Código")["Valor"].sum()

    bal = plano_df[["Código", "Conta", "Grupo", "Natureza"]].copy()
    bal["Débitos"] = bal["Código"].map(debitos).fillna(0.0)
    bal["Créditos"] = bal["Código"].map(creditos).fillna(0.0)

    # Calcula saldo de acordo com a natureza
    saldos = []
    for _, r in bal.iterrows():
        if r["Natureza"] == "D":
            saldo = r["Débitos"] - r["Créditos"]
        else:
            saldo = r["Créditos"] - r["Débitos"]
        saldos.append(saldo)

    bal["Saldo"] = saldos

    # Só mostra contas com movimento
    bal = bal[(bal["Débitos"] != 0) | (bal["Créditos"] != 0)]

    return bal

# -----------------------------------------------------------------------------
# TAB 3 – BALANCETE
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("📊 Balancete de Verificação")

    balancete = gerar_balancete(st.session_state["lancamentos"])

    if balancete.empty:
        st.info("Nenhum lançamento registrado para gerar o balancete.")
    else:
        st.dataframe(balancete, use_container_width=True)

        total_debitos = balancete["Débitos"].sum()
        total_creditos = balancete["Créditos"].sum()

        st.write(f"**Total de Débitos:** R$ {total_debitos:,.2f}")
        st.write(f"**Total de Créditos:** R$ {total_creditos:,.2f}")

        if abs(total_debitos - total_creditos) < 0.01:
            st.success("Balancete em equilíbrio (Débitos = Créditos). ✅")
        else:
            st.error("Balancete não está em equilíbrio. ❌ Verifique os lançamentos.")

# -----------------------------------------------------------------------------
# TAB 4 – BALANÇO PATRIMONIAL
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("🏛️ Balanço Patrimonial (simplificado)")

    balancete = gerar_balancete(st.session_state["lancamentos"])

    if balancete.empty:
        st.info("Nenhum lançamento registrado para gerar o Balanço.")
    else:
        ativo = balancete[balancete["Grupo"] == "Ativo"][["Conta", "Saldo"]]
        passivo = balancete[balancete["Grupo"] == "Passivo"][["Conta", "Saldo"]]
        pl = balancete[balancete["Grupo"] == "Patrimônio Líquido"][["Conta", "Saldo"]]

        col_a, col_p = st.columns(2)

        with col_a:
            st.markdown("### Ativo")
            st.dataframe(ativo, use_container_width=True)
            st.write(f"**Total do Ativo:** R$ {ativo['Saldo'].sum():,.2f}")

        with col_p:
            st.markdown("### Passivo + Patrimônio Líquido")
            st.dataframe(
                pd.concat([passivo.assign(Grupo="Passivo"),
                           pl.assign(Grupo="Patrimônio Líquido")]),
                use_container_width=True
            )
            total_passivo_pl = passivo["Saldo"].sum() + pl["Saldo"].sum()
            st.write(f"**Total do Passivo + PL:** R$ {total_passivo_pl:,.2f}")

# -----------------------------------------------------------------------------
# TAB 5 – DRE
# -----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("📄 Demonstração do Resultado do Exercício (simplificada)")

    balancete = gerar_balancete(st.session_state["lancamentos"])

    if balancete.empty:
        st.info("Nenhum lançamento registrado para gerar a DRE.")
    else:
        receitas = balancete[balancete["Grupo"] == "Receita"][["Conta", "Saldo"]]
        despesas = balancete[balancete["Grupo"] == "Despesa"][["Conta", "Saldo"]]

        # Receitas têm natureza credora (saldo > 0)
        total_receitas = receitas["Saldo"].sum()
        # Despesas têm natureza devedora, saldo > 0
        total_despesas = despesas["Saldo"].sum()

        st.markdown("### Receitas")
        st.dataframe(receitas, use_container_width=True)

        st.markdown("### Despesas")
        st.dataframe(despesas, use_container_width=True)

        resultado = total_receitas - total_despesas

        st.markdown("### Resultado do Período")
        if resultado > 0:
            st.success(f"**Lucro Líquido:** R$ {resultado:,.2f}")
        elif resultado < 0:
            st.error(f"**Prejuízo Líquido:** R$ {abs(resultado):,.2f}")
        else:
            st.info("Resultado de R$ 0,00 (ponto de equilíbrio).")
import streamlit as st
import pandas as pd
from datetime import date

# -------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------------------------
st.set_page_config(
    page_title="General Accounting Lab",
    page_icon="📚",
    layout="wide",
)

st.title("📚 General Accounting Lab")
st.write(
    """
    Ambiente interativo para estudar **Contabilidade Geral**:  
    lançamentos, **Balancete**, **Balanço**, **DRE** e **Fluxo de Caixa**
    (método direto e indireto).
    """
)

# -------------------------------------------------------------------
# PLANO DE CONTAS SIMPLIFICADO
# código, nome, grupo, natureza (D/C)
# -------------------------------------------------------------------
plano_contas_data = [
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
    ("4.1.2", "Despesas Administrativas", "Despesa", "D"),
    ("4.1.3", "Despesas de Vendas", "Despesa", "D"),
]

plano_df = pd.DataFrame(
    plano_contas_data,
    columns=["Código", "Conta", "Grupo", "Natureza"]
)

# -------------------------------------------------------------------
# ESTADO INICIAL – DATAFRAME DE LANÇAMENTOS
# -------------------------------------------------------------------
if "lancamentos" not in st.session_state:
    st.session_state["lancamentos"] = pd.DataFrame(
        columns=[
            "Data", "Histórico",
            "Código Débito", "Conta Débito",
            "Código Crédito", "Conta Crédito",
            "Valor"
        ]
    )

# -------------------------------------------------------------------
# TABS PRINCIPAIS
# -------------------------------------------------------------------
tabs = st.tabs([
    "📘 Plano de Contas",
    "📒 Lançamentos",
    "📊 Balancete",
    "🏛️ Balanço Patrimonial",
    "📄 DRE",
    "💧 Fluxo de Caixa",
])

# -------------------------------------------------------------------
# TAB 1 – PLANO DE CONTAS
# -------------------------------------------------------------------
with tabs[0]:
    st.subheader("📘 Plano de Contas Simplificado")
    st.dataframe(plano_df, use_container_width=True)

# -------------------------------------------------------------------
# TAB 2 – LANÇAMENTOS
# -------------------------------------------------------------------
with tabs[1]:
    st.subheader("📒 Registro de Lançamentos Contábeis")

    col_esq, col_dir = st.columns(2)

    with col_esq:
        data_lanc = st.date_input("Data do lançamento", value=date.today())
        historico = st.text_input("Histórico", value="")

    with col_dir:
        contas_opcoes = plano_df["Código"] + " - " + plano_df["Conta"]

        conta_debito = st.selectbox(
            "Conta de Débito",
            options=contas_opcoes,
        )
        conta_credito = st.selectbox(
            "Conta de Crédito",
            options=contas_opcoes,
        )
        valor = st.number_input(
            "Valor (R$)",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

    if st.button("➕ Adicionar lançamento"):
        if valor <= 0:
            st.warning("Informe um valor maior que zero.")
        elif conta_debito == conta_credito:
            st.warning("Conta de débito e crédito não podem ser iguais.")
        else:
            cod_deb, nome_deb = conta_debito.split(" - ", 1)
            cod_cred, nome_cred = conta_credito.split(" - ", 1)

            novo_lanc = pd.DataFrame([{
                "Data": data_lanc,
                "Histórico": historico,
                "Código Débito": cod_deb,
                "Conta Débito": nome_deb,
                "Código Crédito": cod_cred,
                "Conta Crédito": nome_cred,
                "Valor": valor,
            }])

            st.session_state["lancamentos"] = pd.concat(
                [st.session_state["lancamentos"], novo_lanc],
                ignore_index=True
            )

            st.success("Lançamento incluído com sucesso!")

    st.markdown("### 🧾 Lançamentos registrados")
    if st.session_state["lancamentos"].empty:
        st.info("Nenhum lançamento registrado ainda.")
    else:
        st.dataframe(st.session_state["lancamentos"], use_container_width=True)

        if st.button("🗑️ Limpar todos os lan

