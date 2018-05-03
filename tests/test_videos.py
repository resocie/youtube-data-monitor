from youtube.youtube import YoutubeAPI
from youtube.videos import Videos
import unittest


class TestVideos(unittest.TestCase):

    def setUp(self):
        self._video = Videos()
        self._user = YoutubeAPI()

    def test_has_activities(self):
        channel_id = 'UCj34AOIMl_k1fF7hcBkD_dw'
        max_results = '5'
        result = self._video.get_activity_info(channel_id, max_results)
        self.assertTrue(result['items'])

    def test_has_video(self):
        channel_id = 'V6OvM-0SGUU'
        max_results = '5'
        result = self._video.get_videos_info(channel_id, max_results)
        self.assertTrue(result['items'])

    def test_all_video_ids(self):
        user_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
        max_results = '5'
        result = self._user.get_channel_info(user_id)
        channel_id = self._user.get_channel_id(result)
        result_activities = self._video.get_activity_info(channel_id,
                                                          max_results)
        video_ids = self._video.get_all_video_ids(result_activities)
        assert_list = ['L14U9aasDek', 'WyggT8Q-MIM', 'EXLN3qXkNpY']
        self.assertEqual(video_ids[0:3], assert_list)

    def test_all_videos_count_user_id(self):
        user_id = 'UCs6avCwreiI6QoFR83Ul2UQ'
        result = self._user.get_channel_info(user_id)
        max_results = 50
        video_views = self._video.get_all_video_views_user_id(result,
                                                              max_results)
        video_title = video_views[-1]['title']
        self.assertEqual(video_title, 'Dilma e Amorim \
denunciam milícias à mídia internacional')
        video_view = int(video_views[-1]['views'])
        video_url = str(video_views[-1]['url'])
        self.assertGreater(video_view, 524)
        self.assertLess(video_view, 700)
        self.assertEqual(video_url,
                         'https://www.youtube.com/watch?v=zr6J20IR9J0')


if __name__ == '__main__':
    unittest.main()
