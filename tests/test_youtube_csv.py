from youtube.youtube import YoutubeAPI
import unittest
import os

class TestYoutubeCSV(unittest.TestCase):

    def test_generate_youtube_csv(self):
        csv = YoutubeAPI().generate_csv()
        self.assertTrue(csv)

    def test_clean_youtube_csv(self):
        csv = YoutubeAPI().generate_csv(clean=True)
        self.assertTrue(csv)

    # def test_insert_actors(self):
    #     csv = YoutubeAPI().generate_csv()
    #     self.assertTrue(csv.insert(header='atores', data=data))

if __name__ == '__main__':
    unittest.main()
