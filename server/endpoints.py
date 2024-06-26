"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

# import datetime as dt
# from urllib import request
from flask import Flask, request
from http import HTTPStatus
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz
from flask_cors import CORS

import data.users as usrs
import data.journals as journals
import data.categories as categories
import forms.SignUp_form as SignUp


app = Flask(__name__)
api = Api(app)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Ease Journal"
# USERS = 'users'
USERS_EP = '/users'
USER_ID = 'User ID'
CATEGORY_ID = 'Category ID'
JOURNAL_ID = 'Journal ID'
DELETE = 'delete'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
JOURNALS_EP = '/journals'
CATEGORIES_EP = '/categories'
DEL_CATEGORY_EP = f'{CATEGORIES_EP}/{DELETE}'
DEL_JOURNAL_EP = f'{JOURNALS_EP}/{DELETE}'
DATA = 'Data'
TYPE = 'Type'
TITLE = 'Title'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
SIGNUP = 'signup'
FORM = 'form'
SIGNUP_FORM = 'signup_form'


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


user_fields = api.model('NewUser', {
    usrs.FIRST_NAME: fields.String,
    usrs.LAST_NAME: fields.String,
    usrs.DOB: fields.String,
    usrs.EMAIL: fields.String,
    usrs.PASSWORD: fields.String,
})


@api.route(f'{USERS_EP}/<user_id>')
class UpdateUser(Resource):
    """
    Updates a user's information.
    """
    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def put(self, user_id):
        """
        Update a user's information.
        """
        user_data = request.json
        try:
            updated = usrs.update_user(user_id, user_data)
            if not updated:
                raise wz.NotFound(f'User with {USER_ID} {user_id} not found')
            return {f'Updated user with {USER_ID}': user_id}
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')


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
        password = request.json[usrs.PASSWORD]
        try:
            new_id = usrs.add_user(user_id, first_name, last_name,
                                   dob, email, password)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {f'New user has been added; with {USER_ID}': user_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{USERS_EP}/<identifier>')
class GetUser(Resource):
    """
    This class supports:
        - retrieving a user by their ID or email
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, identifier):
        """
        This method retrieves a user by their ID or email.
        """
        try:
            user = usrs.get_user(identifier)
            if not user:
                raise wz.NotFound(f'User with {USER_ID} or {usrs.EMAIL} ' +
                                  f'{identifier} not found')
            return user
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')


category_post_fields = api.model('NewCategory', {
    categories.CATEGORY_NAME: fields.String(default=""),
    categories.USER: fields.String,
})


category_put_fields = api.model('UpdateCategory', {
    categories.CATEGORY_NAME: fields.String(default=""),
})


@api.route(f'{CATEGORIES_EP}/<user_id>')
class GetCategory(Resource):
    """
    This class supports:
        - retrieving categories for a user
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, user_id):
        """
        This method returns all categories for a user.
        """
        data = categories.get_user_categories(user_id)
        if data:
            return {
                TYPE: DATA,
                TITLE: 'Categories for user',
                DATA: data
            }
        # else:
        #     raise wz.NotAcceptable(
        #         'There are no categories under this user.'
        #     )


@api.route(f'{CATEGORIES_EP}/<category_id>')
class UpdateCategory(Resource):
    """
    Updates a category's details.
    """
    @api.expect(category_put_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def put(self, category_id):
        """
        Update a category's details.
        """
        category_data = request.json
        try:
            updated = categories.update_category(category_id, category_data)
            if not updated:
                raise wz.NotFound(f'Category with '
                                  f'{CATEGORY_ID} {category_id} not found')
            return {f'Updated category with {CATEGORY_ID}': category_id}
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')


@api.route(f'{DEL_CATEGORY_EP}/<category_id>')
class DelCategory(Resource):
    """
    Deletes a category by its ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, category_id):
        """
        Deletes a category by its ID.
        """
        try:
            categories.del_category(category_id)
            return {f'Deleted category with {CATEGORY_ID}': category_id}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(CATEGORIES_EP)
class Category(Resource):
    """
    This class supports:
        - fetching a list of all users
        - adding a user
    """
    def get(self):
        """
        This method returns all categories.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Categories',
            DATA: categories.get_categories(),
        }

    @api.expect(category_post_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a category.
        """
        category_id = categories._get_category_id()
        category_name = request.json[categories.CATEGORY_NAME]
        user_id = request.json[categories.USER]
        if not usrs.exists(user_id):
            raise wz.NotAcceptable("Please input a user ID that exists.")

        try:
            new_id = categories.add_category(category_id, category_name,
                                             user_id)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {f'New category added; with {CATEGORY_ID}': category_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


journal_post_fields = api.model('Journal Post', {
    journals.TITLE: fields.String,
    journals.PROMPT: fields.String,
    journals.CONTENT: fields.String,
    journals.USER: fields.String,
    journals.CATEGORY: fields.String,
})


journal_put_fields = api.model('Journal Put', {
    journals.TITLE: fields.String(default=""),
    journals.PROMPT: fields.String(default=""),
    journals.CONTENT: fields.String(default=""),
    journals.CATEGORY: fields.String(default=""),
})


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

    @api.expect(journal_post_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method adds a journal entry.
        """
        journal_id = journals._get_journal_id()
        title = request.json[journals.TITLE]
        prompt = request.json[journals.PROMPT]
        content = request.json[journals.CONTENT]
        user_id = request.json[journals.USER]
        category_id = request.json[journals.CATEGORY]

        if not usrs.exists(user_id):
            raise wz.NotAcceptable("Please input a user ID that exists.")
        if not categories.exists(category_id):
            raise wz.NotAcceptable("Please input a category ID that exists.")

        try:
            ret = journals.add_journal(journal_id, title, prompt, content,
                                       user_id, category_id)
            if ret is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {JOURNAL_ID: journal_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{JOURNALS_EP}/<journal_id>')
class UpdateJournal(Resource):
    """
    Updates a Journal's details.
    """
    @api.expect(journal_put_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def put(self, journal_id):
        """
        Update a Journals's details.
        """
        journal_data = request.json
        try:
            updated = journals.update_journal(journal_id, journal_data)
            if not updated:
                raise wz.NotFound(f'Journal with '
                                  f'{JOURNAL_ID} {journal_id} not found')
            return {f'Updated Journal with {JOURNAL_ID}': journal_id}
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')


@api.route(f'{DEL_JOURNAL_EP}/<journal_id>')
class DelJournal(Resource):
    """
    Deletes a journal by its ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, journal_id):
        """
        Deletes a journal by ID.
        """
        try:
            journals.del_journal(journal_id)
            return {f'Deleted journal with {JOURNAL_ID}': journal_id}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{JOURNALS_EP}/<category_id>')
class GetJournals(Resource):
    """
    This class supports:
        - retrieving journals for a category
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, category_id):
        """
        This method returns all journals for a category.
        """
        data = journals.get_category_journals(category_id)
        if data:
            return {
                TYPE: DATA,
                TITLE: 'Journals for category',
                DATA: data
            }
        # else:
        #     raise wz.NotAcceptable(
        #         'There are no journals under this category.'
        #     )


@api.route(f'/{SIGNUP}/{FORM}')
class SignUpForm(Resource):
    """
    Get the form for a new user to sign up
    """
    def get(self):
        """
        Get the form for a new user to sign up
        """
        return {SIGNUP_FORM: SignUp.get_form()}
