import os
import openai
import dotenv


def chat_completion(query):
    dotenv.load_dotenv()

    OPENAI_ENDPOINT = ""
    OPENAI_API_KEY = ""
    OPENAI_DEPLOYMENT_NAME = ""
    OPENAI_API_VERSION = ""

    SEARCH_ENDPOINT = ""
    SEARCH_INDEX = ""
    SEARCH_API_KEY = ""

    
    prompt = f"""
    INSTRUCTION: 
    Search the database to retrieve most relevant units (maximum 5 units) to the following query.
    Only return units with high confidence. The format of each unit is:
    - [unit_code] - [unit_title]
      [unit_link]
    In case you cannot find any relevant units, says you cannot find. Do not make up things.
    
    QUERY: {query}
    
    ANSWER: [Brief about the results]
    [List the units]
    """
    
    client = openai.AzureOpenAI(
        azure_endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY,
        api_version=OPENAI_API_VERSION,
    )

    completion = client.chat.completions.create(
        model=OPENAI_DEPLOYMENT_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt.format(query),
            },
        ],
        extra_body={
            "data_sources":[
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": SEARCH_ENDPOINT,
                        "index_name": SEARCH_INDEX,
                        "authentication": {
                            "type": "api_key",
                            "key": SEARCH_API_KEY,
                        }
                    }
                }
            ],
        }
    )

    print(f"{completion.choices[0].message.role}: {completion.choices[0].message.content}")
    
    return completion.choices[0].message.content
    

if __name__ == '__main__':
    chat_completion("Suggest me some units to learn AI")