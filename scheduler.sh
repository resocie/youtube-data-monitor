UPDATE=$(find `pwd` -path "*youtube/update.py")
UPDATE_PATH=$(dirname $UPDATE)
YT_PATH=$(dirname $UPDATE_PATH)
crontab -l | { cat; echo "0 0 * * * cd $YT_PATH && . venv/bin/activate && python -m youtube.update"; } | crontab -
