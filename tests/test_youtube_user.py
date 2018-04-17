from youtube.youtube import YoutubeAPI
import unittest

class TestYoutubeAPI(unittest.TestCase):
	def setUp(self):
		self.user = YoutubeAPI()

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

	def test_get_channel_total_subscribers_on_channel_valid(self):
		username = 'Dayofanne'
		result = self.user.get_channel_info(username)
		subscribers = self.user.get_channel_subscribers(result)
		self.assertEqual('2', subscribers)

	def test_get_channel_total_view_count(self):
		username = 'patrickvrb'
		result = self.user.get_channel_info(username)
		view_count = self.user.get_channel_total_view_count(result)
		self.assertGreater(view_count,'120')

if __name__ == '__main__':
    unittest.main()
