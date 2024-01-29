# Progress and Goals


## Progress:

- Created an API server with endpoints following CRUD operations on related data.
- Endpoints:
	- POST `/journals` - Adds a journal entry
	- GET `/journals` - Returns all journal entries
	- DELETE `/journals/delete/{timestamp}` - Deletes a journal entry by timestamp
	- PUT `/journals/{timestamp}` - Updates details of a journal entry
	- GET `/users` - Returns all users.
	- POST `/users` - Adds a user.
	- DELETE `/users/delete/{user_id}` - Deletes a user by their ID.
	- PUT `/users/{user_id}` - Updates a user's information.
	- GET `/categories` - Returns all categories.
	- POST `/categories` - Adds a category.
	- DELETE `/categories/delete/{category_id}` - Deletes a category by its ID.
	- PUT `/categories/{category_id}` - Updates a category's details.
	- GET `/categories/{user_id}` - Returns categories for a specific user.
	- 
	- 
- Endpoints and data module functions have unit tests to verify correct behavior, document expected behavior, isolate issues, and receive rapid feedback.


## Goals:

- Currently missing unit tests for our data modules will be created to improve coverage.
- 
