# Movie

This script fills the sample data source with data from the OMDb API and operates on them.

## Description of functions:
#### -- Fill csv file with data
To fill 'movie.csv' file with data from the OMDb API run
```sh
$ python movies.py fill_csv_file
```
#### -- Add movies to data source
To add new movie to file 'movie.csv' run
```sh
$ python movies.py add <film_title>
```
#### -- Compare two films
To compare films by IMDb Rating, Box office earnings, Number of awards won, Runtime run
```sh
$ python movies.py compare <film_title1> <film_title2> <what_to_compare>
```
Field <what_to_compare> can take one of these values: 'imdbRating', 'BoxOffice', 'Awards', 'Runtime'.

#### -- Sort movies by columns
Run this to sort movies by one of this column 'Id', 'Title', 'Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country', 'Awards', 'imdbRating', 'imdbVotes', 'BoxOffice'
```sh
$ python movies.py sort_col <column>
```

#### -- Sort movies by multiple columns
To sort movies by multiple columns run
```sh
$ python movies.py sort_multiple_col <column1> <column2>
```
That function first compares movies by <column1>, and if those values are identical it then compares them by <column2>.

#### -- Filter movies by
To filter movie by column 'Director', 'Actors', 'Language' run
```sh
$ python movies.py filter_by <column> <value>
```
Field <column> can take one of these values: 'directors', 'actors', 'language'

#### -- Filter movies by earn money
To filter movie that earned more than 100,000,000 $ run
```sh
$ python movies.py filter_earn_money
```

#### -- Filter movies by nominations
To filter movies that won more than 80% of nominations or that was nominated  for Oscar but did not win any run
```sh
$ python movies.py filter_nominations <win_80> <only_nominated>
```
To get movies that won more than 80% of nominations, specify the win_80 to be 1 and only_nominated to be 0. 
To get movies that was nominated  for Oscar but did not win any, specify the win_80 to be 0 and only_nominated to be 1.

#### -- Show current highscores
To show current highscores in Runtime, Box office earnings, Most awards won, Most nominations, Most Oscars, Highest IMDB Rating run
```sh
$ python movies.py highscores
```

#### -- Import a CSV File Into an SQLite Table
Run
```sh
$ python movies.py csv_to_sqlite
```

#### -- Check column name
To chcek if given column name is valid run
```sh
$ python movies.py check_column_name <column>
```

## Test
The basic way to run tests:
```sh
$ python test.py
```


