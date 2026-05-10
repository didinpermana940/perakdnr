import streamlit as st

st.set_page_config(page_title="AI Finance Agent", page_icon="💰", layout="centered")

# ======================
# TITLE
# ======================
st.title("💰 AI Finance Agent Pro")
st.write("Asisten Keuangan Pribadi Cerdas")

# ======================
# INPUT
# ======================
income = st.number_input("💵 Pemasukan Bulanan", min_value=0)
expense = st.number_input("💸 Pengeluaran Bulanan", min_value=0)

category = st.selectbox(
    "📊 Kategori Pengeluaran",
    ["Makan", "Transport", "Belanja", "Tagihan", "Lainnya"]
)

# ======================
# SESSION HISTORY
# ======================
if "history" not in st.session_state:
    st.session_state.history = []

# ======================
# BUTTON ANALISIS
# ======================
if st.button("🔍 Analisis Keuangan"):

    balance = income - expense
    saving_rate = 0

    if income > 0:
        saving_rate = (balance / income) * 100

    # simpan history
    st.session_state.history.append({
        "income": income,
        "expense": expense,
        "balance": balance,
        "category": category
    })

    # ======================
    # OUTPUT
    # ======================
    st.subheader("📊 Hasil Analisis")

    st.write(f"💰 Saldo: Rp {balance:,.0f}")
    st.write(f"📈 Tingkat Tabungan: {saving_rate:.2f}%")

    # ======================
    # LOGIC AI SEDERHANA
    # ======================
    if balance > 0:
        st.success("Keuangan kamu sehat 👍")

        if saving_rate < 20:
            st.warning("Saran: coba tingkatkan tabungan minimal 20%")
        else:
            st.info("Bagus! kamu sudah menabung dengan baik")

    elif balance == 0:
        st.warning("Kamu impas ⚠ mulai atur pengeluaran")

    else:
        st.error("Kamu defisit ❌ perlu kontrol pengeluaran")

# ======================
# HISTORY
# ======================
st.subheader("📜 Riwayat Transaksi")

for i, item in enumerate(st.session_state.history[::-1]):
    st.write(
        f"{i+1}. 💵 {item['income']} | 💸 {item['expense']} | 💰 {item['balance']} | 📊 {item['category']}"
    )