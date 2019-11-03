import unittest
import movies


class MyTestCase(unittest.TestCase):
    def test_colums_compare(self):
        o = movies.Movie()
        self.assertEqual(o.compare('Se7en','Memento', 'imdbRating'), "Comparison result = > The film Se7en: 8.6")
        self.assertEqual(o.compare('Green Book','Fargo', 'Year'), 'Comparison result = > The film Green Book: 2018')
        self.assertEqual(o.compare('Inception','Blade Runner', 'Runtime'), 'Comparison result = > The film Inception: 148 ' )
        self.assertEqual(o.compare('Jurassic Park','Room', 'Awards'), 'Comparison result => The film Room: Won 1 Oscar. Another 103 wins & 136 nominations.')
        self.assertEqual(o.compare('Coco','The Hunt', 'BoxOffice'), 'Comparison result = > The film Coco: 208,487,719')

    def test_filter_by(self):
        o = movies.Movie()
        output = [('The Usual Suspects', 'Bryan Singer')]
        self.assertEqual(o.filter_by('director','Bryan Singer'), output)

if __name__ == '__main__':
    unittest.main()

