from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
alias_name = "searchable_books"
keep_searching = True
while keep_searching:
    user_search = input("(enter :q! to esc)> Search Bar:\t")
    if user_search == ':q!':
        break
    searchResp = es.search(index=alias_name, q=user_search)
    if searchResp['hits']['total']['value'] > 0:
        print("Fetched these books for you!")
        for book in searchResp['hits']['hits']:
            print('\n-----\n')
            print(f"- {book['_source']['full_title']} by {', '.join(book['_source']['authors'])}")
            print(">> DEBUG", book)
    else:
        print(f"We're fresh out of matches for {user_search}; our apologies!")
