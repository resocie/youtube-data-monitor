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

	def test_get_channel_total_subscribers_on_channel_valid(self):
		username = 'Dayofanne'
		result = self.user.get_channel_info(username)
		subscribers = self.user.get_channel_subscribers(result)
		self.assertEqual('2', subscribers)

	def test_has_activities(self):
		channelId = 'UCj34AOIMl_k1fF7hcBkD_dw'
		result = self.user.get_activitie_info(channelId)
		self.assertTrue(result['items'])

	def test_has_video(self):
		id = 'V6OvM-0SGUU'
		result = self.user.get_videos_info(id)
		self.assertTrue(result['items'])

	def test_channel_id(self):
		username = 'patrickvrb'
		result = self.user.get_channel_info(username)
		id = self.user.get_channel_id(result)
		self.assertEqual('UCsCI7wlAwbzTPK55yVaX2Ig',id)

	def test_all_videos_id(self):
		username = 'msilvaonline'
		result = self.user.get_channel_info(username)
		id = self.user.get_channel_id(result)
		result_activities = self.user.get_activitie_info(id)
		videos_id = self.user.get_all_videos_ids(result_activities)
		assert_list = ['L14U9aasDek', 'WyggT8Q-MIM', 'EXLN3qXkNpY']
		self.assertEqual(videos_id[0:3],assert_list)

	def test_all_videos_count(self):
		username = 'BlogdoEveraldo'
		result = self.user.get_channel_info(username)
		id = self.user.get_channel_id(result)
		result_activities = self.user.get_activitie_info(id)
		videos_id = self.user.get_all_videos_ids(result_activities)
		VideoViews = self.user.get_all_Videoviews(videos_id)
		assert_list = ['58', '95'] #Estão sujeitos a alterações
		self.assertEqual(VideoViews[-2:], assert_list)

if __name__ == '__main__':
    unittest.main()
