import json

cleanDataPath = './data/cleanedBook.json'  # expected to run this file from root
# Open and read the JSON file
with open(cleanDataPath, 'r') as file:
    data = json.load(file)

# Print the data
print(f"ingested: {len(data)} books")

from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
print(f"Connected to our local elasticsearch instance! Elastic Version: {es.info()['version']['number']}")

# let's make a simple index for our data
index_name = "books_first_pass"
alias_name = "searchable_books"

# make sure we have a clean env:
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Create index with alias
es.indices.create(index=index_name, aliases={alias_name: {}})

# and confirm both the index and alias exist:
print("Index exists?", es.indices.exists(index=index_name))
print("Alias exists?", es.indices.exists(index=alias_name))

# so now let's throw it all in elastic! 
# Note: ideally we'd do a batch write, but this should be quick enough
print("Beginning our indexing..")
for book in data:
    es.index(index=index_name, body=book, id=book['isbn'])


print(f"indexed {es.count(index=index_name)['count']} books for you")
