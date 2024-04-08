
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
- **User Management:** Create, update, and delete user profiles. Enhanced validation ensures integrity of user data.
- **Category Management:** Improved category management with validation for uniqueness and the ability to handle duplicates gracefully. Users can add, update, and delete categories for better organization of journal entries.
- **Journal Management:** Users can add, update, and delete journal entries, with improvements in handling and organization.
- **Insights and Prompts:** Future feature to leverage AI for offering journaling insights and prompts based on user entries.

## Updates and Improvements
- Extensive unit testing added for reliability and performance.
- Enhanced user management features with robust validation for emails and passwords.
- Improved category management with duplicate handling and title validation.
- Refactored and optimized journal entry management for better usability.

## Endpoints Overview
The API provides several endpoints to interact with the journaling application, including user, category, and journal management:
- **User Endpoints:** `/users`, `/users/update/<user_id>`, `/users/delete/<user_id>`
- **Category Endpoints:** `/categories`, `/categories/update/<category_id>`, `/categories/<user_id>`, `/categories/delete/<category_id>`
- **Journal Endpoints:** `/journals`, `/journals/update/<journal_id>`, `/journals/delete/<journal_id>`

## Documentation
- [Design Specifications](/documents/design_doc.md)
- [API Reference](/documents/api_reference.md)
- [Progress and Goals](/documents/ProgressAndGoals.md)

## Contributing
Contributions are welcome. Please refer to our contribution guidelines for more details.

## About
Ease Journal is a journaling application designed to help users document their thoughts, reflections, and daily activities, leveraging Flask and OpenAI's GPT-3 technology for a seamless experience.

## React App
For the front-end experience, visit the [Ease Journal Frontend](https://github.com/mirna-ashour/ease-journal-frontend) repository.
