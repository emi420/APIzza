import unittest
import requests
import json
import logging
import sys


###########################################################################
# CONFIGURATION
###########################################################################

MAIL_API_URL = "http://localhost:8006/"
API_APP_ID = "1"
API_APP_KEY = "1234"

###########################################################################
# MAIL.API TEST CASE
###########################################################################

class MailApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.mail_api_url = MAIL_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("MailApiTestCase")
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
        self.assertNotEqual(self.mail_api_url, "")

    # Test sending email...
    def test_001_sendmail(self):
        self.log.debug("I want to make a POST request with HTML code and send a mail")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { "from": "test@voolks.com", "to": "maiorano@gmail.com", "subject": "Testing", "html": "<html><b>Testing email</b></html>" }
        params={}
        url = self.mail_api_url + "sendmail/"
        ret = requests.post(url, params=params, data = json.dumps(data), headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertEquals(1, responseObj["sent"])

