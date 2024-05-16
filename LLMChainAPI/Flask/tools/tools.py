import configparser
from typing import Dict, Union
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel
from vertexai.language_models import TextGenerationModel
import requests
from os import path
import json
import re
from langchain.llms import vertexai as langchainvertexai
from langchain.tools import StructuredTool
from langchain.agents import AgentType, initialize_agent, load_tools

from .potterByConfiguration import GetGraphDataFromQuery
from .CopyFileToTestData import saveJson

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


def getCountries(input_text: str) -> Union[str, Dict]:
    """
    Calls the countries API to get list of all countries. Do provide other details input query apart from countryId and CountryName

    Args:
      input_text: The user query to be used in the API call. Query should only be limited to countries details as this api works on country table which has details CountryID and CountryName only.

    Returns:
      The raw API response in json format if request is successful. Error message string if API request fails.
    """
    # ... (Optional) Preprocess the user query before making the API call
    # For example, extract relevant keywords or entities
    prompt = (
        """Given OData supported {base_url}/countries API get endpoint returns countries data json in the format with countryId and countryName. 
    Return odata query if required based on user query. 
    Here is an example of API response:
    [
        {
        "countryId": 1,
        "countryName": "Australia"
        },
        {
            "countryId": 2,
            "countryName": "Austria"
        },
        {
            "countryId": 3,
            "countryName": "Belgium"
        }
    ]
    User Query: """
        + input_text
        + """
    Output: 
    """
    )
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8
    )
    try:
        odataQuery = model.generate_content(prompt, generation_config=generation_config)
    except Exception as e:
        print("Error while converting input query to odata query")
        return f"Error creating Odata Query {str(e)}"

    print(odataQuery.text)
    # Construct the API request URL (you can modify based on API requirements)
    url = f"{base_url}/api/countries?{odataQuery.text}"  # Replace with appropriate URL structure
    # Build the request headers (add API key if provided)
    print(url)
    # ... Use appropriate library (e.g., requests) to make the API call
    # Replace with your preferred library and error handling

    try:
        jsonData = requests.get(url, verify=False)
    except (requests.exceptions.RequestException, ValueError) as e:
        print("Error occured while making api request: {e}")
        return f"Error retrieving countries data: {str(e)}"

    # ... Parse the API response based on its format (JSON, text, etc.)
    # You can use libraries like `json` or custom parsing logic

    response_data = (
        jsonData.text
    )  # ... (parsed response data)  # Replace with actual parsing

    return response_data


def getProducts(input_text: str) -> Union[str, Dict]:
    """
    Calls the products API with the provided user query converted to appropriate odata query and returns the JSON response to get details of required products.

    Args:
        input_text: The user query to be used in the API call.

    Returns:
        The raw API response in JSON format if request is successful. Error message string if API request fails.
    """

    # ... (Optional) Preprocess the user query before making the API call
    # For example, extract relevant keywords or entities
    prompt = (
        """Given OData supported {base_url}/products API get endpoint returns products data json in the format with productId and productName. 
          Return odata query if required based on user query. 
          Here is an example of API response:
          [
              {
                  "productId": 1,
                  "productName": "Crude oil"
              },
              {
                  "productId": 2,
                  "productName": "Liquified Petroleum Gas"
              },
              {
                  "productId": 3,
                  "productName": "Naphtha"
              }
          ]
          Example 1:
          User Query: I need details of all the products
          Output: $orderby=productName
          Example 2:
          User Query: I need details for product with name Liquified Petroleum Gas
          Output: $filter=productName eq 'Liquefied Petroleum Gas'
          Example 3:
          User Query: Give me details of all the products which is made out of petrol.
          Output: $filter=contains(tolower(productName),'petrol')
          User Query: """
        + input_text
        + """
          Output: 
          """
    )
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8
    )

    try:
        odataQuery = model.generate_content(prompt, generation_config=generation_config)
    except Exception as e:
        print("Error while converting input query to odata query")
        return f"Error creating Odata Query {str(e)}"

    print(odataQuery.text)

    # Construct the API request URL (you can modify based on API requirements)
    url = f"{base_url}/api/products?{odataQuery.text}"  # Replace with appropriate URL structure

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Parse the JSON response
        response_data = response.json()

        return response_data

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occured while making api request: {e}")
        return f"Error retrieving products data: {str(e)}"


