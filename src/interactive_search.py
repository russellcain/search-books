from search_service import search 

keep_searching = True
while keep_searching:
    user_search = input("(enter :q! to esc)> Search Bar:\t")
    if user_search == ':q!':
        break
    searchResp = search(user_search)
    print(">> DEBUG", searchResp)
    if searchResp['hits']['total']['value'] > 0:
        print("Fetched these books for you!")
        for book in searchResp['hits']['hits']:
            print('\n-----\n')
            print(f"- {book['_source']['full_title']} by {', '.join(book['_source']['authors'])}")
    else:
        print(f"We're fresh out of matches for {user_search}; our apologies!")
