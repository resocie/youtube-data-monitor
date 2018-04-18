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

	def test_all_videos_count_username(self):
		username = 'msilvaonline'
		maxResults = 2
		VideoViews = self.user.get_all_Video_Views_Username(username,maxResults)
		assert_list=[{"Temer, Aécio, Renan e cia também precisam ser punidos":'420'},{"Se a escola for boa pra todo mundo, a gente muda a realidade do Brasil":'342'}]
		self.assertEqual(VideoViews,assert_list)

	def test_all_videos_count_userID(self):
		userID = 'UCgzZk2KxLQA8dRciMsI62kg'
		maxResults = 2
		VideoViews = self.user.get_all_Video_Views_user_ID(userID,maxResults)
		assert_list=[{"Montagem Completa Gloster Gladiator Airfix 1/72 parte 4":'348'},{"Montagem completa Gloster Gladiator Airfix 1/72 parte 3":'310'}]
		self.assertEqual(VideoViews,assert_list)

if __name__ == '__main__':
    unittest.main()
