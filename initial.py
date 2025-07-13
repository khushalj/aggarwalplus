import streamlit as st
import pandas as pd
from datetime import datetime

# Title
st.title("Carton Box Order Booking App")

# Session state to store orders
if 'orders' not in st.session_state:
    st.session_state.orders = []

st.sidebar.header("Customer & Order Entry")

# Customer details
with st.sidebar.form("customer_form"):
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
        order = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "address": address,
            "gst_number": gst_number,
            "phone": phone,
            "map_pin": map_pin,
            "box_type": box_type,
            "length": length,
            "breadth": breadth,
            "height": height,
            "quantity": quantity,
            "printing": printing,
            "color": color,
            "image_filename": image.name if image else "None"
        }
        st.session_state.orders.append(order)
        st.success("Order submitted successfully!")

# Display Orders Table
if st.session_state.orders:
    st.subheader("Submitted Orders")
    df = pd.DataFrame(st.session_state.orders)
    st.dataframe(df)

    # Export as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Orders as CSV", csv, "orders.csv", "text/csv")
