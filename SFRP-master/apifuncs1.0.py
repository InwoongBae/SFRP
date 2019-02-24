#built these while desiging DataCollector and yelppull
#use yelppull/DataCollector instead of these

def business_search(name, address, lat, long, api_key):
    """matches business to yelp data base by name and location parameters"""

    url = "https://api.yelp.com/v3/businesses/matches"

    #parameters to send api are fed int the querystring
    querystring = {"name":name,"city":"San%20Francisco","state":"CA","country":"US","address1":address,"latitude": lat,"longitude":long}
    payload = ""
    #API authorization is sent through the header
    headers = {
    'Authorization': "Bearer " + api_key,
    'cache-control': "no-cache",
    }

    #query yelp API using requests
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    r = response.json()

    #if the website fails to return information return 0
    if response.status_code != 200:
        return 0
    #if yelp fails to match with any businesses return 0
    if len(r['businesses']) == 0:
        return 0

    return r

def retrieve_id(name, address, lat, long, api_key):
    """retrieves a business ID from yelp business matches, returns 0 if unable to return ID"""
    #get business matches via business_search()
    r = business_search(name, address, lat, long, api_key)
    #if unable to match return 0
    if r == 0:
        return 0
    return r['businesses'][0]['id']

def business_data(business_id):
    """pulls business data from yelp using the business id"""
    #returns json dictionary with business information
    #returns 0 if http error
    base_url = "https://api.yelp.com/v3/businesses/"
    payload = ""
    headers = {
        'Authorization': "Bearer " + API_KEY,
        'cache-control': "no-cache",
        'Postman-Token': "a1945a32-c271-442e-abbe-af7bebe6c655"
        }

    response = requests.request("GET", base_url + business_id, data=payload, headers=headers)

    if response.status_code != 200:
        return 0

    return response.json()

def data_retrieval(dataframe, index, api_key):
    """pulls data from yelp after retrieving ID from business match"""
    #takes data frame and index as imput. Outputs Dictionary with yelp information
    #will return 0 if failure
    #requires retrieve_id(), business_data(), and business_search()
    #json and requests are neccessary

    #datafame col names must be in original formating
    #extract search information form data frame
    name = raw_score_data.iloc[index]['business_name']
    address = raw_score_data.iloc[index]['business_address']
    lat = raw_score_data.iloc[index]['business_latitude']
    long = raw_score_data.iloc[index]['business_longitude']

    #retrieve ID from yelp
    bid = retrieve_id(name, address, lat, long, api_key)

    #return business information from yelp
    return business_data(bid)
