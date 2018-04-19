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
		username = 'patrickvrb'
		result = self.user.get_channel_info(username)
		id = self.user.get_channel_id(result)
		self.assertEqual('UCsCI7wlAwbzTPK55yVaX2Ig',id)

	def test_all_videos_id(self):
		username = 'msilvaonline'
		maxResults = '5'
		result = self.user.get_channel_info(username)
		id = self.user.get_channel_id(result)
		result_activities = self.user.get_activitie_info(id,maxResults)
		videos_id = self.user.get_all_videos_ids(result_activities)
		assert_list = ['L14U9aasDek', 'WyggT8Q-MIM', 'EXLN3qXkNpY']
		self.assertEqual(videos_id[0:3],assert_list)

	def test_all_videos_count_userID(self):
		userID = 'UC_77GCFm3isnRD5uGLkEi4A'
		maxResults = 1
		VideoViews = self.user.get_all_Video_Views_user_ID(userID,maxResults)
		assert_list=[{"Paradox - Ariel Garcia":'200'}]
		self.assertEqual(VideoViews[0],assert_list[0])

	def test_get_channel_total_view_count(self):
		username = 'patrickvrb'
		result = self.user.get_channel_info(username)
		view_count = self.user.get_channel_total_view_count(result)
		self.assertGreater(view_count,'120')

if __name__ == '__main__':
    unittest.main()
