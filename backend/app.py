
# Import necessary libraries
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask application
superkart_api = Flask("SuperKart")

# Load the trained model pipeline
model = joblib.load("superkart_model.joblib")


# ---------------------------------------------------------
# Home endpoint
# ---------------------------------------------------------
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart sales forecasting system"


# ---------------------------------------------------------
# Single prediction endpoint
# ---------------------------------------------------------
@superkart_api.post("/v1/predict")
def predict_sales():

    # Get JSON data from request
    data = request.get_json()

    # Create one sample with the features expected by the model
    sample = {
        "Product_Weight": data["Product_Weight"],
        "Product_Sugar_Content": data["Product_Sugar_Content"],
        "Product_Allocated_Area": data["Product_Allocated_Area"],
        "Product_MRP": data["Product_MRP"],
        "Store_Size": data["Store_Size"],
        "Store_Location_City_Type": data["Store_Location_City_Type"],
        "Store_Type": data["Store_Type"],
        "Product_Id_char": data["Product_Id_char"],
        "Store_Age_Years": data["Store_Age_Years"],
        "Product_Type_Category": data["Product_Type_Category"]
    }

    # Convert the single record into a DataFrame
    input_data = pd.DataFrame([sample])

    # Predict sales
    prediction = model.predict(input_data)[0]

    # Return prediction
    return jsonify({
        "Sales": round(float(prediction), 2)
    })


# ---------------------------------------------------------
# Batch prediction endpoint
# ---------------------------------------------------------
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():

    # Get uploaded CSV file
    file = request.files["file"]

    # Read CSV into DataFrame
    input_data = pd.read_csv(file)

    # Generate predictions for all rows
    predictions = model.predict(input_data)

    # Create response
    output_dict = {
        str(i): round(float(pred), 2)
        for i, pred in enumerate(predictions)
    }

    return jsonify(output_dict)


# ---------------------------------------------------------
# Run Flask application
# ---------------------------------------------------------
if __name__ == "__main__":
    superkart_api.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
