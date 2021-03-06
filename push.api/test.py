import unittest
import requests
import json
import logging
import sys 


###########################################################################
# CONFIGURATION
###########################################################################

KEYS_API_URL = "http://localhost:7999/"
PUSH_API_URL = "http://www9.m-sistemas.com.ar/"
# PUSH_API_URL = "http://localhost:8044/"
API_APP_ID = "1"
API_APP_KEY = "1234"
REG_ID1 = "regId1234"

###########################################################################
# PUSH.API TEST CASE
###########################################################################

class PushApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.push_api_url = PUSH_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("PushApiTestCase")
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
        self.assertNotEqual(self.push_api_url, "")

    # Test creation of an installation on db...
    def test_001_create(self):
        self.log.debug("I want to create an Android installation on db")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.push_api_url + "installations/"
        data = {"timeZone": "America/Argentina/Buenos_Aires, GMT-07:00", "deviceType": "android", "deviceToken": ""+REG_ID1+"", "appName": "appName", "appVersion": "1.0", "pushApiVersion": "1.0"}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created1"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created1"])
        self.assertTrue("id" in responseObj)
        
    # Test for filtering installations send push notifications...
    def test_003_push_filter(self):
        self.log.debug("I want to filter installations send push notification")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.push_api_url + "push/"
        data = {"where": {"deviceType": "android"}, "data": {"message": "New Message from API by Filter"}}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)         
        
    # Test to one send push notifications...
    def test_004_push_one(self):
        self.log.debug("I want to send one push notification")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.push_api_url + "push/"+ self.tmp_test_data["id_created1"] + "/"
        data = {"data": {"message": "New Message from API by one"}}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)       
        
    # Test for deleting an installation
    def test_995_delete(self):
        self.log.debug("I want to delete an installation")
        url = self.push_api_url + "delete/?objid=" + self.tmp_test_data["id_created1"] + ""
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)      
        
        
        