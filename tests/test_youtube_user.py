from youtube import YoutubeAPI
import unittest


class TestYoutubeAPI(unittest.TestCase):

	def setUp(self):
		self._user = YoutubeAPI()

	def test_has_channel(self):
		channel_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
		result = self._user.get_channel_info(channel_id)
		self.assertTrue(result['items'])

	def test_has_no_channel(self):
		channel_id = 'BC9uefWa6TXIPDRWGZYMcTuA'
		result = self._user.get_channel_info(channel_id)
		self.assertFalse(result['items'])

	def test_get_channel_title_on_channel_valid(self):
		channel_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
		result = self._user.get_channel_info(channel_id)
		title = self._user.get_channel_title(result)
		self.assertEqual('Marina Silva', title)

	def test_raise_value_error_when_get_channel_title_on_channel_invalid(self):
		channel_id = 'BC9uefWa6TXIPDRWGZYMcTuA'
		result = self._user.get_channel_info(channel_id)

		with self.assertRaises(ValueError) as context:
			self._user.get_channel_title(result)

		self.assertTrue('Canal não existe.' in str(context.exception))

	def test_get_channel_id_from_username(self):
		username = 'msilvaonline'
		result = self._user.get_channel_info_by_username(username)
		channel_id = self._user.get_channel_id(result)
		self.assertEqual('UC9uefWa6TXIPDRWGZYMcTuA', channel_id)

	def test_get_channel_total_subscribers_on_channel_valid(self):
		channel_id = 'UCvv3PVl4BnOnozFLjXwYQJQ'
		result = self._user.get_channel_info(channel_id)
		subscribers = self._user.get_channel_subscribers(result)
		self.assertEqual('2', subscribers)

	def test_get_channel_total_video_count(self):
		channel_id = 'UC5ByVewtZ9ZTeft5m3GHtMg'
		result = self._user.get_channel_info(channel_id)
		video_count = self._user.get_channel_video_count(result)
		self.assertEqual('9', video_count)

	def test_get_channel_total_view_count(self):
		channel_id = 'UCsCI7wlAwbzTPK55yVaX2Ig'
		result = self._user.get_channel_info(channel_id)
		view_count = self._user.get_channel_total_view_count(result)
		self.assertGreater(view_count, '120')

if __name__ == '__main__':
    unittest.main()
