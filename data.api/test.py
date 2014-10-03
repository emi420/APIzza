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
        self.auth_api_url = AUTH_API_URL
        self.key_api_url = KEYS_API_URL
        self.app_id = API_APP_ID
        self.app_key = API_APP_KEY
        self.tmp_test_data = {}
        
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
        self.assertNotEqual(self.data_api_url, "")

    # Test creation of class on db...
    def test_001_create(self):
        self.log.debug("I want to create an object")
        #headers = {"content-type": "application/json", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.data_api_url + "classes/testclass/"
        data = {"testNumber": 123, "testDescription": "This is a decription.", "testExtra": "Extra testing field..." }
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)

    # Test for getting data from db...
    def test_002_get(self):
        self.log.debug("I want to get an object")
        url = self.data_api_url + "classes/testclass/" + self.tmp_test_data["id_created"] + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj and responseObj["testNumber"] == 123)

    # Test for getting all objects of class
    def test_003_get_all(self):
        self.log.debug("I want to get all objects")
        url = self.data_api_url + "classes/testclass/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj["result"][0])

    # Test for updating an object
    def test_004_update(self):
        self.log.debug("I want to update an object")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.data_api_url + "classes/testclass/" + self.tmp_test_data["id_created"] + "/"
        data = {"testNumber": 321, "testDescription": "This is a description.", "testExtra": "Extra testing field..." }
        params = {}
        ret = requests.put(url, params=params, data=json.dumps(data), headers=headers)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("updatedAt" in responseObj and "testNumber" in responseObj and responseObj["testNumber"] == 321)

    # Test for filtering objects
    def test_007_filter(self):
        self.log.debug("I want to filter all objects using a where parameter")
        url = self.data_api_url + "classes/testclass/?where=" + """{"testNumber":321}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj["result"][0] and responseObj["result"][0]["testNumber"] == 321)
        
    # Test for filtering objects (reg. ex.)
    def test_008_filter_regex(self):
        self.log.debug("I want to filter all objects using a regular expression")
        url = self.data_api_url + "classes/testclass/?where=" + """{"testDescription":{"$regex":"^This is a (.*)$"}}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj["result"][0] and responseObj["result"][0]["testNumber"] == 321)
        
    # Test for getting only some properties
    def test_009_projections(self):
        self.log.debug("I want to get only some properties on the response objects (projections)")
        url = self.data_api_url + "classes/testclass/?where=" + """[{"testNumber":321},{"testDescription":1}]"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testDescription" in responseObj["result"][0] and not "testExtra" in responseObj["result"][0])

    # Test for limiting query
    def test_010_limit(self):
        self.log.debug("I want to limit the objects count in the response")
        
        # we create another object with same test number for testing...
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.data_api_url + "classes/testclass/"
        data = {"testNumber": 321, "testDescription": "This is a decription for 999.", "testExtra": "Extra testing field 999..." }
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        
        # test limiting...
        url = self.data_api_url + "classes/testclass/?limit=1&where=" + """{"testNumber":321}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj["result"][0] and len(responseObj["result"]) == 1)

    # Test for skipping query
    def test_011_skip(self):
        self.log.debug("I want to skip objects on the response")
        url = self.data_api_url + "classes/testclass/?limit=1&skip=1&where=" + """{"testNumber":321}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj["result"][0] and len(responseObj["result"]) == 1 and responseObj["result"][0]["testDescription"].find("999") >= 0)

    # Test for counting query
    def test_012_count(self):
        self.log.debug("I want to count the objects in the response")
        url = self.data_api_url + "classes/testclass/?where=" + """{"testNumber":321}"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue(len(responseObj["result"]) == 2)

    # Test for ordering query
    def test_013_order(self):
        self.log.debug("I want to order the objects on the response")
        url = self.data_api_url + "classes/testclass/?sort=" + """{"_id":-1}&limit=1"""
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj["result"][0] and len(responseObj["result"]) == 1 and responseObj["result"][0]["testDescription"].find("999") >= 0)

    ###########################################################################

    # Test for setting permissions for object
    def test_101_permissions_set(self):
        self.log.debug("I want to set permissions for object (login as test with password test)")
        
        url = self.auth_api_url + "login/?username=test&password=test"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["session_sessionid"] = responseObj["sessionId"]
        self.tmp_test_data["session_userid"] = responseObj["id"]
        
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/"
        data = { self.tmp_test_data["id_created"]: { self.tmp_test_data["session_userid"]: { "read": "true", "write": "true" }, "*": { "read": "false", "write": "false" } } }
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj2 =  json.loads(ret.text)

        self.assertTrue("code" in responseObj2 and responseObj2["code"] == 1)

    # Test for getting object (no data expected, asking for object with permissions, without session)
    def test_102_permissions_test_nok(self):
        self.log.debug("I want to get no data when asking for object with permissions (without session)")
        url = self.data_api_url + "classes/testclass/" + self.tmp_test_data["id_created"] + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" not in responseObj)

    # Test for getting object (now asking for object with permissions with session)
    def test_103_permissions_test_ok(self):
        self.log.debug("I want to get data when asking for object with permissions (with session)")
        url = self.data_api_url + "classes/testclass/" + self.tmp_test_data["id_created"] + "/"
        ret = requests.get(url, headers={'X-Voolks-Session-Id': self.tmp_test_data["session_sessionid"], 'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("testNumber" in responseObj)


        
    ###########################################################################

    # Test for deleting an object
    def test_995_delete(self):
        self.log.debug("I want to delete an object")
        url = self.data_api_url + "classes/testclass/" + self.tmp_test_data["id_created"] + "/"
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue(responseObj == {})

    # Test for deleting all objects
    def test_996_delete_all(self):
        self.log.debug("I want to delete all objects")
        url = self.data_api_url + "classes/testclass/"
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue(responseObj == {})
