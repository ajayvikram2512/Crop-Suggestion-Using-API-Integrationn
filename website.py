#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import requests
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Title for the Streamlit app
st.title("CROP SUGGESTION USING API INTEGRATION")

# Import the Dataset
data = pd.read_csv("C:/Users/Data Analyst/OneDrive/Desktop/soil_data.csv")

# Create a DataFrame
df = pd.DataFrame(data)

# Train a decision tree model
X = df[['pH', 'N', 'P', 'K', 'organic_matter']]
y = df['soil_type']
model = DecisionTreeClassifier()
model.fit(X, y)

# Function to predict soil type
def calculate_soil_score(soil_data):
    score = model.predict(pd.DataFrame([soil_data]))[0]
    return score

# Function to suggest crops using the Gemini API
def suggest_crops(soil_type, climate, crop_type, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Structure the data according to the API format
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Suggest {crop_type} crops that can grow in {soil_type} soil in a {climate} climate."
                    }
                ]
            }
        ]
    }
    
    # Include the API key in the request
    params = {'key': api_key}
    
    # Send the POST request to the API
    response = requests.post(url, headers=headers, json=data, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Streamlit sidebar for input
st.sidebar.header("Input Soil Characteristics")

# Input fields for soil characteristics using normal input boxes
pH = st.sidebar.text_input("pH level of the soil (3.5 to 9.0)", value="7.0")
nitrogen = st.sidebar.text_input("Nitrogen (N) content in ppm (0 to 200)", value="50")
phosphorus = st.sidebar.text_input("Phosphorus (P) content in ppm (0 to 100)", value="30")
potassium = st.sidebar.text_input("Potassium (K) content in ppm (0 to 500)", value="100")
organic_matter = st.sidebar.text_input("Organic matter percentage (0 to 10%)", value="2.0")

# Convert input to float and calculate soil type when button is pressed
if st.sidebar.button("Calculate Soil Type"):
    try:
        soil_data = {
            'pH': float(pH),
            'N': float(nitrogen),
            'P': float(phosphorus),
            'K': float(potassium),
            'organic_matter': float(organic_matter)
        }

        # Calculate soil type based on input
        soil_type = calculate_soil_score(soil_data)
        st.session_state.soil_type = soil_type  # Store the soil type in session state
        st.success(f"Calculated Soil Type: **{soil_type}**")

    except ValueError:
        st.error("Please enter valid numeric values for soil properties.")

# Use stored soil type if available
if 'soil_type' in st.session_state:
    soil_type = st.session_state.soil_type
    st.write(f"Current Soil Type: **{soil_type}**")

    # Options for climate and crop type
    climate_options = ["Tropical", "Temperate", "Arid", "Continental", "Polar"]
    crop_type_options = ["Vegetables", "Fruits", "Grains", "Legumes", "Flowers"]

    # Dropdowns for selecting climate and crop type
    climate = st.selectbox("Select the climate type", climate_options)
    crop_type = st.selectbox("Select the type of crops", crop_type_options)

    # New API Key
    api_key = "AIzaSyARio43zlnz6k1pyK96tPQ8QY-AMro-8Dg"

    # Button to fetch crop suggestions
    if st.button("Get Crop Suggestions"):
        crop_suggestions = suggest_crops(soil_type, climate, crop_type, api_key)

        # Display the crop suggestions from the Gemini API
        st.write(f"Crop Suggestions for {crop_type} crops in {soil_type} soil under {climate} climate:")

        if isinstance(crop_suggestions, dict) and 'candidates' in crop_suggestions:
            for candidate in crop_suggestions['candidates']:
                st.write(candidate['content']['parts'][0]['text'])
        else:
            st.write(crop_suggestions)

else:
    st.info("Please calculate the soil type first.")


# In[ ]:




