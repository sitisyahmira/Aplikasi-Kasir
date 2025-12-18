import streamlit as st
import pandas as pd
import uuid
from datetime import date

st.set_page_config(page_title="Kasir & Prediksi Usaha", layout="wide")
st.title("💰 Aplikasi Kasir, Prediksi & Rekomendasi Usaha")

transaction_types = ["Income", "Expense"]
categories = ["Sales", "Operational", "Marketing", "Salary", "Other"]
payment_methods = ["Cash", "Bank Transfer", "QRIS", "E-Wallet"]
counterparties = ["Customer", "Supplier", "Vendor", "Internal"]

if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.subheader("📝 Input Transaksi")

with st.form("form_transaksi"):
    col1, col2 = st.columns(2)

    with col1:
        tanggal = st.date_input("Tanggal", date.today())
        jenis = st.selectbox("Jenis Transaksi", transaction_types)
        kategori = st.selectbox("Kategori", categories)

    with col2:
        jumlah = st.number_input(
            "Jumlah / Harga (Rp)",
            min_value=0.0,
            step=1000.0
        )
        metode = st.selectbox("Metode Pembayaran", payment_methods)
        pihak = st.selectbox("Pihak Terkait", counterparties)

    simpan = st.form_submit_button("Simpan")

if simpan:
    st.session_state.transactions.append({
        "transaction_id": f"TX-{uuid.uuid4().hex[:6].upper()}",
        "date": tanggal,
        "transaction_type": jenis,
        "category": kategori,
        "amount": jumlah if jenis == "Income" else -jumlah,
        "payment_method": metode,
        "counterparty": pihak
    })
    st.success("✅ Transaksi berhasil disimpan")

if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expense = abs(df[df["amount"] < 0]["amount"].sum())
    profit = total_income - total_expense

    st.metric("Total Income", f"Rp {total_income:,.0f}")
    st.metric("Total Expense", f"Rp {total_expense:,.0f}")
    st.metric("Profit / Loss", f"Rp {profit:,.0f}")
