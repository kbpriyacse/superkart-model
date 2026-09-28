
import streamlit as st
import requests
import pandas as pd
import os

# Backend URL inside the Docker network
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://superkart-backend:5000"
)

st.set_page_config(
    page_title="SuperKart Sales Forecasting",
    layout="centered"
)

st.title("SuperKart Sales Forecasting")

st.write(
    "Predict product sales using the SuperKart forecasting model."
)

# ---------------------------------------------------------
# Prediction type
# ---------------------------------------------------------

prediction_type = st.radio(
    "Select prediction type",
    ["Single Prediction", "Batch Prediction"]
)


# ---------------------------------------------------------
# SINGLE PREDICTION
# ---------------------------------------------------------

if prediction_type == "Single Prediction":

    st.subheader("Product and Store Information")

    product_weight = st.number_input(
        "Product Weight",
        min_value=0.0
    )

    sugar_content = st.selectbox(
        "Product Sugar Content",
        ["Low Sugar", "Regular", "No Sugar"]
    )

    allocated_area = st.number_input(
        "Product Allocated Area",
        min_value=0.0
    )

    product_mrp = st.number_input(
        "Product MRP",
        min_value=0.0
    )

    store_size = st.selectbox(
        "Store Size",
        ["Small", "Medium", "High"]
    )

    city_type = st.selectbox(
        "Store Location City Type",
        ["Tier 1", "Tier 2", "Tier 3"]
    )

    store_type = st.text_input(
        "Store Type"
    )

    product_id_char = st.text_input(
        "Product ID Character",
        value="FD"
    )

    store_age = st.number_input(
        "Store Age (Years)",
        min_value=0,
        step=1
    )

    product_type_category = st.text_input(
        "Product Type Category"
    )

    if st.button("Predict Sales"):

        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": sugar_content,
            "Product_Allocated_Area": allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": city_type,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age,
            "Product_Type_Category": product_type_category
        }

        try:

            response = requests.post(
                BACKEND_URL + "/v1/predict",
                json=payload
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    f"Predicted Sales: {result['Sales']:.2f}"
                )

            else:
                st.error(
                    f"Prediction failed: {response.text}"
                )

        except Exception as e:
            st.error(f"Unable to connect to backend: {e}")


# ---------------------------------------------------------
# BATCH PREDICTION
# ---------------------------------------------------------

else:

    st.subheader("Batch Sales Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        batch_data = pd.read_csv(uploaded_file)

        st.write("Uploaded Data")
        st.dataframe(batch_data)

        if st.button("Generate Batch Predictions"):

            uploaded_file.seek(0)

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            try:

                response = requests.post(
                    BACKEND_URL + "/v1/predictbatch",
                    files=files
                )

                if response.status_code == 200:

                    predictions = response.json()

                    batch_data["Predicted_Sales"] = [
                        predictions[str(i)]
                        for i in range(len(batch_data))
                    ]

                    st.success(
                        "Batch prediction completed successfully."
                    )

                    st.dataframe(batch_data)

                else:
                    st.error(
                        f"Prediction failed: {response.text}"
                    )

            except Exception as e:
                st.error(f"Unable to connect to backend: {e}")
