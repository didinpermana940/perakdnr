import streamlit as st

st.title("🤖 AI Finance Agent")

income = st.number_input("Pemasukan")
expense = st.number_input("Pengeluaran")

if st.button("Analisis"):
    balance = income - expense
    st.write("Saldo:", balance)

    if balance > 0:
        st.success("Keuangan aman ✅")
    elif balance == 0:
        st.warning("Pas-pasan ⚠")
    else:
        st.error("Defisit ❌")