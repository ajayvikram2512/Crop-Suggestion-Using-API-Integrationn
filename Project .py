#!/usr/bin/env python
# coding: utf-8

# # SOIL QUALITY PREDICTION AND CROP SUGGESTION

# In[33]:


import requests
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Import the Dataset
data = pd.read_csv("C:/Users/Data Analyst/OneDrive/Desktop/soil_data.csv")

# Create a DataFrame
df = pd.DataFrame(data)

# Train a decision tree model
X = df[['pH', 'N', 'P', 'K', 'organic_matter']]
y = df['soil_type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

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

# Main function to run the program
def main():
    print("Please enter the following soil characteristics (ranges provided):")
    pH = float(input("pH level of the soil (Range: 3.5 to 9.0): "))
    nitrogen = float(input("Nitrogen (N) content in ppm (Range: 0 to 200): "))
    phosphorus = float(input("Phosphorus (P) content in ppm (Range: 0 to 100): "))
    potassium = float(input("Potassium (K) content in ppm (Range: 0 to 500): "))
    organic_matter = float(input("Organic matter percentage (Range: 0 to 10%): "))

    # Collect soil data
    soil_data = {
        'pH': pH,
        'N': nitrogen,
        'P': phosphorus,
        'K': potassium,
        'organic_matter': organic_matter
    }

    # Calculate soil type based on input
    soil_type = calculate_soil_score(soil_data)
    print(f"\nCalculated Soil Type: {soil_type}")
    
    # Options for climate and crop type
    climate_options = ["Tropical", "Temperate", "Arid", "Continental", "Polar"]
    print("\nSelect the climate type by entering the index value:")
    for index, option in enumerate(climate_options):
        print(f"{index}: {option}")
    climate_index = int(input("Enter index (0-4): "))
    climate = climate_options[climate_index]

    crop_type_options = ["Vegetables", "Fruits", "Grains", "Legumes", "Flowers"]
    print("\nSelect the type of crops by entering the index value:")
    for index, option in enumerate(crop_type_options):
        print(f"{index}: {option}")
    crop_type_index = int(input("Enter index (0-4): "))
    crop_type = crop_type_options[crop_type_index]
    
    # New API Key
    api_key = "AIzaSyARio43zlnz6k1pyK96tPQ8QY-AMro-8Dg"
    
    # Fetch crop suggestions based on input
    crop_suggestions = suggest_crops(soil_type, climate, crop_type, api_key)
    
    # Print the suggestions from the Gemini API
    print("\nCrop Suggestions from Gemini API based on {} soil in {} climate for {}:".format(soil_type, climate, crop_type))
    
    if isinstance(crop_suggestions, dict) and 'candidates' in crop_suggestions:
        for candidate in crop_suggestions['candidates']:
            print(candidate['content']['parts'][0]['text'])
    else:
        print(crop_suggestions)
        
if __name__ == "__main__":
    main()


# In[ ]:




