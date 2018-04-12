from youtube.youtube import YoutubeUser
import unittest

class TestYoutubeUser(unittest.TestCase):
	def setUp(self):
		self.user = YoutubeUser()

	def test_has_channel(self):
		username = 'msilvaonline'
		result = self.user.get_channel_info(username)
		self.assertTrue(result['items'])

	def test_has_no_channel(self):
		username = 'msilvaonlie'
		result = self.user.get_channel_info(username)
		self.assertFalse(result['items'])

	def test_get_channel_title_on_channel_valid(self):
		username = 'msilvaonline'
		result = self.user.get_channel_info(username)
		title = self.user.get_channel_title(result)
		self.assertEqual('Marina Silva', title)

	def test_get_channel_title_on_channel_invalid(self):
		username = 'msilvaonlin'
		result = self.user.get_channel_info(username)
		title = self.user.get_channel_title(result)
		self.assertEqual('ERROR: Canal não existe.', title)

if __name__ == '__main__':
    unittest.main()
