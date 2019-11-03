import requests
import csv
import sqlite3
import pandas as pd
import fire
import threading


class Movie(object):

    def __init__(self):
        self.header = ['Id', 'Title', 'Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country',
              'Awards', 'imdbRating', 'imdbVotes', 'BoxOffice']
        self.columns = ['Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country', 'Awards',
                   'imdbRating', 'imdbVotes', 'BoxOffice']
        self.file_to_open = 'movies.csv'
        threading.Thread.__init__(self)

    def fill_csv_file(self):
        with open(self.file_to_open) as csv_file:
            csv_f = csv.reader(csv_file, delimiter=',')
            index = 2
            output = []
            for row in csv_f:
                for j in self.columns:
                    if row[1] != 'title':
                        r = requests.get('http://www.omdbapi.com/?apikey=d2558cde&t=' + row[1])
                        data = r.json()
                        if j == "Runtime":
                            row[index] = data[j].replace('min', '')
                        elif j == 'BoxOffice' and row[1] != 'Ben Hur':
                            row[index] = data[j].replace('$', '')
                        elif j == 'BoxOffice' and row[1] == 'Ben Hur':
                            row[index] = "0"
                        else:
                            row[index] = data[j]
                        index = index + 1
                        if index == 14:
                            index = 2
                output.append(row)
        with open(self.file_to_open, "w", encoding="utf-8", newline="") as f:
            file = csv.writer(f)
            file.writerows(output)

    def add(self, film_title):
        with open(self.file_to_open) as csv_f:
            csv_file = csv.reader(csv_f, delimiter=',')
            row_count = len(list(csv_file))
            row = [row_count - 1, film_title]
            for j in self.columns:
                r = requests.get('http://www.omdbapi.com/?apikey=d2558cde&t=' + film_title)
                data = r.json()
                if j == "Runtime":
                    data[j] = data[j].replace('min', '')
                elif j == 'BoxOffice':
                    data[j] = data[j].replace('$', '')
                row.append(data[j])
        with open(self.file_to_open, "a+", encoding="utf-8", newline="") as csv_f:
            file = csv.writer(csv_f)
            file.writerow(row)

    def compare(self, title1, title2, to_compare):
        if self.check_column_name(to_compare):
            with open(self.file_to_open) as csv_file:
                csv_f = csv.reader(csv_file, delimiter=',')
                if to_compare != 'Awards':
                    for row in csv_f:
                        if row[1] == title1:
                            value1 = row[self.header.index(to_compare)]
                            value1_int = value1.replace(',', '')
                            if value1 == 'N/A':
                                value1_int = 0
                            if to_compare != 'imdbRating':
                                value1_int = int(value1_int)
                            else:
                                value1_int = float(value1_int)
                        elif row[1] == title2:
                            value2 = row[self.header.index(to_compare)]
                            value2_int = value2.replace(',', '')
                            if value2 == 'N/A':
                                value2_int = 0
                            if to_compare != 'imdbRating':
                                value2_int = int(value2_int)
                            else:
                                value2_int = float(value2_int)
                else:
                    for row in csv_f:
                        if row[1] == title1:
                            value1 = row[self.header.index(to_compare)]
                            list1 = value1.split(' ')
                            if 'wins' in list1:
                                pos = list1.index('wins')
                                value1_int = int(list1[pos - 1])
                            else:
                                value1_int = 0
                        elif row[1] == title2:
                            value2 = row[self.header.index(to_compare)]
                            list2 = value2.split(' ')
                            if 'wins' in list2:
                                pos = list2.index('wins')
                                value2_int = int(list2[pos - 1])
                            else:
                                value2_int = 0
            if value1_int > value2_int:
                print('Comparison result = > The film ' + title1 + ': ' + value1)
                return 'Comparison result = > The film ' + title1 + ': ' + value1
            elif value1_int < value2_int:
                print('Comparison result => The film ' + title2 + ': ' + value2)
                return 'Comparison result => The film ' + title2 + ': ' + value2
            else:
                print('Comparison result = > equal')
                return 'Comparison result = > equal'
        else:
            print("Invalid column name")

    def sort_col(self, column):
        output = []
        with open(self.file_to_open) as csv_file:
            csv_f = csv.reader(csv_file, delimiter=',')
            next(csv_f)
            if self.check_column_name(column):
                for row in csv_f:
                    output.append(tuple((row[1], row[self.header.index(column)])))
                output = list(output)
                output1 = []
                for k, j in output:
                    if j == "N/A" or j == "":
                        j = "0"
                    j = j.replace(",", "")
                    output1.append(tuple((k, j)))
                if column == "BoxOffice" or column == "Year" or column == "Runtime" or column == 'imdbVotes':
                    sortedlist = sorted(output1, key=lambda x: int(x[1]), reverse=True)
                elif column == 'imdbRating':
                    sortedlist = sorted(output1, key=lambda x: float(x[1]), reverse=True)
                else:
                    sortedlist = sorted(output1, key=lambda x: x[1])
                output = [i for i in sortedlist]
                print(pd.DataFrame(output))
            else:
                print("Invalid column name")

    def sort_multiple_col(self, column, column2):
        output = []
        with open(self.file_to_open) as csv_file:
            csv_f = csv.reader(csv_file, delimiter=',')
            next(csv_f)
            if self.check_column_name(column) and self.check_column_name(column2):
                for row in csv_f:
                    output.append(tuple((row[1], row[self.header.index(column)], row[self.header.index(column2)])))
                output = list(output)
                output1 = []
                for k, j, l in output:
                    if j == "N/A" or j == "":
                        j = "0"
                    if l == "N/A" or l == "":
                        l = "0"
                    j = j.replace(",", "")
                    l = l.replace(",", "")
                    output1.append(tuple((k, j, l)))
                if column == "BoxOffice" or column == "Year" or column == "Runtime" or column == 'imdbVotes':
                    type_1 = int
                elif column == 'imdbRating':
                    type_1 = float
                else:
                    type_1 = str
                if column2 == "BoxOffice" or column2 == "Year" or column2 == "Runtime" or column2 == 'imdbVotes':
                    type_2 = int
                elif column2 == 'imdbRating':
                    type_2 = float
                else:
                    type_2 = str
                sortedlist = sorted(output1, key=lambda x: (type_1(x[1]), type_2(x[2])), reverse=True)
                output = [i for i in sortedlist]
                print(pd.DataFrame(output))
            else:
                print("Invalid column name")

    def filter_by(self, column, value):
        csv_f = pd.read_csv(self.file_to_open)
        output = {('title', column)}
        if column != 'box_office' and column != 'awards':
            for index, row in csv_f.iterrows():
                if value in str(row[column]):
                    output.update([(row['title'], row[column])])
            output = [i for i in output if i[0] != 'title']
            print(pd.DataFrame(output))
        else:
            print("wrong column")
        return output

    def filter_earn_money(self):
        output = {('title', 'box_office')}
        with open(self.file_to_open) as csv_file:
            csv_f = csv.reader(csv_file, delimiter=',')
            for row in csv_f:
                if row[1] != 'title':
                    if row[self.header.index('BoxOffice')] == "N/A":
                        row[self.header.index('BoxOffice')] = 0
                    row[self.header.index('BoxOffice')] = str(row[self.header.index('BoxOffice')]).replace(',', '').replace('"', '')
                    value = str(row[self.header.index('BoxOffice')])
                    if len(value) >= len('100000000'):
                        output.update([(row[1], row[self.header.index('BoxOffice')])])
            output = [i for i in output if i[0] != 'title']
            print(pd.DataFrame(output))

    def filter_nominations(self, win_80, only_nominated):
        output = {('title', 'awards')}
        with open(self.file_to_open) as csv_file:
            csv_f = csv.reader(csv_file, delimiter=',')
            if only_nominated:
                for row in csv_f:
                    if 'Nominated' in row[self.header.index('Awards')]:
                        if 'Oscars' in row[self.header.index('Awards')]:
                            output.update([(row[1], row[self.header.index('Awards')])])
            elif win_80:
                for row in csv_f:
                    list = row[self.header.index('Awards')].split(' ')
                    if 'nominations' in row[self.header.index('Awards')]:
                        pos = list.index('nominations.')
                        nominations = list[pos-1]
                        if 'wins' in row[self.header.index('Awards')]:
                            pos2 = list.index('wins')
                            wins = list[pos2-1]
                            if int(wins)/int(nominations)*100 > 80:
                                output.update([(row[1], row[self.header.index('Awards')])])
        output = [i for i in output if i[0] != 'title']
        print(pd.DataFrame(output))

    def highscores(self):
        output = {('column', 'title', 'value')}
        out = out1 = out2 = out3 = out4 = 0
        out5 = "0"
        with open(self.file_to_open) as csv_file:
            csv_f = csv.reader(csv_file, delimiter=',')
            next(csv_f)
            rows = [3, 13]
            for row in csv_f:
                row[rows[0]] = row[rows[0]].replace(',', '')
                if row[rows[0]] == "N/A" or row[rows[0]] == "":
                    row[rows[0]] = "0"
                value = int(row[rows[0]])
                if out < value:
                    out = value
                    title = row[1]
                row[rows[1]] = row[rows[1]].replace(',', '')
                if row[rows[1]] == "N/A" or row[rows[1]] == "":
                    row[rows[1]] = "0"
                value1 = int(row[rows[1]])
                if out1 < value1:
                    out1 = value1
                    title1 = row[1]
                list = row[self.header.index('Awards')].split(' ')
                if 'nominations' in row[self.header.index('Awards')]:
                    pos = list.index('nominations.')
                    nominations = int(list[pos - 1])
                    if out2 < nominations:
                        out2 = nominations
                        title2 = row[1]
                    if 'wins' in row[self.header.index('Awards')]:
                        pos2 = list.index('wins')
                        wins = int(list[pos2 - 1])
                        if out3 < wins:
                            out3 = wins
                            title3 = row[1]
                if 'Won' in row[self.header.index('Awards')]:
                    pos3 = list.index('Won')
                    oscars = int(list[pos3 + 1])
                    if out4 < oscars:
                        out4 = oscars
                        title4 = row[1]
                if row[self.header.index('imdbRating')] == "N/A":
                    row[self.header.index('imdbRating')] = 0
                row[self.header.index('imdbRating')] = row[self.header.index('imdbRating')].replace(" ", '')
                rating = row[self.header.index('imdbRating')]
                if out5 < rating:
                    out5 = rating
                    title5 = row[1]
            output.update([("runtime", out, title)])
            output.update([("box_office", out1, title1)])
            output.update([("nominations", out2, title2)])
            output.update([("wins", out3, title3)])
            output.update([("oscars", out4, title4)])
            output.update([("imdbRating", out5, title5)])
            output = [i for i in output if i[0] != 'column']
            print(pd.DataFrame(output))

    def csv_to_sqlite(self):
        con = sqlite3.connect("sql.sl3")
        cur = con.cursor()
        cur.execute("CREATE TABLE t (ID, TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, CAST, WRITER, LANGUAGE, COUNTRY, AWARDS, IMDB_RATING, IMDB_VOTES, BOX_OFFICE);")
        with open('movies.csv', 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['title'], i['year'], i['runtime'], i['genre'], i['director'], i['cast'], i['writer'], i['language'], i['country'], i['awards'], i['imdb_rating'], i['imdb_votes'], i['box_office']) for i in dr]
        cur.executemany("INSERT INTO t (ID, TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, CAST, WRITER, LANGUAGE, COUNTRY, AWARDS, IMDB_RATING, IMDB_VOTES, BOX_OFFICE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        con.close()

    def check_column_name(self, column):
        if column in self.header:
            return 1
        else:
            return 0


if __name__ == '__main__':
    fire.Fire(Movie)


