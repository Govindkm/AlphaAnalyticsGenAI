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


mockData = """[{'Country': {'CountryName': 'United States'}, 'CountryID': 36, 'TotalValue': 5408956.5},
        {'Country': {'CountryName': 'Canada'}, 'CountryID': 4, 'TotalValue': 994251.6},
        {'Country': {'CountryName': 'Japan'}, 'CountryID': 18, 'TotalValue': 846293.44},
        {'Country': {'CountryName': 'Germany'}, 'CountryID': 11, 'TotalValue': 549666.94},
        {'Country': {'CountryName': 'South Korea'}, 'CountryID': 19, 'TotalValue': 486178.6}]"""
        
def CreateBarChart(data):
    prompt = """
    Based on data provided give Matplot lib configurations in json format creating a Bar Chart
    
    Example 1
    Data: 
    [{'Country': {'CountryName': 'United States'}, 'CountryID': 36, 'TotalValue': 5408956.5},
        {'Country': {'CountryName': 'Canada'}, 'CountryID': 4, 'TotalValue': 994251.6},
        {'Country': {'CountryName': 'Japan'}, 'CountryID': 18, 'TotalValue': 846293.44},
        {'Country': {'CountryName': 'Germany'}, 'CountryID': 11, 'TotalValue': 549666.94},
        {'Country': {'CountryName': 'South Korea'}, 'CountryID': 19, 'TotalValue': 486178.6}]
    
    Configuration:
    {
    "xaxis": {
        "label": "Country",
        "data": ["United States", "Canada", "Japan", "Germany", "South Korea"],
        "size": 10
    },
    "yaxis": {
        "label": "TotalValue",
        "data": [5408956.5, 994251.6, 846293.44, 549666.94, 486178.6],
        "size": 6
    },
    "title": "Total Production by Country",
    "color": "skyblue"
    }
    Given 
    Data:
    """ + data + """
    Configuration: 
    """
    
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=4096, top_k=40, top_p=0.8
    )
    try:
        configurationText = model.generate_content(prompt, generation_config=generation_config).text
        print(configurationText)
        configuration = json.loads(configurationText)
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
    plt.show()
    
        
CreateBarChart(mockData)

