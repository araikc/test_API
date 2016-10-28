
'''
Basic positive tests for "https://beta.1neschool.com" API testing.
Tests are implemented using 'unittest' python framework.
Used 'requests', 'json' modules.
'''

import requests
import unittest
import json

HOST = "beta.1neschool.com"
PROTOCOL = "https"
DEFAULT_HEADER = 'application/json'
SUCCESS = 200
INCORRECT_HEADER = 400
NAME = 'Test Name'
USERID="test111@example.com"
PASS="test_password"
#USERID="admin@hamoye.com"
#PASS="BQ4AT&i+o9B?zqUAVPwYUVEDcCLBsUZoDR"

class TestServerFunctionality(unittest.TestCase):

    def __init__(self, *a, **kw):
        super(TestServerFunctionality, self).__init__(*a, **kw)
        self.url = '{}://{}'.format(PROTOCOL, HOST)
	TestServerFunctionality.session = requests.session()

    def test_1register_user(self):
	'''
		Positive functional test for registering user via '/core/users' service
		Checkpoits: response status, response fields existance and types
	'''

	api="{}/{}".format(self.url, "core/users")
	data={
        		'authType': 'DbAuthTypeInternal',
        		'authAccountId': USERID,
        		'password': PASS,
        		'name': NAME,
        		'remember': True
	     }
        status_code, text = self._post_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, text)
       	self.assertIn('userId', text.keys())
       	self.assertIn('sessionId', text.keys())


    def test_2register_user_incorrect_header(self):
	'''
		Negative test for registering user via '/core/users' service
		Wrong header will be sent
		Checkpoits: resopnse status check
	'''

	api = "{}/{}".format(self.url, "core/users")
	data = {
        		'authType': '',
        		'authAccountId': '',
        		'password': '',
        		'name': '',
        		'remember': False
	       }
        status_code, text = self._post_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, INCORRECT_HEADER, text)


    def test_3retrieve_user_id(self):
	'''
		Positive test for retrieving user id via '/acl/auth' service
		Checkpoits: response status, response fields existance and types
	'''

	api = "{}/{}/{}/{}".format(self.url, "acl/auth", "Internal", USERID)
	data = {'password' : PASS, 'remember' : True}
        status_code, text = self._post_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, text)

        self.assertIn('userId', text.keys())
        self.assertIn('sessionId', text.keys())
    	TestServerFunctionality.uid = text['userId']
    	TestServerFunctionality.sid = text['sessionId']


    def test_4retrieve_user_data(self):
	'''
		Positive test for retrieving account data via '/core/users' service
		Checkpoits: response status, response fields existance, types and correctnes
	'''

	api="{}/{}/{}".format(self.url, "core/users", TestServerFunctionality.uid)
        status_code, account = self._get_request(api=api, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, account)
       	self.assertIn('id', account.keys())
       	self.assertTrue(isinstance(account['id'], unicode))
       	#self.assertIn('accountId', account.keys())
       	#self.assertTrue(isinstance(account['accountId'], int))
       	#self.assertIn('handle', account.keys())
       	#self.assertTrue(isinstance(account['handle'], str))
       	self.assertIn('fullName', account.keys())
       	self.assertEqual(NAME, account['fullName'])
       	self.assertTrue(isinstance(account['fullName'], unicode))
       	#self.assertIn('avatarId', account.keys())
       	#self.assertTrue(isinstance(account['avatarId'], str))
       	self.assertIn('about', account.keys())
       	self.assertTrue(isinstance(account['about'], unicode))
       	self.assertIn('creationTime', account.keys())
       	self.assertTrue(isinstance(account['creationTime'], unicode))
       	self.assertIn('roles', account.keys())
       	self.assertTrue(isinstance(account['roles'], list))


    def test_5update_user_data(self):
	'''
		Positive test for updating account data via '/core/users/{id}' service
		Checkpoits: response status, updated fields existance in response, types and correctnes
	'''

	api="{}/{}/{}".format(self.url, "core/users", TestServerFunctionality.uid)
	data = {
        		'fullName': 'New Test Name',
        		'about': 'update_about',
        		'avatarId': 'new_id'
	       }
	status_code, account = self._patch_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, account)
	api="{}/{}/{}".format(self.url, "core/users", TestServerFunctionality.uid)
        status_code, account = self._get_request(api=api, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, account)

	self.assertIn('fullName', account.keys())
	self.assertEqual(u'New Test Name', account['fullName'])
	self.assertIn('about', account.keys())
	self.assertEqual(u'update_about', account['about'])
	self.assertIn('avatarId', account.keys())
	self.assertEqual('new_id', account['avatarId'])

	# Revert changes
	data = {
        		'fullName': 'Test Name',
        		'about': '',
        		'avatarId': ''
	       }
	status_code, account = self._patch_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, account)
	api="{}/{}/{}".format(self.url, "core/users", TestServerFunctionality.uid)
        status_code, account = self._get_request(api=api, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, account)

	self.assertIn('fullName', account.keys())
	self.assertEqual(u'Test Name', account['fullName'])
	self.assertIn('about', account.keys())
	self.assertEqual(u'', account['about'])
	self.assertIn('avatarId', account.keys())
	self.assertEqual('', account['avatarId'])


    def test_6grand_role(self):
	'''
		Positive test for adding role to account via '/core/users/{id}/roles' service
		Checkpoits: status of response, corrected of new roles
	'''

	api="{}/{}/{}/{}".format(self.url, "acl/users", TestServerFunctionality.uid, "roles")
	data={
        		'role': 'DbRoleModerator'
	     }
        status_code, text = self._post_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, text)

	api="{}/{}/{}".format(self.url, "core/users", TestServerFunctionality.uid)
	status_code, account = self._get_request(api=api, headers=DEFAULT_HEADER)
	self.assertEqual(status_code, SUCCESS, account)

	self.assertIn('roles', account.keys())
	self.assertIn('DbRoleModerator', account['roles'])


    def test_7revoke_role(self):
	'''
		Positive test for removing role from account via '/core/users/{id}/roles' service
		Checkpoits: status of response, corrected of new roles
	'''

	api="{}/{}/{}/{}".format(self.url, "acl/users", TestServerFunctionality.uid, "roles")
	data={
        		'role': 'DbRoleModerator'
	     }
        status_code, text = self._delete_request(api=api, data=data, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, text)

	api="{}/{}/{}".format(self.url, "core/users", TestServerFunctionality.uid)
	status_code, account = self._get_request(api=api, headers=DEFAULT_HEADER)
	self.assertEqual(status_code, SUCCESS, account)

	self.assertIn('roles', account.keys())
	self.assertNotIn('Moderator', account['roles'])


    def test_8create_ticket(self):
	'''
		Positive test for creating ticket via '/tickets' service
		Checkpoits: status of response, corrected of response
	'''

	api="{}/{}".format(self.url, "tickets")
	data={
        		'title': 'new_ticket',
        		'description': 'test description',
        		'type': 'SupportTicket'
	     }
        status_code, text = self._post_request(api=api, data=data, headers=DEFAULT_HEADER)
	TestServerFunctionality.tid = 1
        self.assertEqual(status_code, SUCCESS, text)
	self.assertIn('ticketId', text.keys())
	TestServerFunctionality.tid = text['ticketId']


    def test_9get_ticket(self):
	'''
		Positive test for getting ticket data via '/tickets/{ticketId}' service
		Checkpoits: status of response, corrected of response
	'''

	api="{}/{}/{}".format(self.url, "tickets", TestServerFunctionality.tid)
        status_code, text = self._get_request(api=api, headers=DEFAULT_HEADER)
        self.assertEqual(status_code, SUCCESS, text)
	self.assertIn('title', text.keys())
	self.assertIn('description', text.keys())
	self.assertIn('creationTime', text.keys())
	self.assertIn('updateTime', text.keys())
	self.assertIn('priority', text.keys())
	self.assertIn('state', text.keys())
	self.assertIn('language', text.keys())
	self.assertIn('assignedTo', text.keys())


