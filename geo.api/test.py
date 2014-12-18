import unittest
import requests
import json
import logging
import sys


###########################################################################
# CONFIGURATION
###########################################################################

GEO_API_URL = "http://localhost:8040/"
API_APP_ID = "1"
API_APP_KEY = "1234"
# Av de Mayo & Peru
LONGITUDE1 = -34.608570
LATITUDE1 = -58.375023
# Av Rivadavia & Florida
LONGITUDE2 = -34.608005
LATITUDE2 = -58.375047
# Washington D.C.
LONGITUDE3 = 38.898441
LATITUDE3 = -77.011144
# Av Corrientes & Av Leandro N. Alem
LONGITUDENEAR = -34.602963
LATITUDENEAR = -58.370436
# Meters
MAXDISTANCENEAR = 1000
MINDISTANCENEAR = 1
# Av Cordoba & Av Leandro N. Alem
LONGITUDEWT1 = -34.598369
LATITUDEWT1 = -58.371302
# Av Independencia & Av Paseo Colon
LONGITUDEWT2 = -34.617116
LATITUDEWT2 = -58.369577
# Av Independencia & Bernardo de Irigoyen
LONGITUDEWT3 = -34.617636
LATITUDEWT3 = -58.380135

###########################################################################
# GEO.API TEST CASE
###########################################################################

class GeoApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.geo_api_url = GEO_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("GeoApiTestCase")
        self.log_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        self.log_handler = logging.StreamHandler(stream=sys.stdout)
        self.log_handler.setFormatter(self.log_formatter)
        self.log_handler.setLevel(logging.DEBUG)
        self.log.addHandler(self.log_handler)
        self.log.setLevel(logging.DEBUG)

        self.log.debug("General setup done.")

    # Tear down called when all tests are done
    @classmethod
    def tearDownClass(self):
        self.log.debug("All tests done.")
    
    # Setup and teardown for each test
    ###########################################################################

    # Setup called for each test
    def setUp(self):
        #self.log.debug("Test setup done.")
        return

    # Tear down called for each test
    def tearDown(self):
        self.log.debug("Test done.")

    # Tests
    ###########################################################################
    
    # Test for needed vars...
    def test_000_pretest(self):
        self.log.debug("Pretest (testing required configurations)")
        self.assertNotEqual(self.geo_api_url, "")

    # Test creation geolocation 
    def test_001_create(self):
        self.log.debug("I want to send a POST request")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.geo_api_url + "savegeo/"
        data = { "myPosition": {"type":"Point", "coordinates":[LONGITUDE1, LATITUDE1]}  }
        params={}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        # self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)
 
    # Test creation geolocation
    def test_0011_create(self):
        self.log.debug("I want to send a POST request")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.geo_api_url + "savegeo/"
        data = { "myPosition": {"type":"Point", "coordinates":[LONGITUDE3, LATITUDE3]}  }
        params={}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        # self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj) 
        
    # Test creation geolocation 
    def test_002_create(self):
        self.log.debug("I want to send a POST request (json)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.geo_api_url + "savegeo/"
        data = "myPosition%5Btype%5D=Point&myPosition%5Bcoordinates%5D%5B%5D="+str(LONGITUDE2)+"&myPosition%5Bcoordinates%5D%5B%5D="+str(LATITUDE2)+""
        params={}
        ret = requests.post(url, params=params, data=data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        # self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)    

    # Test get near geolocation 
    def test_003_get_neargeo(self):
        self.log.debug("I want to get near geolocation")
        url = self.geo_api_url + "neargeo/?where=" + """{"myPosition":{"$near":{"$geometry":{"type":"Point", "coordinates": [""" + str(LONGITUDENEAR) + """, """ + str(LATITUDENEAR) + """]}, "$maxDistance": """ + str(MAXDISTANCENEAR) + """, "$minDistance": """ + str(MINDISTANCENEAR) + """}}}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        # self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("myPosition" in responseObj["result"][0])

    # Test get within geolocation 
    def test_004_get_withingeo(self):
        self.log.debug("I want to get within geolocation")  
        url = self.geo_api_url + "withingeo/?where=" + """{"myPosition":{"$geoWithin":{"$geometry":{"type":"Polygon", "coordinates": [[[""" + str(LONGITUDEWT1) + """, """ + str(LATITUDEWT1) + """], [""" + str(LONGITUDEWT2) + """, """ + str(LATITUDEWT2) + """], [""" + str(LONGITUDEWT3) + """, """ + str(LATITUDEWT3) + """], [""" + str(LONGITUDEWT1) + """, """ + str(LATITUDEWT1) + """]]]}}}}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        # self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("myPosition" in responseObj["result"][0])