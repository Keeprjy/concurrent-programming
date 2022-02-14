# Junye Eluvio take home challange option 2

## Question
Option 2 - Applications

Imagine you have a program that needs to look up information about items using their item ID, often in large batches.

Unfortunately, the only API available for returning this data takes one item at a time, which means you will have to perform one query per item. Additionally, the API is limited to five simultaneous requests. Any additional requests will be served with HTTP 429 (too many requests).

Write a client utility for your program to use that will retrieve the information for all given IDs as quickly as possible without triggering the simultaneous requests limit, and without performing unnecessary queries for item IDs that have already been seen.

API Usage:

GET https://eluv.io/items/:id

Required headers:

Authorization: Base64(:id)

Example:

curl https://challenges.qluv.io/items/cRF2dvDZQsmu37WGgK6MTcL7XjH -H "Authorization: Y1JGMmR2RFpRc211MzdXR2dLNk1UY0w3WGpI"

## Answer
The code is a python3 script. The script name is api_fetch.py

### How to run the script
1. install python3 first since python 2.7 is already deprecated. If you point command python to python3, please feel free to replace python3 with python.
2. in terminal, run `python3 api_fetch.py <input_file.csv>`
I have an input file example, input_example.csv under the folder. You can run `python3 api_fetch.py input_example.csv`. 
3. The results will be output in the terminal and also in a file `output.csv` under the same folder.
4. if you run `python3 api_fetch.py` without the input_file, the script will generate 16 random item_ids + 1 duplicated item_id as input item_id_list
