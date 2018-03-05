import unittest
from youtube.youtube import YoutubeUser

class TestYoutubeUser(unittest.TestCase):
	def test_isonline(self):
		user = YoutubeUser('msilvaonline')

	@classmethod
	def setUpClass(cls):
		cls.user = YoutubeUser('msilvaonline')

	def test_name_retrieval(self):
		self.assertEqual('Marina Silva', TestYoutubeUser.user.name)

	def test_id_retrieval(self):
		self.assertEqual('9999', TestYoutubeUser.user.id)

	def test_view_count_retrieval(self):
		self.assertEqual('4247314', TestYoutubeUser.user.view_count)
		
if __name__ == '__main__':
    unittest.main()