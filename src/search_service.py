from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
alias_name = "searchable_books"

def search(query='', f={}):
    return es.search(index=alias_name, aggregations=addAggs(), q=query)

def addAggs():
    aggregations = {}
    aggregations['rating'] = {'terms': {'field': 'friendly_rating', "order": { "_key": "desc" }}}
    aggregations['minYear'] = {'min': {'field': 'published_year'}}
    aggregations['maxYear'] ={'max': {'field': 'published_year'}}
    return aggregations

# es.search(index=alias_name, query={'bool': {'filter': [{ "range": { "published_year": { "gte": 2015 }}}]}})
