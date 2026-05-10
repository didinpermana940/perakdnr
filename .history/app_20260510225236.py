import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("finance.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    income REAL,
    expense REAL,
    category TEXT,
    note TEXT
)
""")

conn.commit()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Finance Agent Pro",
    page_icon="💰",
    layout="wide"
)

# =========================
# TITLE
# =========================
st.title("💰 AI Finance Agent Pro")
st.caption("Asisten Keuangan Cerdas")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📌 Input Transaksi")

income = st.sidebar.number_input("💵 Pemasukan", min_value=0.0)
expense = st.sidebar.number_input("💸 Pengeluaran", min_value=0.0)

category = st.sidebar.selectbox(
    "📂 Kategori",
    ["Makan", "Transport", "Belanja", "Tagihan", "Investasi", "Lainnya"]
)

note = st.sidebar.text_input("📝 Catatan")

# =========================
# SAVE DATA
# =========================
if st.sidebar.button("💾 Simpan Transaksi"):

    c.execute("""
    INSERT INTO transactions(date, income, expense, category, note)
    VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        income,
        expense,
        category,
        note
    ))

    conn.commit()

    st.sidebar.success("Transaksi berhasil disimpan ✅")

# =========================
# LOAD DATA
# =========================
df = pd.read_sql("SELECT * FROM transactions", conn)

# =========================
# DASHBOARD
# =========================
total_income = df["income"].sum() if not df.empty else 0
total_expense = df["expense"].sum() if not df.empty else 0
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)

col1.metric("💵 Total Pemasukan", f"Rp {total_income:,.0f}")
col2.metric("💸 Total Pengeluaran", f"Rp {total_expense:,.0f}")
col3.metric("💰 Saldo", f"Rp {balance:,.0f}")

# =========================
# AI ANALYSIS
# =========================
st.subheader("🤖 AI Analisis")

if balance > 0:
    st.success("Keuangan kamu sehat 👍")

    saving_rate = 0
    if total_income > 0:
        saving_rate = (balance / total_income) * 100

    st.write(f"📈 Tingkat tabungan: {saving_rate:.2f}%")

    if saving_rate < 20:
        st.warning("Saran AI: tingkatkan tabungan minimal 20%")
    else:
        st.info("Bagus! pola keuangan kamu cukup baik")

elif balance == 0:
    st.warning("Keuangan impas ⚠")

else:
    st.error("Pengeluaran lebih besar dari pemasukan ❌")

# =========================
# CHART
# =========================
st.subheader("📊 Grafik Pengeluaran")

if not df.empty:

    chart_data = df.groupby("category")["expense"].sum()

    st.bar_chart(chart_data)

# =========================
# HISTORY
# =========================
st.subheader("📜 Riwayat Transaksi")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada transaksi")

# =========================
# TARGET TABUNGAN
# =========================
st.subheader("🎯 Target Tabungan")

target = st.number_input("Masukkan target tabungan", min_value=0.0)

if target > 0:

    if balance >= target:
        st.success("🎉 Target tabungan tercapai!")
    else:
        remaining = target - balance
        st.warning(f"Kamu masih perlu Rp {remaining:,.0f}")