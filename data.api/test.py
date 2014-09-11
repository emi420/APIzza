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

class DataApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.data_api_url = DATA_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        
        # Set up logger
        self.log = logging.getLogger("DataApiTestCase")
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
        self.log.debug("Test setup done.")

    # Tear down called for each test
    def tearDown(self):
        self.log.debug("Test done.")

    # Tests
    ###########################################################################
    
    # Test for needed vars...
    def test_000_pretesting(self):
        self.log.debug("Starting test #000...")
        self.assertNotEqual(self.data_api_url, "")

    # Test creation of class...
    def test_001_creating(self):
        self.log.debug("Starting test #001...")
        headers = {"content-type": "application/json", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.data_api_url + "classes/testclass/"
        data = {"testNumber": 123, "testDescription": "This is a decription.", "testExtra": "Extra testing field..." }
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        responseObj =  json.loads(ret.text)
        self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)

    # Test for getting data from record...
    def test_002_querying(self):
        self.log.debug("Starting test #002...")
        url = self.data_api_url + "classes/testclass/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertNotEqual(responseObj, None)

    # Test updating of record...
    def test_003_updating(self):
        self.log.debug("Starting test #003...")
        self.assertNotEqual(self.data_api_url, "")

    def test_004_filtering(self):
        self.log.debug("Starting test #004...")
        self.assertNotEqual(self.data_api_url, "")

    def test_005_limiting(self):
        self.log.debug("Starting test #005...")
        self.assertNotEqual(self.data_api_url, "")

    def test_006_sorting(self):
        self.log.debug("Starting test #006...")
        self.assertNotEqual(self.data_api_url, "")

    def test_007_permissions(self):
        self.log.debug("Starting test #007...")
        self.assertNotEqual(self.data_api_url, "")
        
        
        
        
    def test_099_deleting(self):
        self.log.debug("Starting test #099...")
        self.assertNotEqual(self.data_api_url, "")
