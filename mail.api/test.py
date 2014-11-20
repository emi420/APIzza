import unittest
import requests
import json
import logging
import sys


###########################################################################
# CONFIGURATION
###########################################################################

MAIL_API_URL = "http://localhost:8006/"
AUTH_API_URL = "http://localhost:8000/"
API_APP_ID = "1"
API_APP_KEY = "1234"
TEST_USERNAME = "test9999"
TEST_PASSWORD = "test9999"

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
        self.auth_api_url = AUTH_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.test_username = TEST_USERNAME
        self.test_password = TEST_PASSWORD
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

    # Test user creation (user=test9999&password=test9999)...
    def test_0011_create(self):
        self.log.debug("I want to create a user")
        url = self.auth_api_url + "signup/?username=" + self.test_username + "&password=" + self.test_password
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)    
    
    # Test authentication/login...
    def test_0012_login(self):
        #self.log.debug("I want to login as test with password test")
        self.log.debug("I want to authenticate a user")
        url = self.auth_api_url + "login/?username=" + self.test_username + "&password=" + self.test_password
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.tmp_test_data["session_sessionid"] = responseObj["sessionId"]
        self.tmp_test_data["session_userid"] = responseObj["id"]
        self.assertTrue("id" in responseObj)

    # Test session validation
    def test_0013_validate(self):
        self.log.debug("I want to validate session for a user")
        url = self.auth_api_url + "validate/" + self.tmp_test_data["session_sessionid"] + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + json.dumps(responseObj))
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("userid" in responseObj)
    
    # Test sending email...
    def test_001_sendmail(self):
        self.log.debug("I want to make a POST request with HTML code and send a mail (invalid session)")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { "from": "test@voolks.com", "to": "maiorano@gmail.com", "subject": "Testing", "html": "<html><b>Testing email</b></html>" }
        params={}
        url = self.mail_api_url + "sendmail/"
        # for testing general exception handling (you should uncomment raw response from api also)
        ret = requests.post(url, params=params, data = json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertEquals('53', responseObj["code"]) 
        
        # Test sending email...
    def test_002_sendmail(self):
        self.log.debug("I want to make a POST request with HTML code and send a mail (json (invalid session))")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { "from": "test@voolks.com", "to": "maiorano@gmail.com", "subject": "Testing", "html": "<html><b>Testing email (json)</b></html>" }
        params={}
        url = self.mail_api_url + "sendmail/"
        # for testing general exception handling (you should uncomment raw response from api also)
        ret = requests.post(url, params=params, data = data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertEquals('53', responseObj["code"]) 

    # Test sending email...
    def test_003_sendmail(self):
        self.log.debug("I want to make a POST request with HTML code and send a mail (json and session #3)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { "from": "test@voolks.com", "to": "maiorano@gmail.com", "subject": "Testing", "html": "<html><b>Testing email (json and session)</b></html>" }
        params={}
        url = self.mail_api_url + "sendmail/"
        # for testing general exception handling (you should uncomment raw response from api also)
        ret = requests.post(url, params=params, data = data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertEquals(1, responseObj["sent"])

    # Test user deletion...
    def test_0900_delete(self):
        self.log.debug("I want to delete a user")
        url = self.auth_api_url + "delete/?username=" + self.test_username + "&password=" + self.test_password
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)