def getYears() -> Union[str, Dict]:
    """
    Calls the Years API and returns the JSON response containing year data.

    Returns:
        The raw API response in JSON format if request is successful. Error message string if API request fails.
    """

    # Assuming the Years API has a specific endpoint (replace with actual URL)
    url = f"{base_url}/api/years"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Parse the JSON response
        years_data = response.json()

        return years_data

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occured while making api request to Years API: {e}")
        return f"Error retrieving years data: {str(e)}"


def getFlows(input_text: str) -> Union[str | Dict]:
    """Calls Flows API to get flows data based on user query.
    Args:
        input_text (str): User query to be used to create Odata filters

    Returns:
        Union[str | Dict]: The raw API response in JSON format if request is successful. Error message string if API request fails.
    """

    prompt = (
        """Given OData supported {base_url}/flows API get endpoint returns flows data json in the format with productId and productName. 
          Return odata query if required based on user query. 
          Here is an example of API response:
        [
            {
                "flowId": 1,
                "flowName": "Industrial Production"
            },
            {
                "flowId": 2,
                "flowName": "Net Deliveries"
            },
            {
                "flowId": 3,
                "flowName": "Consumption Pattern"
            },
            {
                "flowId": 4,
                "flowName": "Storage Channelization"
            }
        ]
        
          Example 1:
          User Query: I need details of all the flows
          Output: $orderby=flowName
          Example 2:
          User Query: I need details for flows with name Industrial Production
          Output: $filter=flowName eq 'Consumption Pattern'
          
          Given
          User Query: """
        + input_text
        + """
        Output: 
          """
    )
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8
    )

    try:
        odataQuery = model.generate_content(prompt, generation_config=generation_config)
    except Exception as e:
        print("Error while converting input query to odata query")
        return f"Error creating Odata Query {str(e)}"

    print(odataQuery.text)

    # Construct the API request URL (you can modify based on API requirements)
    url = f"{base_url}/api/flows?{odataQuery.text}"  # Replace with appropriate URL structure

    print(url)

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Parse the JSON response
        response_data = response.json()

        return response_data

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occured while making api request: {e}")
        return f"Error retrieving flows data: {str(e)}"


