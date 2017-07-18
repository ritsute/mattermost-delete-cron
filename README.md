# mattermost-delete-cron
Actually delete data from db and remove files in Mattermost, instead of just flagging it as deleted

```
chmod +x file-system-cleaner.py db-cleaner.py
./db-cleaner.py
./file-system-cleaner.py
```

file-system-cleaner.py is dependent on db-cleaner.py so the order of the script is important.

