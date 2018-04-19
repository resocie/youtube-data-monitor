from youtube.youtube import YoutubeAPI
import unittest

class TestYoutubeAPI(unittest.TestCase):
	def setUp(self):
		self.user = YoutubeAPI()

	def test_has_channel(self):
		id = 'UC9uefWa6TXIPDRWGZYMcTuA'
		result = self.user.get_channel_info(id)
		self.assertTrue(result['items'])

	def test_has_no_channel(self):
		id = 'BC9uefWa6TXIPDRWGZYMcTuA'
		result = self.user.get_channel_info(id)
		self.assertFalse(result['items'])

	def test_get_channel_title_on_channel_valid(self):
		id = 'UC9uefWa6TXIPDRWGZYMcTuA'
		result = self.user.get_channel_info(id)
		title = self.user.get_channel_title(result)
		self.assertEqual('Marina Silva', title)

	def test_get_channel_title_on_channel_invalid(self):
		id = 'BC9uefWa6TXIPDRWGZYMcTuA'
		result = self.user.get_channel_info(id)
		title = self.user.get_channel_title(result)
		self.assertEqual('ERROR: Canal não existe.', title)

	def test_get_channel_total_subscribers_on_channel_valid(self):
		id = 'UCvv3PVl4BnOnozFLjXwYQJQ'
		result = self.user.get_channel_info(id)
		subscribers = self.user.get_channel_subscribers(result)
		self.assertEqual('2', subscribers)

	def test_get_channel_total_video_count(self):
		id = 'UC5ByVewtZ9ZTeft5m3GHtMg'
		result = self.user.get_channel_info(id)
		video_count = self.user.get_channel_video_count(result)
		self.assertEqual('9', video_count)

	def test_get_channel_total_view_count(self):
		id = 'UCsCI7wlAwbzTPK55yVaX2Ig'
		result = self.user.get_channel_info(id)
		view_count = self.user.get_channel_total_view_count(result)
		self.assertGreater(view_count,'120')

if __name__ == '__main__':
    unittest.main()
