import configparser
from typing import Dict, Union
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel
import requests
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


def getCountries(input_text: str) -> Union[str, Dict]:
    """
    Calls the countries API with the provided user query converted to appropriate odata query and returns the json response to get details of required countries.

    Args:
      input_text: The user query to be used in the API call.

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
    Example 1:
    User Query: I need details of all the countries starting in alphabetic order    
    Output: $orderby=countryName
    Example 2:
    User Query: I need to find countryId for United States
    Output: $filter=countryName eq 'United States'
    Example 3:
    User Query: I need to get countries starting with letter p
    Output: $filter=startswith(tolower(countryName), 'p')
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
    
    Example 1
    User Query: Show me all data values.
    OData Query: $orderBy=value asc
    
    Example 2
    User Query: Retrieve data values for product with ID 1.
    OData Query: $filter=productID eq 1
    
    Example 3
    User Query: Retrieve data values between ID 1 and ID 5.
    OData Query: $filter=dataValueID ge 1 and dataValueID le 5
    
    Example 4
    User Query: Show me data values with value 18029.678.
    OData Query: $filter=value eq 18029.678
    
    Example 5
    User Query: Fetch data values for country with ID 1 and product with ID 1.
    OData Query: $filter=countryID eq 1 and productID eq 1
    
    Example 6
    User Query: Show me data values for country with ID 1, product with ID 1, and year with ID 1.
    OData Query: $filter=countryID eq 1 and productID eq 1 and yearID eq 1
    
    Example 7
    User Query: Retrieve data values with value greater than 500.
    OData Query: $filter=value gt 500
    
    Example 8
    User Query: All productions from country with countryId 36 and order by ascending value
    OData Query: $filter=countryID eq 36 and $orderBy=value asc
    
    Example 9
    User Query: Get sum of Values by country
    OData Query: $apply=groupby((CountryID), aggregate(Value with sum as TotalValue))
    
    Example 10
    User Query: Get sum of Values for country id 3
    Odata Query: $apply=groupby((CountryID), aggregate(Value with sum as TotalValue)) & $filter=CountryID eq 3
    
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

    Given
    User Query: 
    """
    + input_text 
    + """
    OData Query: 
    """)
    
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8
    )

    try:
        odataQuery = model.generate_content(prompt, generation_config=generation_config)
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

        return response_data

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occured while making api request: {e}")
        return f"Error retrieving values data: {str(e)}"
