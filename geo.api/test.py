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
LONGITUDE = 1
LATITUDE = 2

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
        data = { "myPosition": {"type":"Point", "coordinates":[LONGITUDE, LATITUDE]}  }
        params={}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.log.debug("Response from api: " + json.dumps(responseObj))
        # self.assertTrue("id" in responseObj)
        
    # Test creation geolocation 
    def test_002_create(self):
        self.log.debug("I want to send a POST request (json)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.geo_api_url + "savegeo/"
        data = "myPosition%5Btype%5D=Point&myPosition%5Bcoordinates%5D%5B%5D="+str(LONGITUDE)+"&myPosition%5Bcoordinates%5D%5B%5D="+str(LATITUDE)+""
        params={}
        ret = requests.post(url, params=params, data=data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.log.debug("Response from api: " + json.dumps(responseObj))
        # self.assertTrue("id" in responseObj)    
