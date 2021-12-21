# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import library yang akan digunakan
import json
import re
import sqlite3
import unicodedata
from datetime import datetime

from kafka import KafkaConsumer

# %%
# Membuat database Tweets.db serta tabel tweet di dalam database
try:
  sqliteConnection = sqlite3.connect('Tweets.db')
  cursor = sqliteConnection.cursor()
  print("Database created and Successfully Connected to SQLite")

  query = "select sqlite_version();"
  cursor.execute(query)
  record = cursor.fetchall()
  print("SQLite Database Version is: ", record)

  query = """CREATE TABLE IF NOT EXISTS tweet 
      (id TEXT PRIMARY KEY NOT NULL,
      user_id TEXT NOT NULL,
      username TEXT NOT NULL,
      tweet TEXT NOT NULL,
      created_at TEXT NOT NULL,
      favorite_count INTEGER NOT NULL,
      retweet_count INTEGER NOT NULL,
      reply_count INTEGER NOT NULL,
      quote_count INTEGER NOT NULL,
      lang_type TEXT
      );"""
  cursor.execute(query)
  sqliteConnection.commit()
  cursor.close()

except sqlite3.Error as error:
  print("Error while connecting to sqlite", error)
finally:
  if sqliteConnection:
    sqliteConnection.close()
    print("The SQLite connection is closed")
# %%
# Fungsi untuk melakukan transform, yaitu normalisasi tanggal dan membersihkan teks tweet
def normalize_timestamp(time):
    mytime = datetime.strptime(time, '%a %b %d %H:%M:%S %z %Y')
    return (mytime.strftime('%Y-%m-%d %H:%M:%S'))

def clean(tweet):
    #remove non-ascii
    tweet = unicodedata.normalize("NFKD", tweet).encode("ascii", "ignore").decode("utf-8", "ignore")
    #remove URLs
    tweet = re.sub(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\".,<>?«»“”‘’]))", "", tweet)
    #remove punctuations
    tweet = re.sub(r"[^\w]|_", " ",tweet)
    #remove digit from tweeting
    tweet = re.sub("\S*\d\S*", "", tweet).strip()
    #remove digit or numbers
    tweet = re.sub(r"\b\d+\b", " ", tweet)
    #to lowercase
    tweet = tweet.lower()
    #Remove additional white spaces
    tweet = re.sub("[\s]+", " ", tweet)
    tweet = re.sub(r"http\S+", "", tweet)
    return tweet
# %%
# Fungsi untuk melakukan clean beberapa data dan load ke tabel tweet di dalam Tweets.db
def load(msg):
  temp = json.loads(msg)
  tweet = (temp['id'],temp['user']['id'],temp['user']['name'], normalize_timestamp(temp['created_at']),
           temp['favorite_count'], temp['retweet_count'], temp['reply_count'],
           temp['quote_count'], temp['lang'], clean(temp['text']))
  try:
    sqliteConnection = sqlite3.connect('Tweets.db')
    
    cursor = sqliteConnection.cursor()
    query = f"""INSERT INTO tweet (id, user_id, username, 
                created_at, favorite_count, retweet_count, reply_count, quote_count,
                lang_type, tweet)
            VALUES
              (?,?,?,?,?,?,?,?,?,?);"""
    cursor.execute(query, tweet)
    sqliteConnection.commit()
    cursor.close()

  except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
  finally:
    if sqliteConnection:
      sqliteConnection.close()  
# %%
# Inisialisasi consumer untuk mendapatkan data dari producer
consumer1 = KafkaConsumer('tugas-11-2', bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='consumers',
                        value_deserializer=lambda x: x.decode('utf8'), 
                        consumer_timeout_ms=10000,
                        heartbeat_interval_ms=1000,
                        api_version=(3, 0, 0))
# %%
# Mengambil data menggunakan consumer dan memanggilnya ke dalam fungsi load
print(consumer1.bootstrap_connected())
for msg in consumer1:
    print(msg.value)
    load(msg.value)


