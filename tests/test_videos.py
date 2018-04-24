from youtube.youtube import YoutubeAPI
from youtube.videos import Videos
import unittest

class TestVideos(unittest.TestCase):

    def setUp(self):
        self.video = Videos()
        self.user = YoutubeAPI()

    def test_has_activities(self):
        channelId = 'UCj34AOIMl_k1fF7hcBkD_dw'
        maxResults = '5'
        result = self.video.get_activitie_info(channelId,maxResults)
        self.assertTrue(result['items'])

    def test_has_video(self):
        id = 'V6OvM-0SGUU'
        maxResults = '5'
        result = self.video.get_videos_info(id,maxResults)
        self.assertTrue(result['items'])

    def test_all_videos_id(self):
        userID = 'UC9uefWa6TXIPDRWGZYMcTuA'
        maxResults = '5'
        result = self.user.get_channel_info(userID)
        id = self.user.get_channel_id(result)
        result_activities = self.video.get_activitie_info(id,maxResults)
        videos_id = self.video.get_all_videos_ids(result_activities)
        assert_list = ['L14U9aasDek', 'WyggT8Q-MIM', 'EXLN3qXkNpY']
        self.assertEqual(videos_id[0:3],assert_list)

    def test_all_videos_count_userID(self):
        userID = 'UC_77GCFm3isnRD5uGLkEi4A'
        result = self.user.get_channel_info(userID)
        maxResults = 1
        VideoViews = self.video.get_all_Video_Views_user_ID(result,maxResults)
        assert_list=[{'Título':'HIRA - The Roxy Live - 30.03.2018','Número de visualizações':'29'}]
        self.assertEqual(VideoViews[0],assert_list[0])



if __name__ == '__main__':
    unittest.main()
