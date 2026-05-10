import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# =========================
# CONFIG UI
# =========================
st.set_page_config(page_title="Permana Link", layout="centered")

st.markdown("""
<style>
body { background-color: #0b1220; color: white; }

.header {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-top: 10px;
}

.balance {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    background-color: #2563eb;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("finance.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user'
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
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# =========================
# ADMIN DEFAULT
# =========================
def create_admin():
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "admin")
        )
        conn.commit()

create_admin()

# =========================
# FUNCTIONS
# =========================
def register(u, p):
    try:
        c.execute("INSERT INTO users VALUES (NULL,?,?,?)",
                  (u, hash_password(p), "user"))
        conn.commit()
        return True
    except:
        return False

def login(u, p):
    c.execute("SELECT username, role FROM users WHERE username=? AND password=?",
              (u, hash_password(p)))
    return c.fetchone()

def add_tx(user, t, a):
    c.execute("INSERT INTO transactions VALUES (NULL,?,?,?)",
              (user, t, a))
    conn.commit()

def get_tx(user):
    c.execute("SELECT type, amount FROM transactions WHERE username=?", (user,))
    return c.fetchall()

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = ""
    st.session_state.role = ""

# =========================
# MENU
# =========================
menu = st.sidebar.selectbox("Menu", ["Home", "Login", "Register"])

# =========================
# HOME
# =========================
if menu == "Home":
    st.markdown('<div class="header">💳 PERMANA LINK</div>', unsafe_allow_html=True)
    st.caption("Digital Banking & Finance App")

    st.markdown("""
    <div class="card">
        <h3>🚀 Selamat Datang</h3>
        <p>Aplikasi keuangan modern seperti OVO / DANA</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# REGISTER
# =========================
elif menu == "Register":
    st.title("📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Daftar"):
        if register(u, p):
            st.success("Akun dibuat 🎉")
        else:
            st.error("Username sudah ada")

# =========================
# LOGIN
# =========================
elif menu == "Login":
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(u, p)
        if user:
            st.session_state.login = True
            st.session_state.user = user[0]
            st.session_state.role = user[1]
            st.success("Login berhasil 🚀")
        else:
            st.error("Login gagal")

# =========================
# DASHBOARD (BANK STYLE)
# =========================
if st.session_state.login:

    st.markdown(f"## 🏦 Halo, {st.session_state.user}")

    # INPUT TRANSAKSI
    st.subheader("➕ Transaksi")

    t = st.selectbox("Tipe", ["Pemasukan", "Pengeluaran"])
    a = st.number_input("Jumlah", min_value=0)

    if st.button("Simpan"):
        add_tx(st.session_state.user, t, a)
        st.success("Tersimpan!")

    # DATA
    data = get_tx(st.session_state.user)

    if data:
        df = pd.DataFrame(data, columns=["type", "amount"])

        pemasukan = df[df["type"] == "Pemasukan"]["amount"].sum()
        pengeluaran = df[df["type"] == "Pengeluaran"]["amount"].sum()
        saldo = pemasukan - pengeluaran

        # SALDO CARD
        st.markdown(f"""
        <div class="balance">
            <h3>💳 Saldo</h3>
            <h1>Rp {saldo:,}</h1>
        </div>
        """, unsafe_allow_html=True)

        # STAT
        col1, col2 = st.columns(2)
        col1.metric("💰 Masuk", f"Rp {pemasukan:,}")
        col2.metric("💸 Keluar", f"Rp {pengeluaran:,}")

        # GRAFIK
        st.subheader("📊 Grafik")
        st.bar_chart(df.groupby("type").sum())

        # TRANSAKSI
        st.subheader("📄 Transaksi")
        st.dataframe(df)

    # ADMIN PANEL
    if st.session_state.role == "admin":
        st.markdown("---")
        st.title("🧑‍💼 Admin Panel")

        c.execute("SELECT username, role FROM users")
        st.dataframe(pd.DataFrame(c.fetchall(), columns=["User","Role"]))

    # LOGOUT
    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.user = ""
        st.session_state.role = ""