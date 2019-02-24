import requests #for HTTP requests
import json #for handling API responses
import pandas as pd

def data_collector(dataframe, index, api_key):
    """Collects Data From Yelp"""
    #takes data frame and index as input. Outputs Dictionary with yelp information
    #will return 0 if failure
    #json and requests are neccessary

    #datafame col names must be in original formating
    #extract search information form data frame
    name = dataframe.iloc[index]['business_name']
    address = dataframe.iloc[index]['business_address']
    lat = dataframe.iloc[index]['business_latitude']
    long = dataframe.iloc[index]['business_longitude']

    #url path for matching a business to the input information
    url_match = "https://api.yelp.com/v3/businesses/matches"
    #url path for returing business info for a particular ID
    url_business = "https://api.yelp.com/v3/businesses/"

    #parameters to send api are fed int the querystring
    querystring = {"name":name,"city":"San%20Francisco","state":"CA","country":"US","address1":address,"latitude": lat,"longitude":long}
    payload = ""

    #API authorization is sent through the header
    headers = {
    'Authorization': "Bearer " + api_key,
    'cache-control': "no-cache",
    }

    #query yelp API using requests
    match_response = requests.request("GET", url_match, data=payload, headers=headers, params=querystring)

    #format the json response in python
    match_dict = match_response.json()

    #exit if theres an HTTP error
    if match_response.status_code != 200:
        return 0
    #exit if no business is found
    if len(match_dict['businesses']) == 0:
        return 0
    #pull the business id from yelps json dictionary
    business_id = match_dict['businesses'][0]['id']

    #request the business information for this id
    business_response = requests.request("GET", url_business + business_id, data=payload, headers=headers)

    #if theres a HTTP error exit
    if business_response.status_code != 200:
        return 0

    #format the json response in python
    info = business_response.json()

    #return business information from yelp
    return info
