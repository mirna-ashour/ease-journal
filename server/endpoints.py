"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

import datetime as dt
# from urllib import request
from data import categories
from flask import Flask, request
from http import HTTPStatus
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz

import data.users as usrs
import data.journals as journals


app = Flask(__name__)
api = Api(app)

MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Ease Journal"
# USERS = 'users'
USERS_EP = '/users'
USER_ID = 'User ID'
DELETE = 'delete'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
JOURNALS_EP = '/journals'
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


@api.route(f'{DEL_USER_EP}/<user_id>')
class DelUser(Resource):
    """
    Deletes a user by their ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, user_id):
        """
        Deletes a user by their ID.
        """
        try:
            usrs.del_user(user_id)
            return {f'Deleted user with {USER_ID}': user_id}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


user_fields = api.model('NewUser', {
    # usrs.USER_ID: fields.String,
    usrs.FIRST_NAME: fields.String,
    usrs.LAST_NAME: fields.String,
    usrs.DOB: fields.String,
    usrs.EMAIL: fields.String,
})


@api.route(USERS_EP)
class Users(Resource):
    """
    This class supports:
        - fetching a list of all users
        - adding a user
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: usrs.get_users(),
        }

    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        user_id = usrs._get_user_id()
        first_name = request.json[usrs.FIRST_NAME]
        last_name = request.json[usrs.LAST_NAME]
        dob = request.json[usrs.DOB]
        email = request.json[usrs.EMAIL]
        try:
            new_id = usrs.add_user(user_id, first_name, last_name, dob, email)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {f'New user has been added; with {USER_ID}': user_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route('/add_category')
class AddCategory(Resource):
    def post(self):
        '''This endpoint adds a new category to the database.'''
        # parsing the request data
        data = request.get_json()
        user = data.get('user_id')
        title = data.get('title', "Untitled")
        date_time_str = data.get('date_time')

        # validating input
        if not user:
            raise wz.ServiceUnavailable('We have a technical problem.')
        try:
            date_time = dt.datetime.strptime(date_time_str,
                                             "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

        # generating a unique category ID to be implemented later !!!!!
        # category_id = generate_unique_category_id()
        category_id = 1231346
        try:
            categories.add_category(category_id, title, user, date_time)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

        return {"category_id": category_id}, 200


journal_fields = api.model('NewJournal', {
    journals.TIMESTAMP: fields.String,
    journals.TITLE: fields.String,
    journals.PROMPT: fields.String,
    journals.CONTENT: fields.String,
    journals.MODIFIED: fields.String,
})

JOURNAL_ID = 'Journal ID'


@api.route(JOURNALS_EP)
class Journals(Resource):
    """
    This class supports:
        - fetching a list of all journals
        - adding a journal
    """
    def get(self):
        """
        This method returns all journals.
        """
        return {
            TYPE: DATA,
            TITLE: 'All Journals',
            DATA: journals.get_journals(),
        }

    @api.expect(journal_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method adds a journal entry.
        """
        timestamp = request.json[journals.TIMESTAMP]
        title = request.json[journals.TITLE]
        prompt = request.json[journals.PROMPT]
        content = request.json[journals.CONTENT]
        modified = request.json[journals.MODIFIED]
        try:
            new_id = journals.add_journal(timestamp, title,
                                          prompt, content, modified)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {JOURNAL_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# @api.route('/delete_journal', methods=['DELETE'])
# class DeleteJournal(Resource):
#     def delete(self):
#         data = request.get_json()
#         timestamp = data.get('timestamp')
#         if not timestamp:
#             raise wz.BadRequest("Timestamp is required")

#         if journals.del_journal(timestamp):
#             return {"message": "Journal deleted successfully"}, 200
#         else:
#             raise wz.NotFound("Journal not found")
