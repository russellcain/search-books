# search-books
Walk through of taking a random dataset (reviews of books) and starting to shape it into a searchable collection.

## Background:

### Our Data:
Illustrating points in the article, we'll be using this public book dataset, courtesy of [Kaggle](https://www.kaggle.com/datasets/abdallahwagih/books-dataset/data). This isn't nearly as unruly as your production-level data likely is, nor does it perfectly match up against every point identified, but it gives us some common footing by which to navigate a couple of the core concepts together. You'll find the pertinent data from that site in our `/data` folder. 

### Our "Infrastructure"
We will be using a local docker instance of elasticsearch to store and search for our data. This requires a working and running instance of Docker. 

You can verify this with:
```
docker -v
> Docker version <version.number>, build <build_slug>
```

We'll be running with elastic's 8.8 version for this duration of this example. You can pull this down with:
```
docker pull elasticsearch:8.8.0
```
and can spin it up with:
```
docker run --rm --name elasticsearch_container -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.8.0
```
which will result in a long-running process in your terminal window. You can verify that your container is up and running by navigating to a separate terminal instance and running `docker ps | grep elastic` and verifying that a result comes back with the `elasticsearch_container` as a name. It'll also mention that it has an accessible port of 9200, so let's make sure we can interact with it at http://localhost:9200/.

Navigating to the above should result in a page (of raw json) with the following:
```
{
  "name" : "13d88b15206c",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "Lxx7pQSeS0-A30GTr1NO3g",
  "version" : {
    "number" : "8.8.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "c01029875a091076ed42cdb3a41c10b1a9a5a20f",
    "build_date" : "-----",
    "build_snapshot" : false,
    "lucene_version" : "9.6.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```
### Stack
For ease of readability / broad popularity, we will be using Python in this repo. Of course, feel free to run with whichever language you prefer. 

Regardless, we'll be working in a virtual env. If you're moving forward with python, run the following to get up and humming:
```
source venv/bin/activate
pip3 install -r requirements.txt
```
This will spin up your virtual environment (you'll begin to see your terminal lines are prefixed by `(venv)`) and download the relevant packages used for this project. I want to keep this as language-agnostic as possible, so I'll be trying to keep the packages used to a minimum. 

## Learning with Our Data
One key point made by the article is a reminder that elasticsearch should not be viewed as a database. As such, let's take a look at our dataset and see which values make sense to include in our search index and which ought to remain behind in our "database" (our simple csv file). 

Here are a few random values (feel free to peruse more) which help us get a sense of the data:

| isbn13 | isbn10 | title | subtitle | authors | categories | thumbnail | description | published_year | average_rating | num_pages | ratings_count |
| :----------------: | :------: | :-------: | :----: | :----: | :-----: | :----: | :----: | :----: | :----: | :----: | :----: |
| 9780006163831 | 0006163831 | The One Tree | | Stephen R. Donaldson | American fiction | http://books.google.com/books/content?id=OmQawwEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api | Volume Two of Stephen Donaldson's acclaimed second trilogy featuing the compelling anti-hero Thomas Covenant. | 1982 | 3.97 | 479 | 172 |
9780006551812| 0006551815 | 'Tis | A Memoir | Frank McCourt | Ireland | http://books.google.com/books/content?id=Q3BhQgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api | "FROM THE PULIZER PRIZE-WINNING AUTHOR OF THE #1 ""NEW YORK TIMES"" BESTSELLER ""ANGELA'S ASHES"" Frank McCourt's glorious childhood memoir, ""Angela's Ashes, "" has been loved and celebrated by readers everywhere. It won the National Book Critics Circle Award, the ""Los Angeles Times"" Book Award and the Pulitzer Prize. Rarely has a book so swiftly found its place on the literary landscape. And now we have ""'Tis, "" the story of Frank's American journey from impoverished immigrant to brilliant teacher and raconteur. Frank lands in New York at age nineteen and gets a job at the Biltmore Hotel, where he immediately encounters the vivid hierarchies of this ""classless country,"" and then is drafted into the army and is sent to Germany to train dogs and type reports. It is Frank's incomparable voice that renders these experiences spellbinding. When Frank returns to America in 1953, he works on the docks, always resisting what everyone tells him. He knows that he should be getting an education, and though he left school at fourteen, he talks his way into New York University. There, he falls in love with the quintessential Yankee and tries to live his dream. But it is not until he starts to teach that Frank finds his place in the world."| 2000 |3.68 | 495 | 44179 |
| 9780007158522 | 0007158521 | Oh, the Places You'll Go! |  | Dr. Seuss | Adventure stories | http://books.google.com/books/content?id=Ev4Llq5fv4IC&printsec=frontcover&img=1&zoom=1&source=gbs_api | From bang-ups and hang-ups to lurches and slumps. Dr. Seuss takes a hilarious look at the mishaps and misadventures that life may have in store for us. | 2003 | 4.35 | 48 | 926 |
| 9780030420566 | 0030420563 | "Rest, Rabbit, Rest"| | Jacquelyn Reinach;Richard Hefter | Juvenile Fiction | http://books.google.com/books/content?id=8-40_Zrp5voC&printsec=frontcover&img=1&zoom=1&source=gbs_api | Rabbit's schedule keeps him so busy his friends have to trick him into resting.| 1978 | 4.01 | 32 | 88 |
 
Formatting tables in markdown is not my forte so let's leave it there, for now. What we can see is that our data, though fairly uniform, is a bit sprawling. For instance, there is no set convention about the length of the description value. We can see that it can include references to books we haven't yet read, noisy reviews from certain publications before mentioning the plot, or can be a rather short tagline of what we have in store. Further, we see that there are two identifier fields (an `isbn13` and an `isbn10`), both of which are surely useful should we wan't to find references to these pieces elsewhere (perhaps if we wanted to include integration with a user's local library and want to check availability), but most readers don't walk around with these identifiers in their pockets, nor at their fingertips while searching. The same could be said for the thumbnails, whereas these might be fun for a display layer, they are not necessary values by which to search. An example of a pitfall for these is the fact that `zoom` is a property of some of these links, but I'd bet most searchers would be befuddled and upset should they be met with a book about "all the places you'll go" when searching for Zoom etiquette tips upon deciding they'll be staying home for the next little bit. As such, I vote that we, to start, remove some of these noisier fields.