#########################################################################
# Private utility methods for different type of requests
#########################################################################


    def _post_request(self, api, data, headers):
	_headers = {'Content-Type': headers} if headers else None
	_payload = json.dumps(data) if data else None
	_response = TestServerFunctionality.session.post(api, data=_payload, headers=_headers)
	code, data = _response.status_code, ''
	try:
		data = _response.json()
	except ValueError as e:
		data = {'error': 'No JSON data in response: {}'.format(_response.text)}
        return code, data


    def _get_request(self, api, headers):
        _headers = {'Content-Type': headers}
        _response = TestServerFunctionality.session.get(api, headers=_headers)
	code, data = _response.status_code, ''
	try:
		data = _response.json()
	except ValueError as e:
		data = {'error': 'No JSON data in response: {}'.format(_response.text)}
        return code, data


    def _patch_request(self, api, data, headers):
	_headers = {'Content-Type': headers} if headers else None
	_payload = json.dumps(data) if data else None
        _response = TestServerFunctionality.session.patch(api, data=_payload, headers=_headers)
	code, data = _response.status_code, ''
	try:
		data = _response.json()
	except ValueError as e:
		data = {'error': 'No JSON data in response: {}'.format(_response.text)}
        return code, data


    def _delete_request(self, api, data, headers):
	_headers = {'Content-Type': headers} if headers else None
	_payload = json.dumps(data) if data else None
	_response = TestServerFunctionality.session.delete(api, data=_payload, headers=_headers)
	code, data = _response.status_code, ''
	try:
		data = _response.json()
	except ValueError as e:
		data = {'error': 'No JSON data in response: {}'.format(_response.text)}
        return code, data


if __name__ == '__main__':
    unittest.main(verbosity=2)

