#!/usr/bin/env python

import psycopg2
import psycopg2.extras

#------------------------------README------------------------------
# edit dbconnstring with your own postgres credentials
# comment out dbconn.commit() to test the script without making changes to your database 
#------------------------------------------------------------------

dbconnstring = "host=127.0.0.1 dbname=mattermost user=mattermost_user password=password"
dbconn = psycopg2.connect(dbconnstring)

# delete channels flagged as deleted
cur = dbconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
cur.execute("DELETE FROM posts where channelid in (SELECT id FROM channels where deleteat <> 0)")
print("Deleted " + str(cur.rowcount) + " 'deleted' channel post(s).")
cur.execute("DELETE FROM channelmembers WHERE channelid in (SELECT id FROM channels WHERE deleteat <> 0)")
print("Deleted " + str(cur.rowcount) + " 'deleted' channel member(s).")
cur.execute("DELETE FROM channels WHERE deleteat <> 0")
print("Deleted " + str(cur.rowcount) + " 'deleted' channel(s).")
dbconn.commit()
print("* committed")

# delete posts flagged as deleted
cur = dbconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
cur.execute("DELETE FROM posts where deleteat <> 0")
print("Deleted " + str(cur.rowcount) + " 'deleted' post(s).")
dbconn.commit()
print("* committed")

# remove orphaned files records from db, file-system-cleaner.py compares existing files in './data' against the db 
cur = dbconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
cur.execute(
  "DELETE FROM fileinfo WHERE id not in " +
  "(SELECT unnest(string_to_array(replace(replace(replace(fileids, '\"', ''), ']', ''), '[', ''), ',')) FROM posts WHERE fileids <> '[]')"
)
print("Deleted " + str(cur.rowcount) + " orphaned file reference(s).")
dbconn.commit()
print("* committed")

# delete slash commands flagged as deleted
cur = dbconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
cur.execute("DELETE FROM commands where deleteat <> 0")
print("Deleted " + str(cur.rowcount) + " 'deleted' slash command(s).")
dbconn.commit()
print("* committed")
