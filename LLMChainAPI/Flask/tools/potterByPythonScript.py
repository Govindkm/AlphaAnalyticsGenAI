import configparser
from typing import Dict, Union
import vertexai
from langchain_community.llms import VertexAI
from langchain.tools import StructuredTool
from langchain_community import agent_toolkits
from vertexai.generative_models import GenerationConfig, GenerativeModel
from langchain_core.tools import tool
import json
import matplotlib.pyplot as plt
from os import path

current_dir = path.dirname(__file__)
config = configparser.ConfigParser()
config_file_path = path.join(current_dir, "..", "config.ini")
config.read(config_file_path)

project_id = config.get("DEFAULT", "PROJECT_ID")
location = config.get("DEFAULT", "LOCATION")
model_name = config.get("DEFAULT", "MODEL_NAME")

base_url = config.get("DEFAULT", "BASE_URL")

vertexai.init(project=project_id, location=location)

model = GenerativeModel(model_name)
generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8
)



mockData = """[{'Country': {'CountryName': 'United States'}, 'CountryID': 36, 'TotalValue': 5408956.5},
        {'Country': {'CountryName': 'Canada'}, 'CountryID': 4, 'TotalValue': 994251.6},
        {'Country': {'CountryName': 'Japan'}, 'CountryID': 18, 'TotalValue': 846293.44},
        {'Country': {'CountryName': 'Germany'}, 'CountryID': 11, 'TotalValue': 549666.94},
        {'Country': {'CountryName': 'South Korea'}, 'CountryID': 19, 'TotalValue': 486178.6}]"""
        
def GetGraphDataFromQuery(query, apiData):
    prompt = """
    Given User Query and Data, give python script to create a visualization of the data using python matplotlib library.
    
    Example 1
    User Query: Give me  top 5 countries with highest production
    Data: 
    [{"Country":{"CountryName":"United States"},"CountryID":36,"TotalValue":5408956.5},{"Country":{"CountryName":"Canada"},"CountryID":4,"TotalValue":994251.6},{"Country":{"CountryName":"Japan"},"CountryID":18,"TotalValue":846293.44},{"Country":{"CountryName":"Germany"},"CountryID":11,"TotalValue":549666.94},{"Country":{"CountryName":"South Korea"},"CountryID":19,"TotalValue":486178.6}]    
    Response:
  
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
    
    Example 2
    User Query: Give top 5 products for the year 2021
    Data:
    [{"Product": {"ProductName": "Total oil products production"}, "ProductID": 9, "TotalValue": 3991038}, {"Product": {"ProductName": "Crude oil"}, "ProductID": 1, "TotalValue": 3085046}, {"Product": {"ProductName": "Gasoline and diesel"}, "ProductID": 6, "TotalValue": 1244947.8}, {"Product": {"ProductName": "Total gas oil production"}, "ProductID": 4, "TotalValue": 1237099.2}, {"Product": {"ProductName": "Total oil production"}, "ProductID": 10, "TotalValue": 961125.75}]
    Response:
    {"configuration":{"xaxis":{"label":"Product","data":["Total oil products production","Crude oil","Gasoline and diesel","Total gas oil production","Total oil production"],"size":10},"yaxis":{"label":"TotalValue in USD in Millions","data":[3991038,3085046,1244947.8,1237099.2,961125.75],"size":6},"title":"Top 5 Products (2021)","color":"blue"}},"type":"barchart"}
    
    Example 3
    User Query:
    
    Given
    User Query:  """ + query + """
    Data:
    """ + apiData + """
    Response: 
    """

    
    
    
        
CreateBarChart(mockData)

