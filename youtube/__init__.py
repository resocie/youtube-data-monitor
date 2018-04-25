# import logging
# import os
# import sys
#
# LEVEL = logging.DEBUG
# # LEVEL = logging.INFO
# LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#
# log = logging.getLogger()
# log.setLevel(LEVEL)
#
# output = logging.StreamHandler(sys.stdout)
# output.setLevel(LEVEL)
# output.setFormatter(logging.Formatter(LOG_FORMAT))
# log.addHandler(output)
#
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
# logging.getLogger("selenium").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("google_auth_httplib2").setLevel(logging.WARNING)
# logging.getLogger("googleapiclient").setLevel(logging.WARNING)

__all__ = ['update', 'videos', 'youtube']

from youtube.youtube import YoutubeAPI
