import os
import logging

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


class YoutubeUser:

	CLIENT_SECRETS_FILE = "client_secret.json"
	SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
	API_SERVICE_NAME = 'youtube'
	API_VERSION = 'v3'

	def get_authenticated_service(self):
	  flow = InstalledAppFlow.from_client_secrets_file(YoutubeUser.CLIENT_SECRETS_FILE, YoutubeUser.SCOPES)
	  credentials = flow.run_console()
	  return build(YoutubeUser.API_SERVICE_NAME, YoutubeUser.API_VERSION, credentials=credentials)

	def __init__(self,username):
		service = self.get_authenticated_service()

		part = 'id,snippet,contentDetails,statistics'
		channel = service.channels().list(part=part, forUsername=username).execute()['items'][0]

		# logging.debug('channel=%s' % channel)

		self.id = channel['id']
		self.username = 'neymar'
		self.name = channel['snippet']['title']
		self.view_count = channel['statistics']['viewCount']
