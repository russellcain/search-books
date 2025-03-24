from flask import Flask, json, request
from flask_cors import CORS, cross_origin
from search_service import search 

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)
CORS(api)

@api.route('/search', methods=['GET'])
@cross_origin(origin='*')
def get_companies():
    print("hit search", request.args)
    search_terms = request.args.get('q') or ''
    min_year = request.args.get('min_year')
    max_year = request.args.get('max_year')
    rating = request.args.get('rating')
    searchResp = search(search_terms)
    print(f"SEARCH RESPONSE FOR {search_terms}: ", searchResp)
    preppedBooks = []
    for bookDoc in searchResp['hits']['hits']:
        preppedBooks.append({
            'id': bookDoc['_source']['isbn'],
            'title': bookDoc['_source']['full_title'],
            'authors': bookDoc['_source']['authors'],
            'publisher': [], # implement,
            'year': bookDoc['_source']['published_year'],
            'rating': bookDoc['_source']['friendly_rating'],
            'full_rating': bookDoc['_source']['meta']['rating'],
            'description': bookDoc['_source']['description'],
            'coverArt': bookDoc['_source']['meta']['thumbnail']
        })
    return preppedBooks
    

if __name__ == '__main__':
    api.run()
