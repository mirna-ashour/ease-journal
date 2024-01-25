
# Flask API
An example Flask REST API server for a journaling application powered by OpenAI's GPT3. This API offers journaling insights and prompts based on the user's journal entries.

## Getting Started
To build for production, type `make prod`.

To set up the development environment for a new developer, run `make dev_env`.

## Endpoints
- **/hello**: A basic endpoint for testing server connectivity. Returns a "hello world" response.
- **/endpoints**: Lists all available endpoints in the system.
- **/** or **/MainMenu**: Provides a main menu interface with various options:
  - List user account information
  - List user journal categories
  - List all user journal entries
  - List all users
  - Exit
- **/users**: Supports fetching a list of all users and adding a new user.
- **/users/update/<user_id>**: Updates a user's information.
- **/users/delete/<user_id>**: Deletes a user by their ID.
- **/categories**: Supports fetching a list of all journal categories and adding a new category.
- **/categories/update/<category_id>**: Updates a category's information.
- **/categories/<user_id>**: Retrieves categories for a specific user.
- **/categories/delete/<category_id>**: Deletes a category by its ID.
- **/journals**: Supports fetching a list of all journal entries and adding a new journal entry.
- **/journals/update/title/<timestamp>/<new_title>**: Updates the title of a journal entry.
- **/journals/update/content/<timestamp>/<new_content>**: Updates the content of a journal entry.
- **/journals/delete/<timestamp>**: Deletes a journal entry by its timestamp.

## Documentation
- [Design Specifications](/documentation/design_doc.md)
- [Progress and Goals](/documentation/ProgressAndGoals.md)

## About
This Flask API serves as the backend for a journaling application. It leverages OpenAI's GPT-3 to provide journaling insights and prompts based on user journal entries.
