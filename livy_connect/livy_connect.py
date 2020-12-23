import json
import requests
import textwrap
from pprint import pprint
from time import sleep


class LivyConnect:
    """
    LivyConnect
    """
    _HOST = 'localhost' # Default IP address of host
    _PORT = 8998 # Default Port 
    _headers = {'Content-Type': 'application/json'}
    code_type = 'spark' #default code type

    def __init__(self, host=None, port=None, 
            code_type=None, session_id=None
        ):
        if host:
            self._HOST = host
        if port:
            self._PORT = port
        if session_id:
            self._session_id = session_id
        if code_type:
            self.code_type = code_type
        self.uri = 'http://{}:{}'.format(self._HOST, self._PORT)

    def _get_uri (self, url_appender=None): 
        if url_appender:
            return (self.uri + url_appender)
        return self.uri

    def get_sessions_list(self):
        response = requests.get(
            self._get_uri('/sessions')
            )
        
        if not response.ok:
            raise Exception(response.json().get("msg"))
        
        result = response.json().get("sessions", [])
        # result = list(map(self._response_mapper, result))
        return result

    @staticmethod
    def _response_mapper(session):
        return {
            'session_id': session['id'],
            'status': session['state']
        }

    def create_session(self, code_type=None, session_name=None):
        if code_type:
            self.code_type = code_type
        data = {'kind': self.code_type}
        if session_name:
            data['name']=session_name
        response = requests.post(
            self._get_uri('/sessions'), 
            data=json.dumps(data), 
            headers=self._headers
            )

        if not response.ok:
            raise Exception(response.json().get("msg"))

        # pprint(response.json())
        self._session_id = response.headers['Location'].split('/')[-1]
        print("Session Created With Id : {}".format(self._session_id))
        return response.json()

    def session_details(self, session_id=None):
        if not session_id:
            session_id = self._session_id
        session_url = self._get_uri('/sessions/{}'.format(session_id))
        response = requests.get(
            session_url, 
            headers=self._headers
            )

        if not response.ok:
            raise Exception(response.text)
        # pprint(response.json())
        return response.json()

    def session_status(self, session_id=None):
        result  = self.session_details(session_id).get('state')
        print(result)
        # return result.get('state')
        return result

    def get_codes_list(self, session_id=None):
        if not session_id:
            session_id = self._session_id
        session_url = self._get_uri('/sessions/{}/statements'.format(session_id))
        response = requests.get(
            session_url, 
            headers=self._headers
            )

        if not response.ok:
            raise Exception(response.json().get("msg"))
        result = response.json().get('statements',[])
        return result

    def post_code(self, code_block, session_id=None):
        if not session_id:
            session_id = self._session_id
        data = {'code': code_block}
        session_url = self._get_uri('/sessions/{}/statements'.format(session_id))
        response = requests.post(
            session_url, 
            data=json.dumps(data), 
            headers=self._headers
            )

        pprint(response.json())
        self._code_id = response.headers['Location'].split('/')[-1]
        return response.json()

    def code_block_details(self, code_block_id=None, session_id=None):
        if not session_id:
            session_id = self._session_id
        if not code_block_id:
            code_block_id = self._code_id
        session_url = self._get_uri('/sessions/{}/statements/{}'.format(session_id, code_block_id))
        response = requests.get(
            session_url,
            headers=self._headers
            )

        if not response.ok:
            raise Exception(response.json().get("msg"))
        
        # pprint(response.json())
        return  response.json()

    def code_block_status(self, code_block_id=None, session_id=None):
        result = self.code_block_details(code_block_id, session_id).get("state")
        print(result)
        # return  result.get("state")
        return  result

    def delete_session(self, session_id=None):
        if not session_id:
            session_id = self._session_id
        session_url = self._get_uri('/sessions/{}'.format(session_id))
        response = requests.delete(
            session_url, 
            headers=self._headers
            )
        if not response.ok:
            raise Exception(response.json().get("msg"))
        print("Session Deleted, Id : {}".format(session_id))


class LivySession(LivyConnect):
    closed = False
    def __init__(self, host):
        super().__init__(host=host)
        super().create_session()
        print("Creating session")

    def __enter__(self):
        return super()
    
    def __exit__(self, type, value, traceback):
        self.close()
    
    def close(self):
        x = super().delete_session()
        if not x:
            self.closed = True
        else:
            self.closed = False  
