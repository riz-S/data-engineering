# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import library yang digunakan
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream,StreamListener
from kafka import KafkaProducer
import time


# %%
# Fungsi untuk melacak hasil producer
def on_send_success(record_metadata):
    # print(record_metadata.topic)
    print(record_metadata)
    # print(record_metadata.offset)

def on_send_error(excp):
    print("error", excp)
    log.error('I am an errback', exc_info=excp)


# %%
# Menginisiasi producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],api_version=(3, 0, 0), value_serializer=lambda x: x.encode('utf-8'))
topic_name = 'tugas-11-2'


# %%
# Melihat status koneksi producer
print(producer.bootstrap_connected())


# %%
# Class untuk stream twitter berdasarkan waktu
class Listener(StreamListener):
  def __init__(self, time_limit=60):
    self.start_time = time.time()
    self.limit = time_limit
    super(Listener, self).__init__()

  def on_data(self, data):
    if (time.time() - self.start_time) < self.limit:
      producer.send(topic_name, data).add_callback(on_send_success).add_errback(on_send_error)
      return True
    else:
      return False


# %%
# Setup autentikasi ke Twitter API
consumer_key = "TCHVbt5fbcttUMjNoNYPLsyzZ"
consumer_secret = "wih7b5RUNRkezZouANXqm1aXfTq6A9SOcIcQxJ4WY5tW1b5WT0"
access_token = "1000362437558743041-VnnlqzolYZfdp843j3ZaLVZ1oAnbiK"
access_token_secret = "lmqiLv45HT3ckrnLAz0XaYdsBamkxzpszDRpbS9NeLAT5"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# %%
# Melakukan stream
stream = Stream(auth, Listener(time_limit=60), lang='en')
stream.filter(languages=["en"], track=['Samsung'])

# Menutup producer
producer.flush()
producer.close()

