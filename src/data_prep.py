import json

# Open and read the JSON file
with open('./data/formattedBooks.json', 'r') as file:
    data = json.load(file)

# Print the data
print(f"ingested: {len(data)} books")

{'isbn13': 9780002005883, 'isbn10': '0002005883', 'title': 'Gilead', 'subtitle': '', 'authors': 'Marilynne Robinson', 'categories': 'Fiction', 'thumbnail': 'http://books.google.com/books/content?id=KQZCPgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 'description': 'A NOVEL THAT READERS and critics have been eagerly anticipating for over a decade, Gilead is an astonishingly imagined story of remarkable lives. John Ames is a preacher, the son of a preacher and the grandson (both maternal and paternal) of preachers. It’s 1956 in Gilead, Iowa, towards the end of the Reverend Ames’s life, and he is absorbed in recording his family’s story, a legacy for the young son he will never see grow up. Haunted by his grandfather’s presence, John tells of the rift between his grandfather and his father: the elder, an angry visionary who fought for the abolitionist cause, and his son, an ardent pacifist. He is troubled, too, by his prodigal namesake, Jack (John Ames) Boughton, his best friend’s lost son who returns to Gilead searching for forgiveness and redemption. Told in John Ames’s joyous, rambling voice that finds beauty, humour and truth in the smallest of life’s details, Gilead is a song of celebration and acceptance of the best and the worst the world has to offer. At its heart is a tale of the sacred bonds between fathers and sons, pitch-perfect in style and story, set to dazzle critics and readers alike.', 'published_year': 2004, 'average_rating': 3.85, 'num_pages': 247, 'ratings_count': 361}

cleanedBooks = []
for book in data:
    newBook = {}
    newBook['_id'] = book['isbn13']
    newBook['full_title'] = str(book['title']) + (f': {book["subtitle"]}' if bool(book['subtitle']) else '')
    newBook['authors'] = book['authors'].split(';')
    newBook['categories'] = book['categories']
    newBook['description'] = book['description']
    newBook['published_year'] = book['published_year']
    newBook['friendly_rating'] = int(float(book.get('average_rating', 0)) + .50) if book['average_rating'] else 0
    newBook['num_pages'] = book['num_pages']
    newBook['ratings_count'] = book['ratings_count']
    newBook['meta']['thumbnail'] = book['thumbnail']
    cleanedBooks.append(newBook)


with open('./data/cleanedBook.json', 'w+') as file:
    json.dump(cleanedBooks, file)

