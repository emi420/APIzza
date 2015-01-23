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
# New app-id/api-key
API_APP_ID_NEW = "app_id_new1"
API_APP_KEY_NEW = "app_key_new1234"
API_APP_NAME_NEW = "app_name_new"
API_APP_DOMINE_NEW = "*"
API_APP_PERMISSION_NEW = "app_permission_new"

###########################################################################
# DATA.API TEST CASE
###########################################################################

class KeyApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.key_api_url = KEYS_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.app_id_new = API_APP_ID_NEW
        self.app_key_new = API_APP_KEY_NEW
        self.app_name_new = API_APP_NAME_NEW
        self.app_domine_new = API_APP_DOMINE_NEW
        self.app_permission_new = API_APP_PERMISSION_NEW
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("KeyApiTestCase")
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
        self.assertNotEqual(self.key_api_url, "")

    # Test validations of api credentials
    def test_001_validate(self):
        self.log.debug("I want to I want to validate API credentials (Voolks-Api-Key, Voolks-App-Id)")
        url = self.key_api_url + "check_key/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("domain" in responseObj)

    # Test creation an api credentials...
    def test_001_create(self):
        self.log.debug("I want to create a key")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = self.key_api_url + "create_key/"
        data = {"id_aplication": self.app_id_new, "api_key": self.app_key_new, "name": self.app_name_new, "domine": self.app_domine_new, "permission": self.app_permission_new}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)

    # Test creation an api credentials...
    def test_0012_create(self):
        self.log.debug("I want to create a key (json)")
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        url = self.key_api_url + "create_key/"
        data = "id_aplication="+self.app_id_new+"1"+"&api_key="+self.app_key_new+"1"+"&name="+self.app_name_new+"1"+"&domine="+self.app_domine_new+"&permission="
        params = {}
        ret = requests.post(url, params=params, data=data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)
        
    # Test validations of new api credentials 
    def test_0021_validate(self):
        self.log.debug("I want to I want to validate new API credentials (Voolks-Api-Key, Voolks-App-Id)")
        url = self.key_api_url + "check_key/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id_new, 'X-Voolks-Api-Key': self.app_key_new}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("domain" in responseObj)    
        
    # Test validations of new api credentials 
    def test_0031_validate(self):
        self.log.debug("I want to I want to validate new API credentials (json (Voolks-Api-Key, Voolks-App-Id))")
        url = self.key_api_url + "check_key/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id_new+"1", 'X-Voolks-Api-Key': self.app_key_new+"1"}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("domain" in responseObj)      

    # Test new api credentials deletion...
    def test_0900_delete(self):
        self.log.debug("I want to delete a new api credentials")
        url = self.key_api_url + "delete/?name=" + self.app_name_new
        ret = requests.delete(url)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)    
        
    # Test new api credentials deletion...
    def test_0901_delete(self):
        self.log.debug("I want to delete a new api credentials (json)")
        url = self.key_api_url + "delete/?name=" + self.app_name_new+"1"
        ret = requests.delete(url)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)        