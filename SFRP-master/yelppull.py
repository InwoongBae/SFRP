from DataCollector import data_collector #yelp api function
import json #for file handling
import requests #for api query
import pandas as pd #for data frames
import caffeine #prevent OSX from sleeping while the script is running

#load API Keys
with open('keys.json') as file:
    keys = json.load(file)
YELP_KEY = keys.get('yelp')

#load the reference data frame
initial_data = pd.read_csv('clean_data_initial.csv')

#take length of index for percentage calculation
l = len(initial_data.index)

#initialize list to write to
yelp_list = []

#iterate over data frame and pull yelp info for each entry
try:
    for index in initial_data.index:
        d = data_collector(initial_data, index, YELP_KEY)
        #add entry to yelp yelp_list
        yelp_list.append(d)
        #print percent completion
        p = index / l * 100
        print("******* %.3f%% *******" % p)
except:
    #if theres a connection failure dump the data
    with open('apipull', 'w') as fout:
        json.dump(yelp_list, fout)


#dump list into a json like txt file
with open('apipull', 'w') as fout:
    json.dump(yelp_list, fout)