def getProductionValues(input_text: str) -> Union[str | Dict]:
    """Gets production details from values API for given query.

    Args:
        input_text (str): User query for production values details.

    Returns:
        Union[str | Dict]: The raw API response in JSON format if request is successful. Error message string if API request fails.
    """
    
    prompt = ("""
    Given Odata supported API {base_url}/values get endpoint which returns values data in json format with given example values
    Example values: 
    {
    "dataValueID": 1,
    "countryID": 1,
    "productID": 1,
    "flowID": 1,
    "yearID": 1,
    "value": 18029.678
    },
    {
    "dataValueID": 2,
    "countryID": 2,
    "productID": 1,
    "flowID": 1,
    "yearID": 1,
    "value": 561.852
    } 
    where amount is in USD.
    
    Return an OData Query based on user input if required. 
    Remove any delimiters around answer such as "```"
    
    Here are some examples: 
    Example 1
    User Query: Show me all data values.
    OData Query: $top=20&$orderBy=Value asc
    
    Example 2
    User Query: Retrieve data values for product with ID 1.
    OData Query: $filter=ProductID eq 1
    
    Example 3
    User Query: Retrieve data values between ID 1 and ID 5.
    OData Query: $filter=DataValueID ge 1 and DataValueID le 5
    
    Example 4
    User Query: Show me data values with value 18029.678.
    OData Query: $filter=Value eq 18029.678
    
    Example 5
    User Query: Fetch data values for country with ID 1 and product with ID 1.
    OData Query: $filter=CountryID eq 1 and ProductID eq 1
    
    Example 6
    User Query: Show me data values for country with ID 1, product with ID 1, and year with ID 1.
    OData Query: $filter=CountryID eq 1 and ProductID eq 1 and YearID eq 1
    
    Example 7
    User Query: Retrieve data values with value greater than 500.
    OData Query: $filter=Value gt 500
    
    Example 8
    User Query: All productions from country with countryId 36 and order by ascending value
    OData Query: $filter=CountryID eq 36 and $orderBy=Value asc
    
    Example 9
    User Query: Get sum of Values by country
    OData Query: $apply=groupby((CountryID), aggregate(Value with sum as TotalValue))
    
    Example 10
    User Query: Get sum of Values for country id 3
    Odata Query: $apply=groupby((CountryID, Country/CountryName), aggregate(Value with sum as TotalValue)) & $filter=CountryID eq 3
    
    Example 11
    User Query: Get sum of values for the product with id 2
    Odata Query: $apply=groupby((ProductID), aggregate(Value with sum as TotalValue)) & $filter=ProductID eq 2
    
    Example 12
    User Query: Get all the sales made by country United States
    Odata Query: $expand=product&$filter=tolower(Country/CountryName) eq 'United States'&$orderby=CountryID,ProductID
    
    Example 13
    User Query: Get the sales of the product which Spain sells the most.
    Odata Query: $apply=filter(tolower(Country/CountryName) eq 'spain')/groupby((ProductID, Product/ProductName, Country/CountryName), aggregate(Value with sum as TotalValue))&$orderby=TotalValue desc&$top=1
    
    Example 14
    User Query: Which products does United States sells.
    Odata Query: $apply=filter(tolower(Country/CountryName) eq 'united states')/groupby((ProductID, Product/ProductName), aggregate(Value with sum as TotalValue))&$orderby=TotalValue desc
    
    Example 15
    User Query: Give all products total sales yearwise.
    Odata Query: $apply=groupby((ProductID, YearID, Year/YearValue), aggregate(Value with sum as TotalValue))&$orderby=ProductID asc, YearID asc
    
    Example 16
    User Query: How much sales did United States had in the year 2023?
    Odata Query: $apply=filter(tolower(Country/CountryName) eq 'united states')/groupby((YearID, Year/YearValue), aggregate(Value with sum as TotalValue))&$filter=Year/YearValue eq 2023&$orderby=YearID asc
    
    Example 17
    User Query: Give last 5 products for the year 2021.
    Odata Query: $apply=filter(Year/YearValue eq 2021)/groupby((ProductID, Product/ProductName), aggregate(Value with sum as TotalValue))&$orderby=TotalValue asc&$top=5
    
    Example 18
    User Query: Prime Minister of India
    Odata Query: ERROR: I do not have any knowledge on outside world apart from oil production data.
    
    Example 18
    User Query: I want to know about Democracy.
    Odata Query: ERROR: Sorry I can only provide details about oil production data.
    
    Example 19
    User Query: give data for total sales Australia, Japan, United States, United Kingdom, Turkey oil production data for year 2022.
    Odata Query: $apply=filter(tolower(Country/CountryName) eq 'australia' or tolower(Country/CountryName) eq 'japan' or tolower(Country/CountryName) eq 'united states' or tolower(Country/CountryName) eq 'united kingdom' or tolower(Country/CountryName) eq 'turkey')/groupby((CountryID, Country/CountryName, Year/YearValue), aggregate(Value with sum as TotalValue))&$filter=Year/YearValue eq 2022&$orderby=TotalValue desc
    
    Example 20
    User Query: give data for last 3 countries by sale value
    Odata Query: $apply=groupby((CountryID, Country/CountryName), aggregate(Value with sum as TotalValue))&$orderby=TotalValue asc&$top=3
    
    Given
    User Query: 
    """
    + input_text 
    + """
    OData Query: 
    """)
    
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=2048, top_k=40, top_p=0.8
    )

    try:
        odataQuery = model.generate_content(prompt, generation_config=generation_config)
        pattern = r'\bERROR\b'
        if re.search(pattern, odataQuery.text):
            print(f"Error in odata query: {odataQuery.text}")
            saveJson({"error": odataQuery.text})
            return {"Result": odataQuery.text}
    except Exception as e:
        print("Error while converting input query to odata query")
        return f"Error creating Odata Query {str(e)}"
    
    print(odataQuery.text)
    
    url = f"{base_url}/api/values?{odataQuery.text}"  # Replace with appropriate URL structure
    
    print(url)
    
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        # Parse the JSON response
        response_data = response.json()
        GetGraphDataFromQuery(input_text, response_data)
        
        saveJson(response_data)
        
        response_data
        
        
        return response_data

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occured while making api request: {e}")
        return f"Error retrieving values data: {str(e)}"
    