Of the values we want to keep, I'd also vote we normalize our author field a bit. What we see in the last record is that multiple authors can collaborate on a book, with their names being separated by a semicolon. This is all well and good, but we want our data to remain flexible for our users and we shouldn't put the onus of knowing whether collaboration occured on them. As such, this is a prime candidate for making the authors field an array of values (many of which will just include one value). 

Additionally, we'll meet our users where they are at by following the "stars" convention for ratings. Though we have more precise values at our disposal (i.e. `4.35` for Dr. Suess' work), we'll break this continuous field (all values from 0.00 to 5.00) into a finite enumeration of 0, 1, 2, 3, 4, or 5 stars. Again, this might seem like an odd choice to make, losing two added places of certainty in how good a rating is, but we are transforming data back down into values which are loosely agreeable for our users. Rephrased, if I were to be having a conversation with a friend in which their review of a book was "yeah, pretty good", my brain loosely translates that into 3 stars, not 3.37 points out of a possible 5. Less precise, ideally more useable. In contrast, we'll want to keep the publishing years as they are, versus grouping by decade, as years are a conventionally accepted continium. 

One last note on our data: we see that we have a sparsely populated column, `subtitle`. Given this value is optionally populated, we don't want to always rely on it being there and base our whole search around it, but recognize that it does lend us context about the book so we don't want to do away with it altogether. As such, I vote we make a search-only field called `full_title` which is a concatenation of `title, subtitle`. This decision is also made due to a feeling that books which have subtitles are not innately different from ones which do not have that. If, instead, we knew that only academic papers were the only works allowed to have this field populated, we'd want to keep it around as a flag to help preserve that unique property.  

## Loading Our Data

I went ahead and did the loose data formatting mentioned above to generate `./data/cleanedBooks.json` for us. We'll be pulling those values and sticking them into elastic as they are. 

If we run our data loading script (`python3 src/data_loader.py`) and give it a second or two to whir away, we'll see that we have an index populated with `6607` books. We used the `isbn` number to be our unique doc identifier in elastic, bringing a sensibily unique constraint from the our domain into our data reflection layer which makes sense within the context of any eventual implementation (re: lookup book in user's local library). 

This is a very quick and rudimentary approach to ingesting our data, but serves our purposes. Once faced with millions of records, you'll want to structure a more efficient batch indexing process, but for our measley little library, this will only take us a few seconds. 

## First Search

To give us a quick sense of our bare search, let's run `python3 src/interactive_search.py` and type in `dog` when prompted to do so.

The random assortment of results we get back help illustrate the need for tuning in our algorithm, as well as some flaws in our data that escaped us on a first pass! For example, we need to address how we want to serve up a book when we don't know the author. Depending on the strictness of your library, you might want to get rid of all such records in the spirit of completeness of data or you might recognize that you still have an isbn and enough about the book to recommend it to an eager reader. 


## Filters
