"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

import datetime
# from urllib import request
from data import categories
from flask import Flask, request
from flask_restx import Resource, Api
import werkzeug.exceptions as wz

import data.users as users


app = Flask(__name__)
api = Api(app)

MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Ease Journal"
# USERS = 'users'
USERS_EP = '/users'
DATA = 'Data'
TYPE = 'Type'
TITLE = 'Title'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'/{MAIN_MENU}')
@api.route('/')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 1,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List user account information'},
                    '2': {'url': '/', 'method': 'get',
                          'text': 'List user journal categories'},
                    '3': {'url': '/', 'method': 'get',
                          'text': 'List all user journal entries'},
                    '4': {'url': f'/{USERS_EP}', 'method': 'get',
                          'text': 'List all users'},
                    'X': {'text': 'Exit'},
                }}


@api.route(USERS_EP)
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: users.get_users(),
        }


@api.route('/add_category')
class AddCategory(Resource):
    def post(self):
        # parsing the request data
        data = request.get_json()
        user = data.get('user_id')
        title = data.get('title', "Untitled")
        date_time_str = data.get('date_time')

        # validating input
        if not user:
            raise wz.ServiceUnavailable('We have a technical problem.')
        try:
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

        # generating a unique category ID to be implemented later !!!!!
        # category_id = generate_unique_category_id()
        category_id = 1231346

        # add the new category to user
        categories.add_category(category_id, title, user, date_time)

        return {"category_id": category_id}, 200