def formatJson(input_text: object) -> Union[str | Dict]:
    prompt = """
    Given the json data remove the ID fields from the data and reformat it in json.
    Example:
    data: {"Product": {"ProductName": "Total oil products production"}, "ProductID": 9, "MaxValue": 790672.44}
    output: {"Product": "Tota; oil products production", "MaxValue": 790672.44"}
    
    data: {"CountryID": 1, "Country": {"CountryName": "United States"}, "ProductID": 3 "Product": {"ProductName": "Indian Oil"}}
    output: {"Country": "United States", "Product": "Indian Oil"}
    
    Given
    data: 
    """ + json.dumps(input_text) + """
    output: 
    """    
    data = model.generate_content(prompt).text
    
    print(json.dumps(data))
    return json.dumps(data)

def getSummary(user_query: str, input_data: str) -> Union[str | Dict]:
    """Uses the data fetched and returns the summary based on user query.

    Args:
        user_query (str): string representing the user query
        input_data (str): string containing the data fetched from odataapis

    Returns:
        Union[str | Dict]: string representing summary of the data which user query generated.
    """
    prompt = f"""Given user query and input data as input for that input give details of the data and provide a summary of the data in natural language as output. 
    Input:
    user_query: {user_query}
    input_data: {input_data}
    Output
    Details of Data: 
    Natural language Explanation: 
    """
    # text_model = TextGenerationModel.from_pretrained("text-bison")
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=2048, top_k=40, top_p=0.8
    )       
    summary = model.generate_content(prompt, generation_config=generation_config).text
    return summary

def CreateBarChart(data: str):
    """Creates a bar chart for the data provided in text

    Args:
        data (str): Text data to be used for creating bar graph
    """
    prompt = """
    Given data extract data out of it and respond in json format.
    Example 1:
    given this data:
    {"type":"bar","data":{"x":["Canada","Japan","Mexico","United States"],"y":[994251.6,846293.44,436448.12,5408956.5]},"options":{"title":"Country-wise Revenue for 2021","xlabel":"Country","ylabel":"Revenue ($)"}}       
    response:
    Total Revenue for the year 2021:** $7,742,199.66
    **Country-wise Revenue for the year 2021:**
    - Canada: $994,251.6
    - Japan: $846,293.44
    - Mexico: $436,448.12
    - United States: $5,408,956.5"
    
    **Summary**
    Here's a summary of the data in a way that's easy to understand for someone unfamiliar with the oil market:
    In the year 2021, the total revenue was $7,742,199.66. That's a lot of money! Here's a breakdown of where that money came from:
    The United States was the biggest spender, contributing over half ($5,408,956.50) of the total revenue.
    Canada came in second place, spending almost $1 million ($994,251.60).
    Japan spent around $846,293.44.
    Mexico contributed $436,448.12.
    
    Basically, the United States was the biggest customer, followed by Canada, Japan, and Mexico.  These countries likely bought some kind of product or service, but it wasn't oil in this case! 
    """

def processWithReAct(user_query: str):
    """Uses Reasoning and Action prompts to process user query

    Args:
        user_query (str): returns nothing
    """
    structuredtools = [StructuredTool.from_function(getProductionValues)]

    llm = langchainvertexai.VertexAI(model_name="text-bison", max_output_tokens=2048)

    agent = initialize_agent(structuredtools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, return_intermediate_steps = True)
    data = agent(user_query)
    output =  getSummary(user_query, data)
    output = f"""**Data**\n
    {data}
    \n
    {output}
    
    """
    response = {"summary": output, "data": f"{data}"}
    return response
    # Placeholder code to process the user query and retrieve data
    # Here, you would implement your logic to obtain data from various APIs or sources
    
    
    
    # Placeholder data for demonstration
    data_from_country_api = [...]  # Data obtained from the country API
    data_from_value_api = [...]    # Data obtained from the value API
    data_from_flow_api = [...]     # Data obtained from the flow API
    images_data = [...]            # Image URLs or data
    summary_text = "Placeholder text summary of data obtained"
    table_id = "tableid"          # Placeholder table ID
    
    # Determine the status based on whether data retrieval was successful
    status = "success"  # or "fail" based on actual logic
    
    # Construct the JSON response
    response = {
        "status": status,
        "summary": summary_text,
        "data": {
            "countryapi": data_from_country_api,
            "valueapi": data_from_value_api,
            "flowapi": data_from_flow_api
        },
        "images": images_data,
        "tableid": table_id
    }
    
    return response



def sanitize_output(text: str) -> str:
    # Strip whitespace and any potential backticks enclosing the code block
    text = text.strip()
    regex = re.compile(r"^\s*```(\w+)?|```\s*$")
    text = regex.sub("", text).strip()

    return text