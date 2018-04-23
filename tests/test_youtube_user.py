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


	def test_has_activities(self):
		channelId = 'UCj34AOIMl_k1fF7hcBkD_dw'
		maxResults = '5'
		result = self.user.get_activitie_info(channelId,maxResults)
		self.assertTrue(result['items'])

	def test_has_video(self):
		id = 'V6OvM-0SGUU'
		maxResults = '5'
		result = self.user.get_videos_info(id,maxResults)
		self.assertTrue(result['items'])

	def test_channel_id(self):
		userID = 'UCsCI7wlAwbzTPK55yVaX2Ig'
		result = self.user.get_channel_info(userID)
		id = self.user.get_channel_id(result)
		self.assertEqual('UCsCI7wlAwbzTPK55yVaX2Ig',id)

	def test_all_videos_id(self):
		userID = 'UC9uefWa6TXIPDRWGZYMcTuA'
		maxResults = '5'
		result = self.user.get_channel_info(userID)
		id = self.user.get_channel_id(result)
		result_activities = self.user.get_activitie_info(id,maxResults)
		videos_id = self.user.get_all_videos_ids(result_activities)
		assert_list = ['L14U9aasDek', 'WyggT8Q-MIM', 'EXLN3qXkNpY']
		self.assertEqual(videos_id[0:3],assert_list)

	def test_all_videos_count_userID(self):
		userID = 'UC_77GCFm3isnRD5uGLkEi4A'
		result = self.user.get_channel_info(userID)
		maxResults = 1
		VideoViews = self.user.get_all_Video_Views_user_ID(result,maxResults)
		assert_list=[{'Título':'HIRA - The Roxy Live - 30.03.2018','Número de visualizações':'29'}]
		self.assertEqual(VideoViews[0],assert_list[0])

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
