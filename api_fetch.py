#!/usr/bin/python

import base64
import csv
import threading
import random
import requests
import sys

# input
item_id_list = []

# use set to dedup item ids
item_id_used_set = set()

# store output
output_list = []

# lock to protect item_id_list.pop and add to item_id_used_set
input_lock = threading.Lock()
# lock to protect write results
output_lock = threading.Lock()

MAX_THREAD_COUNT = 5

# Define a function for the thread
def fetch_thread(threadName):
  popped_thread = []
  output_thread = []
  while True:
    # protect list pop and add to set
    with input_lock: 
      if len(item_id_list) == 0:
        break
      item_id = item_id_list.pop()
      popped_thread.append(item_id)
      # print(f"{threadName}: pop {item_id}")
      if item_id not in item_id_used_set:
        # fetch data
        item_id_used_set.add(item_id)
      else:
        continue

    # fetch data
    # print(f"{threadName}: fetching item {item_id}")
    response = fetch_item(item_id)
    # print(f"{threadName}: fetched item {item_id}")

    # protect write results
    # DO NOT write to global variable to avoid several lock wait. Assume thread switch has overhead
    output_thread.append({"item_id": item_id, "response": response})

  # write results
  print(f"{threadName}: popped items {popped_thread}")
  print(f"{threadName}: fetched items {output_thread}")
  global output_list
  with output_lock:
    output_list = output_list + output_thread
  print(f"{threadName}: is done")

# fetch api
def fetch_item(item_id):
  url = f"https://challenges.qluv.io/items/{item_id}"
  item_id_bytes = item_id.encode("ascii")
  headers = {
    "Authorization": base64.b64encode(item_id_bytes)
  }

  response = requests.request("GET", url, headers=headers)
  # print(f"item_id {item_id}, response.status_code {response.status_code}")
  if response.status_code == 200:
    # print(response.text)
    return response.text
  else:
    print(f"item_id {item_id}, response.status_code {response.status_code}")
  return None

def generate_random_id(candidates):
  chars = random.sample(candidates, 27)
  id = ''.join(chars)
  return id

def get_default_item_id_list():
  candidates = []
  for i in range(0, 25):
    candidates.append(chr(ord('a') + i))
    candidates.append(chr(ord('A') + i))
    if i < 10:
      candidates.append(chr(ord('0') + i))
  item_id_list.append('cRF2dvDZQsmu37WGgK6MTcL7XjH')
  for i in range(0, 15):
    item_id_list.append(generate_random_id(candidates))
  item_id_list.append('cRF2dvDZQsmu37WGgK6MTcL7XjH')

def get_item_id_list_from_file(filename):
  global item_id_list
  with open(filename) as csvfile:
    rows = csv.reader(csvfile, delimiter=",")
    for row in rows:
      if len(row) > 0:
        item_id_list.append(row[0])

if __name__ == '__main__':
  # initialize input
  if len(sys.argv) == 1:
    get_default_item_id_list()
  else:
    filename = sys.argv[1]
    get_item_id_list_from_file(filename)
  
  print("input is -")
  print(item_id_list)
  print("==========================================")

  # Create count threads as follows
  threads = []
  try:
    for i in range(0, MAX_THREAD_COUNT):
      th = threading.Thread(target=fetch_thread, args=(f"Thread-{i}", ) )
      threads.append(th)

    for th in threads:
      th.start()

    for th in threads:
      th.join()
  except:
    print("Error: unable to start thread")

  print("==========================================")
  print("output is -")
  print(output_list)
  with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = ['item_id', 'response'])
    writer.writeheader()
    writer.writerows(output_list)
