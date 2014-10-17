import unittest
import requests
import json
import logging
import sys
import base64


###########################################################################
# CONFIGURATION
###########################################################################

FILE_API_URL = "http://localhost:8010/"
API_APP_ID = "1"
API_APP_KEY = "1234"
FILE_FOR_TESTING = "test.file.api.txt"


###########################################################################
# FILE.API TEST CASE
###########################################################################

class FileApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.file_api_url = FILE_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.test_file = FILE_FOR_TESTING
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("FileApiTestCase")
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
        self.assertNotEqual(self.file_api_url, "")

    # Test creation of file #1...
    def test_001_create_1(self):
        self.log.debug("I want to create a file from a multipart/form-data POST request")
        #headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        headers = {"X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        files = {'file': (self.test_file, 'Test file content...\n')}
        ret = requests.post(self.file_api_url  + "create/", files=files, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        self.assertTrue(ret.text != 'NO_FILES_FOUND')

    # Test creation of file #2...
    def test_002_create_2(self):
        self.log.debug("I want to create a file from a base64 string")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { self.test_file : base64.b64encode('Test file content...\n')}
        params={}
        ret = requests.post(self.file_api_url  + "createBase64/", params=params, data=data, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        self.assertTrue(ret.text == 'OK')
        
    # Test to get file...
    def test_003_get(self):
        self.log.debug("I want to get a file")
        url = self.file_api_url + self.test_file + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        self.assertTrue(ret.text != 'FILE NOT FOUND')

    # Test deletion of a file...
    def test_004_delete(self):
        self.log.debug("I want to delete a file")
        url = self.file_api_url + "delete/" + self.test_file + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        self.assertTrue(ret.text == 'OK')
