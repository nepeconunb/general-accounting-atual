import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="General Accounting Lab",
    page_icon="📚",
    layout="wide",
)

st.title("📚 General Accounting Lab")
st.write(
    """
    Bem-vinda ao **General Accounting Lab**!  
    Um ambiente interativo para estudar **Contabilidade Geral**, 
    com foco em lançamentos, partidas dobradas e demonstrações básicas.
    """
)

tabs = st.tabs(["📒 Lançamentos básicos", "🧮 Verificar partida dobrada", "❓ Quiz de Contabilidade"])

# --------------------------------------------------------------------
# TAB 1 – LANÇAMENTOS BÁSICOS
# --------------------------------------------------------------------
with tabs[0]:
    st.subheader("📒 Simulador de Lançamentos Contábeis")

    operacoes = {
        "Compra de mercadorias à vista (dinheiro)":
            {"debito": "Estoques", "credito": "Caixa"},
        "Compra de mercadorias a prazo (fornecedor)":
            {"debito": "Estoques", "credito": "Fornecedores"},
        "Venda de mercadorias à vista":
            {"debito": "Caixa", "credito": "Receita de Vendas"},
        "Venda de mercadorias a prazo (cliente)":
            {"debito": "Clientes", "credito": "Receita de Vendas"},
        "Pagamento de fornecedor":
            {"debito": "Fornecedores", "credito": "Caixa"},
        "Recebimento de cliente":
            {"debito": "Caixa", "credito": "Clientes"},
    }

    operacao = st.selectbox(
        "Selecione uma operação econômica:",
        list(operacoes.keys())
    )

    valor = st.number_input(
        "Informe o valor da operação (R$):",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

    if st.button("Gerar lançamento"):
        if valor <= 0:
            st.warning("Informe um valor maior que zero.")
        else:
            lanc = operacoes[operacao]
            debito = lanc["debito"]
            credito = lanc["credito"]

            st.markdown("### Lançamento Contábil Sugerido")
            st.write(f"**Débito:** {debito} – R$ {valor:,.2f}")
            st.write(f"**Crédito:** {credito} – R$ {valor:,.2f}")

            data = {
                "Conta": [debito, credito],
                "Débito (R$)": [valor, 0.0],
                "Crédito (R$)": [0.0, valor],
            }
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            st.info("Observação: todo lançamento deve manter a igualdade entre débitos e créditos (partida dobrada).")

# --------------------------------------------------------------------
# TAB 2 – VERIFICAR PARTIDA DOBRADA
# --------------------------------------------------------------------
with tabs[1]:
    st.subheader("🧮 Verificador de Partida Dobrada")

    st.write("Digite um lançamento com até **3 contas** para verificar se os débitos são iguais aos créditos.")

    col1, col2, col3 = st.columns(3)

    with col1:
        conta1 = st.text_input("Conta 1")
        tipo1 = st.selectbox("Tipo 1", ["Débito", "Crédito"], key="tipo1")
        valor1 = st.number_input("Valor 1 (R$)", min_value=0.0, step=10.0, key="valor1")

    with col2:
        conta2 = st.text_input("Conta 2")
        tipo2 = st.selectbox("Tipo 2", ["Débito", "Crédito"], key="tipo2")
        valor2 = st.number_input("Valor 2 (R$)", min_value=0.0, step=10.0, key="valor2")

    with col3:
        conta3 = st.text_input("Conta 3 (opcional)")
        tipo3 = st.selectbox("Tipo 3", ["Débito", "Crédito"], key="tipo3")
        valor3 = st.number_input("Valor 3 (R$)", min_value=0.0, step=10.0, key="valor3")

    if st.button("Verificar"):
        debitos = 0.0
        creditos = 0.0

        linhas = []

        if conta1 and valor1 > 0:
            if tipo1 == "Débito":
                debitos += valor1
            else:
                creditos += valor1
            linhas.append((conta1, valor1 if tipo1 == "Débito" else 0.0,
                           valor1 if tipo1 == "Crédito" else 0.0))

        if conta2 and valor2 > 0:
            if tipo2 == "Débito":
                debitos += valor2
            else:
                creditos += valor2
            linhas.append((conta2, valor2 if tipo2 == "Débito" else 0.0,
                           valor2 if tipo2 == "Crédito" else 0.0))

        if conta3 and valor3 > 0:
            if tipo3 == "Débito":
                debitos += valor3
            else:
                creditos += valor3
            linhas.append((conta3, valor3 if tipo3 == "Débito" else 0.0,
                           valor3 if tipo3 == "Crédito" else 0.0))

        if not linhas:
            st.warning("Informe pelo menos uma conta com valor.")
        else:
            df_lanc = pd.DataFrame(linhas, columns=["Conta", "Débito (R$)", "Crédito (R$)"])
            st.dataframe(df_lanc, use_container_width=True)

            st.write(f"**Total de Débitos:** R$ {debitos:,.2f}")
            st.write(f"**Total de Créditos:** R$ {creditos:,.2f}")

            if abs(debitos - creditos) < 0.01:
                st.success("Lançamento em partida dobrada! ✅")
            else:
                st.error("Os débitos não são iguais aos créditos. ❌ Verifique o lançamento.")

# --------------------------------------------------------------------
# TAB 3 – QUIZ
# --------------------------------------------------------------------
with tabs[2]:
    st.subheader("❓ Quiz de Lançamentos Básicos")

    pergunta = "A compra de mercadorias a prazo com fornecedor gera qual lançamento?"
    st.write(pergunta)

    alternativa = st.radio(
        "Escolha a alternativa correta:",
        [
            "Débito em Fornecedores e Crédito em Estoques",
            "Débito em Estoques e Crédito em Fornecedores",
            "Débito em Caixa e Crédito em Estoques",
            "Débito em Despesa de Mercadorias e Crédito em Caixa",
        ]
    )

    if st.button("Corrigir resposta"):
        if alternativa == "Débito em Estoques e Crédito em Fornecedores":
            st.success("Correto! 🎉 A compra aumenta Estoques (ativo) e aumenta Fornecedores (passivo).")
        else:
            st.error("Incorreto! Tente novamente.")
