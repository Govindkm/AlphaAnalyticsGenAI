import matplotlib.pyplot as plt
import os
import configparser
from typing import Dict, Union
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel
import requests
from os import path

current_dir = path.dirname(__file__)
config = configparser.ConfigParser()
config_file_path = path.join(current_dir, "config.ini")
config.read(config_file_path)

project_id = config.get("DEFAULT", "PROJECT_ID")
location = config.get("DEFAULT", "LOCATION")
model_name = config.get("DEFAULT", "MODEL_NAME")

vertexai.init(project=project_id, location=location)
generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8
)
prompt = """
Given User Query and Data, give python script to create a visualization of the data using python matplotlib library.
Note: Return Python script only. Do not give any text apart from python code.   
Example 1
User Query: 
Give me  top 5 countries with highest production
Data: 
[{"Country":{"CountryName":"United States"},"CountryID":36,"TotalValue":5408956.5},{"Country":{"CountryName":"Canada"},"CountryID":4,"TotalValue":994251.6},{"Country":{"CountryName":"Japan"},"CountryID":18,"TotalValue":846293.44},{"Country":{"CountryName":"Germany"},"CountryID":11,"TotalValue":549666.94},{"Country":{"CountryName":"South Korea"},"CountryID":19,"TotalValue":486178.6}]    

Response:
#python
import matplotlib.pyplot as plt
import os

data = [{"Country":{"CountryName":"United States"},"CountryID":36,"TotalValue":5408956.5},{"Country":{"CountryName":"Canada"},"CountryID":4,"TotalValue":994251.6},{"Country":{"CountryName":"Japan"},"CountryID":18,"TotalValue":846293.44},{"Country":{"CountryName":"Germany"},"CountryID":11,"TotalValue":549666.94},{"Country":{"CountryName":"South Korea"},"CountryID":19,"TotalValue":486178.6}]
# Extract data and sort by total value (descending)
sorted_data = sorted(data, key=lambda x: x["TotalValue"], reverse=True)
top_5_countries = sorted_data[:5]

# Extract country names and total values
country_names = [country["Country"]["CountryName"] for country in top_5_countries]
total_values = [country["TotalValue"] for country in top_5_countries]

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(country_names, total_values, color='royalblue')
plt.xlabel('Country')
plt.ylabel('Total Value')
plt.title('Top 5 Countries with Highest Production')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Get the current visualization number (assuming consecutive numbering)
existing_files = [f for f in os.listdir('.') if f.startswith(filename_prefix) and f.endswith('.png')]
if existing_files:
  highest_num = max(int(f.split('_')[-1].split('.')[0]) for f in existing_files)
  visualization_number = highest_num + 1
else:
  visualization_number = 1

# Generate filename and save the plot
filename = f"{filename_prefix}{visualization_number}.png"
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(filename)
plt.close()  # Close the plot to avoid memory issues with multiple visualizations

print(f"Visualization saved as: {filename}")
"""
model = GenerativeModel(model_name)

def promptGenerator(userquery:str, data:str):
    prompt + f"""
    Given
    User Query: 
    {userquery}
    Data: 
    {data}
    Response:
    """
    return prompt

def getPlottingScript(userquery:str, data: str):
    plotprompt = promptGenerator(userquery, data)
    try:
        script = model.generate_content(prompt, generation_config=generation_config).text
        return script
    except Exception as e:
        print("Error while converting input query to odata query")
        return f"Error creating Odata Query {str(e)}"