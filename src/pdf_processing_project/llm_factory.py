import openai
# from llama3 import Llama3Client  # Uncomment if using Llama3
from openai import OpenAI

client = OpenAI() 

class LLMFactory:
    @staticmethod
    def get_llm(model_name, api_key):
        if model_name == "openai":
            #openai.api_key = api_key
            return OpenAIModel()   
           
            #client.api_key=api_key     
            #return client
        elif model_name == "llama3":
            # return Llama3Client(api_key=api_key)  # Uncomment if using Llama3
            pass
        else:
            raise ValueError(f"Unsupported LLM model: {model_name}")

class OpenAIModel:
    def query(self, prompt):
        client_instance = OpenAI(api_key="")
        
        response = client_instance.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
  