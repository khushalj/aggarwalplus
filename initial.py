import streamlit as st
import pandas as pd
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# ---- GOOGLE SHEETS SETUP ----
SHEET_NAME = "CartonBoxOrders"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Upload your Google service account credentials JSON file in .streamlit/secrets.toml for Streamlit Cloud
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=SCOPES
)
client = gspread.authorize(credentials)

# Create or open Google Sheet
try:
    sheet = client.open(SHEET_NAME).sheet1
except:
    sheet = client.create(SHEET_NAME).sheet1
    sheet.append_row([
        "Timestamp", "Name", "Address", "GST Number", "Phone", "Map Pin", "Box Type",
        "Length", "Breadth", "Height", "Quantity", "Printing", "Color", "Image Filename"
    ])

# ---- SESSION SETUP ----
if 'orders' not in st.session_state:
    st.session_state.orders = []

# ---- PAGE LAYOUT ----
st.title("Carton Box Order Booking System")

page = st.sidebar.radio("Select View", ["Salesman View", "Admin View"])

# ---- SALES VIEW ----
if page == "Salesman View":
    st.header("Salesman - Enter New Order")
    with st.form("salesman_form"):
        st.subheader("Customer Details")
        name = st.text_input("Customer Name")
        address = st.text_area("Address")
        gst_number = st.text_input("GST Number")
        phone = st.text_input("Phone Number")
        map_pin = st.text_input("Map Location Pin")

        st.subheader("Order Specifications")
        box_type = st.selectbox("Box Type", ["3 Ply", "5 Ply", "7 Ply"])
        length = st.number_input("Length (in inches)", min_value=1.0)
        breadth = st.number_input("Breadth (in inches)", min_value=1.0)
        height = st.number_input("Height (in inches)", min_value=1.0)
        quantity = st.number_input("Quantity", min_value=1)
        printing = st.radio("Printing Required?", ["Yes", "No"])
        color = st.selectbox("Color", ["Brown Kraft", "White", "Custom Print"])
        image = st.file_uploader("Upload Reference Image", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Submit Order")

        if submitted:
            order = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, address, gst_number,
                phone, map_pin, box_type, length, breadth, height, quantity,
                printing, color, image.name if image else "None"
            ]
            sheet.append_row(order)
            st.success("Order submitted successfully!")

# ---- ADMIN VIEW ----
elif page == "Admin View":
    st.header("Admin - View All Orders")
    password = st.text_input("Enter Admin Password", type="password")

    if password == st.secrets["admin_password"]:
        orders_data = sheet.get_all_records()
        df = pd.DataFrame(orders_data)

        if df.empty:
            st.info("No orders submitted yet.")
        else:
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Orders as CSV", csv, "all_orders.csv", "text/csv")
    elif password:
        st.error("Incorrect password")
