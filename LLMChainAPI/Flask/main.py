from tools.tools import getProductionValues, formatJson, getCountries
from tools.potterByConfiguration import GetGraphDataFromQuery
import json

user_query = "List all products which made sales more than 5000?"
data = getProductionValues(user_query)
formatteddata = formatJson(data)

# GetGraphDataFromQuery(user_query, data)

queryOutput  = {
    "query": user_query,
    "data": data
    }

jsonnloutput = json.dumps(queryOutput)

print(jsonnloutput)

with open('./training_data/jsonoutputforgraphs.jsonl', 'a') as outfile:
    outfile.write(jsonnloutput + '\n')
    