from elasticsearch import Elasticsearch

# Set the Elasticsearch URL
es_url = "http://192.168.0.1:9200"

# Initialize Elasticsearch
es = Elasticsearch(es_url)

# Check if the connection is successful
try:
    if es.ping():
        print("Connected to Elasticsearch!")
    else:
        print("Could not connect to Elasticsearch.")
except Exception as e:
    print(f"Connection error: {e}")
