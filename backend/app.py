from flask import Flask, request, redirect
import twilio.twiml
import requests
from twilio.rest import TwilioRestClient
import nltk, re, pprint
import random
import sys
import math
import requests
import json
from nltk.util import ngrams
import psycopg2

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def receive_text():
    """Respond to incoming text with a simple text message."""
    msgcount = 0
    input_text = request.values['Body']
    print input_text

    ######## TEXT ANALYSIS ############

    category = get_category(input_text)
    print category
    requester, giver = get_type(input_text)

    ######### LOCATION ANALYSIS ###############
    latitude = 35.687782
    longitude = 36.786667
    lon, lat = geo_data(longitude, latitude )
    required_distance = 1000
    #geo_data(lon, lat, num_rows):

    phone_num = '123123123123'

    ########### POST MESSAGE TO THE postgres DATABASE #############

    #post_str = str(id)
    #final_out = get_helpers_nearby(id, category, requester, giver, phone_num, lat, long)

    ############ return a sms back to the user via twilio ########################
    if category:
        final_res = query_db(required_distance, category)
    else:
        final_res = 'whats your location?'
    resp = twilio.twiml.Response()
    #resp.message(row[0])
    resp.message(final_res)
    return str(resp)

def query_db(required_distance, category):

    ########### Connect to postgres aws #############

    try:
        conn = psycopg2.connect(" dbname='techcrunch' host = 'techcrunch1.c4zgnitpovl7.us-west-2.rds.amazonaws.com' user='mudy' password='techcrunch' ")

    except:
        print "I am unable to connect to the database."

    cur = conn.cursor()
    try:
        t = ('shelter')
        q = '''select ST_Distance(c.x, location) AS distance, phone_num FROM  test_table t, (SELECT ST_GeographyFromText('SRID=4326;POINT(36.832031 35.738504)')) AS c(x) WHERE  ST_DWithin(c.x, location, 1200) AND category LIKE '%shelter%' ORDER  BY distance;'''
        cur.execute(q)

    except:
        print "Error connecting to db"



    rows = cur.fetchall()
    num_people = len(rows)
    distance = int(rows[0][0])
    phone_number = str(rows[0][1])

    final_out = "We have found {} helpers who is {} meters away who can help! Connect with them at: {}".format(num_people, distance, phone_number  )
    return final_out
    #print "\nRows: \n"
    #for row in rows:
    #    print "   ", row



def get_helpers_nearby(id, lat, long, category, requester, giver):
    """
    returns results from the post request to the postgres database
    """
    post_data = {'id': id, 'latitude':lat, 'longitude': long, 'category': category, 'requester': requester, 'giver':giver}
    post_response = requests.post(url='http://some.other.site', data=json.dumps(post_data))
    print post_response.status_code
    return " "

def get_type(input):
    """
    return type: requester or giver
    """
    tokens = nltk.word_tokenize(input)
    bigrams = ngrams(tokens, 2)
    bigram_strings = [' '.join(t).lower() for t in bigrams]

    if 'need help' or 'send help' in bigram_strings:
        requester = True
        giver = False

    elif 'can provide' or 'can help' in bigram_strings:
        giver = True
        requester = False

    return requester, giver


def get_category(input):
    """ Analyse text using nltk -- returns category """
    requester = False
    giver = False
    categories = ['food','shelter', 'transportation', 'medicine' , 'money']

    tokens = nltk.word_tokenize(input)

    res = ""

    for i in categories:
        if i in tokens:
           res += i # res = food or money or shelter
    if res:
        return res
    else:
        return "What is your location?"

def geo_data(lon, lat):

    hex1 = '%012x' % random.randrange(16**12) # 12 char random string
    flt = float(random.randint(0,100))
    dec_lat = random.random()/10
    dec_lon = random.random()/10
    #return '%.6f %.6f'.format(lon+dec_lon, lat+dec_lat)
    return lon+dec_lon, lat+dec_lat
    

if __name__ == "__main__":
    app.run(debug=True)
