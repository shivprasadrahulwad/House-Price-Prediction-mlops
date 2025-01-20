import streamlit as st
import json
import requests
import pandas as pd

def predict_house_price(input_features):
    # URL of the MLflow prediction server
    url = "http://127.0.0.1:8000/invocations"
    
    # Prepare input data
    input_data = {
        "dataframe_records": [input_features]
    }
    
    # Convert to JSON
    json_data = json.dumps(input_data)
    
    # Set headers
    headers = {"Content-Type": "application/json"}
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=json_data)
        
        if response.status_code == 200:
            prediction_value = response.json()
            
            # Extract the first prediction from the response
            if isinstance(prediction_value, dict) and 'predictions' in prediction_value:
                return prediction_value['predictions'][0]
            else:
                return "Error: Unexpected response format"
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the MLflow server. Please make sure it's running."
    except json.JSONDecodeError:
        return f"Error: Invalid JSON response from server: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("House Price Prediction")
    st.write("Enter the house details below to get a price prediction")
    
    # Create input fields for features
    col1, col2 = st.columns(2)
    
    with col1:
        ms_subclass = st.number_input("MS SubClass", value=20)
        lot_frontage = st.number_input("Lot Frontage", value=80.0)
        lot_area = st.number_input("Lot Area", value=9600)
        overall_qual = st.slider("Overall Quality", 1, 10, 5)
        overall_cond = st.slider("Overall Condition", 1, 10, 7)
        year_built = st.number_input("Year Built", value=1961)
        year_remod = st.number_input("Year Remodeled", value=1961)
        mas_vnr_area = st.number_input("Masonry Veneer Area", value=0.0)
        bsmtfin_sf_1 = st.number_input("Basement Finished SF 1", value=700.0)
        bsmtfin_sf_2 = st.number_input("Basement Finished SF 2", value=0.0)
        
    with col2:
        bsmt_unf_sf = st.number_input("Basement Unfinished SF", value=150.0)
        total_bsmt_sf = st.number_input("Total Basement SF", value=850.0)
        first_flr_sf = st.number_input("First Floor SF", value=856)
        second_flr_sf = st.number_input("Second Floor SF", value=854)
        gr_liv_area = st.number_input("Above Ground Living Area", value=1710.0)
        bsmt_full_bath = st.number_input("Basement Full Bathrooms", value=1)
        bsmt_half_bath = st.number_input("Basement Half Bathrooms", value=0)
        full_bath = st.number_input("Full Bathrooms", value=1)
        half_bath = st.number_input("Half Bathrooms", value=0)
        bedroom_abvgr = st.number_input("Bedrooms Above Ground", value=3)
    
    # Create input dictionary
    input_features = {
        "Order": 1,
        "PID": 5286,
        "MS SubClass": ms_subclass,
        "Lot Frontage": lot_frontage,
        "Lot Area": lot_area,
        "Overall Qual": overall_qual,
        "Overall Cond": overall_cond,
        "Year Built": year_built,
        "Year Remod/Add": year_remod,
        "Mas Vnr Area": mas_vnr_area,
        "BsmtFin SF 1": bsmtfin_sf_1,
        "BsmtFin SF 2": bsmtfin_sf_2,
        "Bsmt Unf SF": bsmt_unf_sf,
        "Total Bsmt SF": total_bsmt_sf,
        "1st Flr SF": first_flr_sf,
        "2nd Flr SF": second_flr_sf,
        "Low Qual Fin SF": 0,
        "Gr Liv Area": gr_liv_area,
        "Bsmt Full Bath": bsmt_full_bath,
        "Bsmt Half Bath": bsmt_half_bath,
        "Full Bath": full_bath,
        "Half Bath": half_bath,
        "Bedroom AbvGr": bedroom_abvgr,
        "Kitchen AbvGr": 1,
        "TotRms AbvGrd": 7,
        "Fireplaces": 2,
        "Garage Yr Blt": year_built,
        "Garage Cars": 2,
        "Garage Area": 500.0,
        "Wood Deck SF": 210.0,
        "Open Porch SF": 0,
        "Enclosed Porch": 0,
        "3Ssn Porch": 0,
        "Screen Porch": 0,
        "Pool Area": 0,
        "Misc Val": 0,
        "Mo Sold": 5,
        "Yr Sold": 2010,
    }
    
    if st.button("Predict Price"):
        # Get prediction
        prediction = predict_house_price(input_features)
        
        # Display prediction
        st.subheader("Predicted House Price")
        if isinstance(prediction, str) and prediction.startswith("Error"):
            st.error(prediction)
        elif prediction is not None:
            try:
                # Format prediction as currency
                st.success(f"${float(prediction):,.2f}")
            except (TypeError, ValueError) as e:
                st.error(f"Error formatting prediction: {prediction} ({str(e)})")
        else:
            st.error("No prediction received from the model")
            
        # Display input features
        st.subheader("Input Features")
        st.write(pd.DataFrame([input_features]))

if __name__ == "__main__":
    main()