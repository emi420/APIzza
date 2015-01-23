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
TEST_USERNAME = "test9999"
TEST_PASSWORD = "test9999"
TEST_GROUP_NAME = "testgroup9999"
TEST_OBJECT = "5412f6ca3c45889fbda30af1"

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
        self.test_username = TEST_USERNAME
        self.test_password = TEST_PASSWORD
        self.test_group_name = TEST_GROUP_NAME
        self.test_object = TEST_OBJECT
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
    def test_0000_pretest(self):
        self.log.debug("Pretest (testing required configurations)")
        self.log.debug("Test auth.api URL: " + self.auth_api_url)
        self.log.debug("Test username: " + self.test_username)
        self.log.debug("Test password: " + self.test_password)
        self.log.debug("Test object: " + self.test_object)
        self.assertNotEqual(self.auth_api_url, "")

    # Test user creation (user=test9999&password=test9999)...
    def test_0001_create(self):
        self.log.debug("I want to create a user")
        url = self.auth_api_url + "signup/?username=" + self.test_username + "&password=" + self.test_password
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("id" in responseObj)

     # Test user creation (user=test99991&password=test99991)...
    def test_00012_create(self):
        self.log.debug("I want to create a user (post)")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "signup/"
        data = {"username": self.test_username+"1", "password": self.test_password+"1"}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)
    
    # Test user creation (user=test99992&password=test99992)...
    def test_00013_create(self):
        self.log.debug("I want to create a user (post/json)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "signup/"
        data = {"username": self.test_username+"2", "password": self.test_password+"2"}
        params = {}
        ret = requests.post(url, params=params, data=data, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)
     
     # Test user creation (user=test99991&password=test99991)...
    def test_00014_create(self):
        self.log.debug("I want to create a user (post)")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "signup/"
        data = {"username": self.test_username+"3", "password": self.test_password+"3"}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_created"] = responseObj["id"]
        #self.log.debug("Parsed id for testing: " + self.tmp_test_data["id_created"])
        self.assertTrue("id" in responseObj)
     
    # Test authentication/login...
    def test_0010_login(self):
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
    def test_0011_validate(self):
        self.log.debug("I want to validate session for a user")
        url = self.auth_api_url + "validate/" + self.tmp_test_data["session_sessionid"] + "/"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + json.dumps(responseObj))
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("userid" in responseObj)

    # Test group creation (name=testgroup)...
    def test_001_create_group(self): 
        self.log.debug("I want to create a group (post)")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "group/"
        data = {"name": self.test_group_name, "permissions": {"*": {"write": "true"}}}
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_group_created"] = responseObj["id"]
        self.assertTrue("id" in responseObj)     
    # Test group creation (name=testgroup1)...
    def test_0012_create_group(self):
        self.log.debug("I want to create a group (post/json)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "group/"
        data = "name="+self.test_group_name+"1"+"&permissions%5B*%5D%5Bwrite%5D=true"
        params = {}
        ret = requests.post(url, params=params, data=data, headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["id_group_created"] = responseObj["id"]
        self.assertTrue("id" in responseObj)    
    # Test add user to a group...
    def test_001_add_users_to_group(self):
        self.log.debug("I want to add users to a group")
        headers = {"Content-Type": "application/x-www-form-urlencoded",  "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "group/"+ self.tmp_test_data["id_group_created"] + "/"
        data = {"users": [self.test_username]}
        params = {}
        ret = requests.put(url, params=params, data=json.dumps(data), headers=headers)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        # self.assertTrue("code" in responseObj and responseObj["code"] == 1)    
        
    # Test permissions creation...
    def test_0020_create_permission(self):
        self.log.debug("I want to create user permissions for an object")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/"
        data = { self.test_object: { self.tmp_test_data["session_userid"]: { "read": "true", "write": "true" }, "*": { "read": "true", "write": "false" } } }
        params = {}
        ret = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)

     # Test permissions creation...
    def test_0021_create_permission(self):
        self.log.debug("I want to create user permissions for an object (json)")
        headers = {"Content-Type": "application/json; charset=UTF-8", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/"
        # data = { self.test_object: { self.tmp_test_data["session_userid"]: { "read": "true", "write": "true" }, "*": { "read": "true", "write": "false" } } }
        data = "kk17er39tmxs0pfawmym8ly9bgpavfnb%5B" + str(self.tmp_test_data["session_userid"]) + "%5D%5Bread%5D=true&kk17er39tmxs0pfawmym8ly9bgpavfnb%5B11%5D%5Bwrite%5D=true&kk17er39tmxs0pfawmym8ly9bgpavfnb%5B*%5D%5Bread%5D=false&kk17er39tmxs0pfawmym8ly9bgpavfnb%5B*%5D%5Bwrite%5D=false"
        params = {}
        ret = requests.post(url, params=params, data=data, headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)   
        
    # Test permissions updating...
    def test_0030_update_permission(self):
        self.log.debug("I want to update user permissions for an object")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/"
        data = { self.test_object: { self.tmp_test_data["session_userid"]: { "read": "true", "write": "true" }, "*": { "read": "false", "write": "false" } } }
        params = {}
        ret = requests.put(url, params=params, data=json.dumps(data), headers=headers)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)

    # Test permissions getting...
    def test_0040_get_permission(self):
        self.log.debug("I want to get user permissions for an object")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/?objid=" + self.test_object
        ret = requests.get(url, headers=headers, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1) # and self.tmp_test_data["session_userid"] in responseObj)
        
    # Test permissions deletion...
    def test_0050_delete_permission(self):
        self.log.debug("I want to delete user permissions for an object")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "X-Voolks-Session-Id": self.tmp_test_data["session_sessionid"], "X-Voolks-App-Id": self.app_id, "X-Voolks-Api-Key": self.app_key }
        url = self.auth_api_url + "permissions/?objid=" + self.test_object + "&userid=" + str(self.tmp_test_data["session_userid"])
        ret = requests.delete(url, headers=headers, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)
    
    # Test reset password user...
    def test_0700_reset(self):
        self.log.debug("I want to reset password user")
        url = self.auth_api_url + "reset_password/?username=" + self.test_username + "3"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("newpassword" in responseObj)
    
    # Test change password user...
    def test_0800_change(self):
        self.log.debug("I want to change password user")
        url = self.auth_api_url + "change_password/?username=" + self.test_username+"3" + "&password=" + self.test_password+"3" + "&newpassword=" + self.test_password+"4"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        self.tmp_test_data["newpassword"] = responseObj["newpassword"]
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("newpassword" in responseObj)
    
    # Test user deletion...
    def test_0900_delete(self):
        self.log.debug("I want to delete a user")
        url = self.auth_api_url + "delete/?username=" + self.test_username + "&password=" + self.test_password
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)
            
    # Test user deletion...
    def test_0901_delete(self):
        self.log.debug("I want to delete a user")
        url = self.auth_api_url + "delete/?username=" + self.test_username+"1" + "&password=" + self.test_password+"1"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)    
        
    # Test user deletion...
    def test_0902_delete(self):
        self.log.debug("I want to delete a user")
        url = self.auth_api_url + "delete/?username=" + self.test_username+"2" + "&password=" + self.test_password+"2"
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)      
        
    # Test user deletion...
    def test_0903_delete(self):
        self.log.debug("I want to delete a user")
        url = self.auth_api_url + "delete/?username=" + self.test_username+"3" + "&password=" + self.tmp_test_data["newpassword"]
        ret = requests.get(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        #self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)          
    
    # Test group deletion...
    def test_0900_delete_group(self):
        self.log.debug("I want to delete a group")
        url = self.auth_api_url + "group/?name=" + self.test_group_name
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)    
        
    # Test group deletion...
    def test_0901_delete_group(self):
        self.log.debug("I want to delete a group")
        url = self.auth_api_url + "group/?name=" + self.test_group_name + "1"
        ret = requests.delete(url, headers={'X-Voolks-App-Id': self.app_id, 'X-Voolks-Api-Key': self.app_key}, verify=False)
        # self.log.debug("Raw response from api: " + ret.text)
        responseObj =  json.loads(ret.text)
        #self.log.debug("Response from api: " + json.dumps(responseObj))
        self.assertTrue("code" in responseObj and responseObj["code"] == 1)        