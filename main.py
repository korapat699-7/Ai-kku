
import os  
import base64
from openai import AzureOpenAI  



# endpoint = os.getenv("ENDPOINT_URL", "https://ai-korapatseedamarts3335ai740227246567.openai.azure.com/")  
# deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")  
# subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")  


endpoint = "https://ai-korapatseedamarts3335ai740227246567.cognitiveservices.azure.com/openai/deployments/gpt-35-turbo"
deployment = "gpt-35-turbo"
subscription_key = "AkKXLqebVy8r1ZoYitLx3KjPxHRiWSL7FGSyN1g6pRamAsQUS2XtJQQJ99BBACHYHv6XJ3w3AAAAACOG2XtG"


# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)
    
    

#Prepare the chat prompt 
chat_prompt = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
]

    
# Include speech result if speech is enabled  
messages = chat_prompt  
    
# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,
    messages=messages,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False
)

print(completion.to_json())  
    