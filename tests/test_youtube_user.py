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
        subscribers = int(self._user.get_channel_subscribers(result))
        self.assertTrue(subscribers > 0 and subscribers < 10)

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

    def test_get_channel_total_comment_count(self):
        channel_id = 'UCsCI7wlAwbzTPK55yVaX2Ig'
        result = self._user.get_channel_info(channel_id)
        comment_count = self._user.get_channel_total_comment_count(result)
        self.assertGreaterEqual(comment_count, '0')
        self.assertLessEqual(comment_count, '5')

    def test_get_channel_creation_date(self):
        channel_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
        result = self._user.get_channel_info(channel_id)
        channel_date = self._user.get_channel_creation_date(result)
        self.assertEqual(channel_date, '2010-01-26T19:44:02.000Z')

    def test_get_channel_thumbnail(self):
        channel_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
        result = self._user.get_channel_info(channel_id)
        channel_thumbnails = self._user.get_channel_thumbnail(result)
        self.assertEqual(channel_thumbnails, 'https://yt3.ggpht.com/' +
                         '-dKJCCcRJLUM/AAAAAAAAAAI/AAAAAAAAAAA/dPAqpLhWma4/' +
                         's88-c-k-no-mo-rj-c0xffffff/photo.jpg')

    def test_get_channel_description(self):
        channel_id = 'UCs6avCwreiI6QoFR83Ul2UQ'
        result = self._user.get_channel_info(channel_id)
        channel_description = self._user.get_channel_description(result)
        self.assertEqual(channel_description, 'O Instituto Lula foi criado' +
                         ' para ampliar a cooperação' +
                         ' entre Brasil, África e América Latina e dar' +
                         ' continuidade ao trabalho político de Lula.')

    def test_get_channel_keywords(self):
        channel_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
        result = self._user.get_channel_info(channel_id)
        channel_keywords = self._user.get_channel_keywords(result)
        self.assertEqual(channel_keywords, '"nova politica"')

    def test_get_channel_banner(self):
        channel_id = 'UC9uefWa6TXIPDRWGZYMcTuA'
        result = self._user.get_channel_info(channel_id)
        channel_banner = self._user.get_channel_banner(result)
        self.assertEqual(channel_banner, 'https://yt3.ggpht.com/_' +
                         'TMNHFdl76PF7AePJJu6CK384TYDUHxWG2EkqSsS' +
                         '5VBjdC6ZYekK1-H15Lcbna4Kyv2HLsiDexI=w1060' +
                         '-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no')

    def test_is_channel_above_one_hundred_thousand(self):
        channel_id = 'UCvv3PVl4BnOnozFLjXwYQJQ'
        result = self._user.get_channel_info(channel_id)
        subscribers = int(self._user.get_channel_subscribers(result))
        self.assertFalse(self._user.check_above_one_hundred_thousand
                         (subscribers))


if __name__ == '__main__':
    unittest.main()
