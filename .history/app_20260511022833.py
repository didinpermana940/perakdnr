import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# =========================
# DATABASE SETUP
# =========================
conn = sqlite3.connect("finance.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    type TEXT,
    amount INTEGER
)
""")

conn.commit()

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# USER FUNCTIONS
# =========================
def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

# =========================
# TRANSAKSI
# =========================
def add_transaction(username, ttype, amount):
    c.execute("INSERT INTO transactions (username, type, amount) VALUES (?, ?, ?)",
              (username, ttype, amount))
    conn.commit()

def get_data(username):
    c.execute("SELECT type, amount FROM transactions WHERE username=?", (username,))
    return c.fetchall()

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = ""

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# =========================
# REGISTER
# =========================
if menu == "Register":
    st.title("📝 Register")

    u = st.text_input("Username baru")
    p = st.text_input("Password baru", type="password")

    if st.button("Daftar"):
        if register_user(u, p):
            st.success("Akun berhasil dibuat 🎉")
        else:
            st.error("Username sudah dipakai")

# =========================
# LOGIN
# =========================
elif menu == "Login":
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(u, p)
        if user:
            st.session_state.login = True
            st.session_state.user = u
            st.success("Login berhasil 🚀")
        else:
            st.error("Login gagal")

# =========================
# DASHBOARD
# =========================
if st.session_state.login:

    st.title(f"📊 Dashboard Keuangan - {st.session_state.user}")

    # INPUT TRANSAKSI
    st.subheader("➕ Tambah Transaksi")

    col1, col2 = st.columns(2)

    with col1:
        ttype = st.selectbox("Tipe", ["Pemasukan", "Pengeluaran"])

    with col2:
        amount = st.number_input("Jumlah", min_value=0)

    if st.button("Simpan"):
        add_transaction(st.session_state.user, ttype, amount)
        st.success("Tersimpan!")

    # DATA
    data = get_data(st.session_state.user)

    if data:
        df = pd.DataFrame(data, columns=["type", "amount"])

        st.subheader("📊 Grafik Keuangan")

        chart_data = df.groupby("type").sum()
        st.bar_chart(chart_data)

        st.subheader("📄 Data Transaksi")
        st.dataframe(df)
    else:
        st.info("Belum ada transaksi")

    # LOGOUT
    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.user = ""
        # 