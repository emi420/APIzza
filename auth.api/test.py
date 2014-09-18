import unittest
import requests
import json
import logging
import sys


###########################################################################
# CONFIGURATION
###########################################################################

KEYS_API_URL = "http://localhost:7999/"
AUTH_API_URL = "http://localhost:8000/"
DATA_API_URL = "http://localhost:8001/"
API_APP_ID = "1"
API_APP_KEY = "1234"


###########################################################################
# DATA.API TEST CASE
###########################################################################

class AuthApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.auth_api_url = AUTH_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("AuthApiTestCase")
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
        self.assertNotEqual(self.auth_api_url, "")

    # Test login (user=test&password=test)...
    def test_001_login(self):
        self.log.debug("I want to login as test with password test")
        url = self.auth_api_url + "login/?username=test&password=test"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.tmp_test_data["session_sessionid"] = responseObj["sessionId"]
        self.tmp_test_data["session_userid"] = responseObj["id"]
        self.assertTrue("id" in responseObj)

    # Test permissions creation...
    def test_002_create_permission(self):
        self.log.debug("I want to create permissions for an object")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/" + self.tmp_test_data["session_sessionid"] + "/"
        # xxx - test
        data = { "5412f6ca3c45889fbda30aef": { self.tmp_test_data["session_userid"]: { "read": "true", "write": "true" }, "*": { "read": "false", "write": "false" } } }
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)

