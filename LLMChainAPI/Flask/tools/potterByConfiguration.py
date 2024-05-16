import configparser
import re
from typing import Dict, Union
import vertexai
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


mockData = """[{'Country': {'CountryName': 'United States'}, 'CountryID': 36, 'TotalValue': 5408956.5},
        {'Country': {'CountryName': 'Canada'}, 'CountryID': 4, 'TotalValue': 994251.6},
        {'Country': {'CountryName': 'Japan'}, 'CountryID': 18, 'TotalValue': 846293.44},
        {'Country': {'CountryName': 'Germany'}, 'CountryID': 11, 'TotalValue': 549666.94},
        {'Country': {'CountryName': 'South Korea'}, 'CountryID': 19, 'TotalValue': 486178.6}]"""

            
def CreateBarChart(data):
    try:
        configurationText = ("""{
  "xaxis": {
    "label": "Product",
    "data": ["Total oil products production", "Crude oil", "Gasoline and diesel", "Total gas oil production", "Total oil production"],
    "size": 10
  },
  "yaxis": {
    "label": "TotalValue in USD in Millions",
    "data": [3991038, 3085046, 1244947.8, 1237099.2, 961125.75],
    "size": 6
  },
  "title": "Top 5 Products (2021)",
  "color": "blue"
}""")
        configuration=data
    except Exception as e:
        print(f"Error while fetching configuration for the plot {e}")
        return f"Error creating Odata Query {str(e)}"
    
    # Create bar plot
    plt.figure(figsize=(configuration['xaxis']['size'], configuration['yaxis']['size']))
    plt.bar(configuration['xaxis']['data'], configuration['yaxis']['data'], color=configuration['color'])
    plt.xlabel = configuration['xaxis']['label']
    plt.ylabel = configuration['yaxis']['label']
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("plot.png")
    
def GetGraphDataFromQuery(query, apiData):
    prompt = """
    Given User Query and Data, give the suggested graph to use for visualization along with configuration required for plotting it using matplotlib.
    
    Example 1
    User Query: Give me  top 5 countries with highest production
    Data: 
    [{"Country":{"CountryName":"United States"},"CountryID":36,"TotalValue":5408956.5},{"Country":{"CountryName":"Canada"},"CountryID":4,"TotalValue":994251.6},{"Country":{"CountryName":"Japan"},"CountryID":18,"TotalValue":846293.44},{"Country":{"CountryName":"Germany"},"CountryID":11,"TotalValue":549666.94},{"Country":{"CountryName":"South Korea"},"CountryID":19,"TotalValue":486178.6}]    
    Response:
    {"configuration":{"xaxis":{"label":"Country","data":["United States","Canada","Japan","Germany","South Korea"],"size":10},"yaxis":{"label":"TotalValue","data":[5408956.5,994251.6,846293.44,549666.94,486178.6],"size":6},"title":"Total Production by Country","color":"skyblue"},"type":"barchart"}

    Example 2
    User Query: Give top 5 products for the year 2021
    Data:
    [{"Product": {"ProductName": "Total oil products production"}, "ProductID": 9, "TotalValue": 3991038}, {"Product": {"ProductName": "Crude oil"}, "ProductID": 1, "TotalValue": 3085046}, {"Product": {"ProductName": "Gasoline and diesel"}, "ProductID": 6, "TotalValue": 1244947.8}, {"Product": {"ProductName": "Total gas oil production"}, "ProductID": 4, "TotalValue": 1237099.2}, {"Product": {"ProductName": "Total oil production"}, "ProductID": 10, "TotalValue": 961125.75}]
    Response:
    {"configuration":{"xaxis":{"label":"Product","data":["Total oil products production","Crude oil","Gasoline and diesel","Total gas oil production","Total oil production"],"size":10},"yaxis":{"label":"TotalValue in USD in Millions","data":[3991038,3085046,1244947.8,1237099.2,961125.75],"size":6},"title":"Top 5 Products (2021)","color":"grey"},"type":"barchart"}
    
    Given
    User Query:  """ + query + """
    Data:
    """ + f"{apiData}" + """
    Response: 
    """   
    
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=2048, top_k=40, top_p=0.8
    )
    
    try:
      response = model.generate_content(prompt, generation_config=generation_config)
      print(response.text)
      cleaned_response = response.text.strip("```json")
      pattern = r'^.*?\n({.*})'
      match = re.search(pattern, cleaned_response, re.DOTALL)
      if match:
        data = match.group(1)
        print("Cleaned JSON data:", data)      
      json_data = json.loads(data)
      configuration = json_data['configuration']
      CreateBarChart(configuration)
    except Exception as e:
      print(f"Error while getting configurtaion from VertexAI, {e}")
      return

