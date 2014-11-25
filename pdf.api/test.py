import unittest
import requests
import json
import logging
import sys


###########################################################################
# CONFIGURATION
###########################################################################

PDF_API_URL = "http://localhost:8005/"
API_APP_ID = "1"
API_APP_KEY = "1234"
URL_FOR_TESTING = "http://www.w3schools.com/html/tryhtml_basic_document.htm"
#xxx
#URL_FOR_TESTING = "https://inspection.tnolen.com/report/html/542d92c2a00ebd0e2ee34fc0/"


###########################################################################
# PDF.API TEST CASE
###########################################################################

class PdfApiTestCase(unittest.TestCase):

    # Setup and teardown for the class (all tests)
    ###########################################################################
    
    # Setup called once, prior to all tests
    @classmethod
    def setUpClass(self):
        # Set up general vars
        self.pdf_api_url = PDF_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.test_url = URL_FOR_TESTING
        self.tmp_test_data = {}
        
        # Set up logger
        self.log = logging.getLogger("PdfApiTestCase")
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
        self.assertNotEqual(self.pdf_api_url, "")

    # Test creation of pdf file #1...
    def test_001_create(self):
        self.log.debug("I want to send a POST request with HTML code and get an URL of a generated PDF file")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { requests.get(self.test_url, verify=False).text : ""}
        # xxx
        # data = { requests.get(self.test_url, verify=False).text.replace("240px", "10px") : ""}
        params={}
        ret = requests.post(self.pdf_api_url, params=params, data=data, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)

    # Test creation of pdf file #2...
    def test_002_create(self):
        self.log.debug("I want to send a GET request with an URL parameter of an HTML file and get the contents of a generated PDF file")
        url = self.pdf_api_url + "?url=" + self.test_url
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        ## for testing...
        #write to pdf file in current folder
        #pdf_file = open("testing.pdf", "w")
        #pdf_file.write(ret.text)
        #pdf_file.close()
        self.assertTrue(ret.headers['content-type'] == 'application/pdf')

    # Test creation of pdf file #3...
    def test_003_create(self):
        self.log.debug("I want to send a POST request with HTML code and get an URL of a generated PDF file (with voolks images)")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { requests.get(self.test_url, verify=False).text : ""}
        imgs = "<br /><img src='https://www.voolks.com/img/logo_voolks_header.png' /><br /><img src='https://www.voolks.com/img/logo_voolks_header.png' /><br />"
        data = { requests.get(self.test_url, verify=False).text.replace("<body>", "<body>" + imgs) : ""}
        params={}
        ret = requests.post(self.pdf_api_url, params=params, data=data, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)

    # Test creation of pdf file #4...
    def test_004_create(self):
        self.log.debug("I want to send a POST request with HTML code and get an URL of a generated PDF file (with NON voolks images)")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        data = { requests.get(self.test_url, verify=False).text : ""}
        imgs = "<br /><img src='https://www.voolks.com/img/logo_voolks_header.png' /><br /><img src='https://www.xxx.com/img/logo_voolks_header.png' /><br />"
        data = { requests.get(self.test_url, verify=False).text.replace("<body>", "<body>" + imgs) : ""}
        params={}
        ret = requests.post(self.pdf_api_url, params=params, data=data, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == "2")
