
<p align="center">
    <img src="documents/src/EaseJournalLOGO_V1_vector.png" alt="logo">
</p>

<p align="center">
[EASE-JOURNAL]
</p>

# Flask API for Ease Journal
A Flask REST API server for a journaling application, providing users with the ability to create and manage journals, categories, and user profiles. This API serves as the backend infrastructure, offering CRUD operations for journals, categories, and users.

## Getting Started
To get started with the Ease Journal Flask API, follow the setup instructions below:
- **For Production:** Run `make prod` to build the application for production use.
- **For Development:** Execute `make dev_env` to set up the development environment.

## Features
- User management: Create, update, and delete user profiles.
- Journal management: Users can add, update, and delete journal entries.
- Category management: Organize journal entries into categories for better organization.
- Insights and prompts: Leverage AI to offer journaling insights and prompts based on user entries (future feature).

## Endpoints Overview
The API provides several endpoints to interact with the journaling application:
- **User Endpoints:**
  - `/users`: Fetch all users or add a new user.
  - `/users/update/<user_id>`: Update a user's information.
  - `/users/delete/<user_id>`: Delete a user by their ID.
- **Category Endpoints:**
  - `/categories`: Fetch all categories or add a new category.
  - `/categories/update/<category_id>`: Update a category's information.
  - `/categories/<user_id>`: Retrieve categories for a specific user.
  - `/categories/delete/<category_id>`: Delete a category by its ID.
- **Journal Endpoints:**
  - `/journals`: Fetch all journal entries or add a new entry.
  - `/journals/update/<timestamp>`: Update a journal entry.
  - `/journals/delete/<timestamp>`: Delete a journal entry by its timestamp.

## Documentation
For more information on the API design, features, and usage, refer to the following documentation:
- [Design Specifications](/documents/design_doc.md)
- [API Reference](/documents/api_reference.md)
- [Progress and Goals](/documents/ProgressAndGoals.md)

## Contributing
Contributions to the Ease Journal Flask API are welcome. Please refer to our contribution guidelines for more details.

## About
Ease Journal is a journaling application designed to help users document their thoughts, reflections, and daily activities. By leveraging the Flask framework and OpenAI's GPT-3 technology, we aim to provide a seamless and insightful journaling experience.

## React App
For a front-end experience, check out the [Ease Journal Frontend](https://github.com/mirna-ashour/ease-journal-frontend) repository, which provides a user-friendly interface to interact with this Flask API.
