#!/usr/bin/env python

import psycopg2
import psycopg2.extras
import os
import pprint

#------------------------------README------------------------------
# edit dbconnstring with your own postgres credentials
# edit media_root with your data folder location 
#------------------------------------------------------------------

dbconnstring = "host=127.0.0.1 dbname=mattermost user=mattermost_user password=password"
media_root = "/opt/mattermost/data/"

#get all db referenced files.
dbconn = psycopg2.connect(dbconnstring)
cur = dbconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
cur.execute("SELECT unnest(ARRAY[path, thumbnailpath, previewpath]) FROM fileinfo")

db_files = cur.fetchall()
db_files = set([val
  for sublist in db_files
  for val in sublist
])
#pprint.pprint(db_files)

# get paths of physical files.
fs_files = set()
for relative_root, dirs, files in os.walk(media_root):
  for file_ in files:   #Compute the relative file path to the media directory, so it can be compared to the values from the db
        relative_file = os.path.join(os.path.relpath(relative_root, media_root), file_)
        fs_files.add(relative_file)
#pprint.pprint(fs_files)

# diff files and(show info to) delete them
diff_files = fs_files - db_files
del_files = [f
  for f in diff_files
  if not f.startswith('users/')
]
#pprint.pprint(del_files)

# delete, the flagged as deleted files
if del_files:
  for file_ in del_files:
        print('rm "' + os.path.join(media_root, file_) + '"')
        #comment out the line below to do a dry run
        os.remove(os.path.join(media_root, file_))

# delete all empty folders
for relative_root, dirs, files in os.walk(media_root, topdown = False):
  for dir_ in dirs:
        if not os.listdir(os.path.join(relative_root, dir_)):
                print('rmdir "' + os.path.join(relative_root, dir_) + '"')
                #comment out the line below to do a dry run
                os.rmdir(os.path.join(relative_root, dir_))
