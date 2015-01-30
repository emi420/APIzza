import unittest
import requests
import json
import logging
import sys 


###########################################################################
# CONFIGURATION
###########################################################################

KEYS_API_URL = "http://localhost:7999/"
PUSH_API_URL = "http://localhost:8044/"
API_APP_ID = "1"
API_APP_KEY = "1234"


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
        self.log.debug("I want to create an installation on db")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.push_api_url + "installations/"
        data = {"badge": "", "timeZone": "", "deviceType": "", "pushType": "", "GCMSenderId": "", "installationId": "", "deviceToken": "", "channelUris": "", "appName": "", "appVersion": "", "appIdentifier": ""}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created1"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created1"])
        self.assertTrue("id" in responseObj)

    # Test creation of an installation on db...
    def test_0012_create(self):
        self.log.debug("I want to create an installation on db (json)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.push_api_url + "installations/"
        data = "badge=badge&timeZone=timeZone&deviceType=deviceType&pushType=pushType&GCMSenderId=GCMSenderId&installationId=installationId&deviceToken=deviceToken&channelUris=channelUris&appName=appName&appVersion=appVersion&appIdentifier=appIdentifier"
        params = {}
        ret = requests.post(url, params=params, data=data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created2"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created2"])
        self.assertTrue("id" in responseObj)
        
    # Test for getting an installation from db...
    def test_002_get(self):
        self.log.debug("I want to get an installation from db")
        url = self.push_api_url + "installations/" + self.tmp_test_data["id_created1"] + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)   

    # Test for filtering installations send push notifications...
    def test_003_push_filter(self):
        self.log.debug("I want to filter installations send push notification")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.push_api_url + "push/"
        data = {"where": {"deviceType": "android"}, "data": {"alert": "Message"}}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)        
        
    # Test for deleting an installation
    def test_995_delete(self):
        self.log.debug("I want to delete an installation")
        url = self.push_api_url + "installations/" + self.tmp_test_data["id_created1"] + "/"
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)      
        
    # Test for deleting an installation
    def test_996_delete(self):
        self.log.debug("I want to delete an installation")
        url = self.push_api_url + "installations/" + self.tmp_test_data["id_created2"] + "/"
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)          
        