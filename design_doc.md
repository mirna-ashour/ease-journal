
# List of ideas for project

- Sports: Soccer clubs stats, achievements, trophies.
    - Keep track of club points, goals, wins, losses, and trophies, etc.
        - Create: “Create” will be used to add clubs to the Db
        - Read: “Read” will be used to get updates and information about certain clubs
        - Update: “Update” will be used to update the club’s points, goals, wins, etc.
        - Delete: “Delete” will be used to remove clubs.

- Health: General info, tips, reminders.
    - Help users stay on top of their appointments, prescriptions, and overall personal health.
        - Create: Add general info/tips. Users can add reminders for appointments and prescriptions with names, time, location, recommended daily dosages, descriptions, etc. Users can also star general info/tips.
        - Read: Users can have access to general info, tips, and reminders.
        - Update: General info/tips can be updated to be kept up do date. Users can update information about their reminders.
        - Delete: General info/tips can be removed if outdated. Users can remove reminders. Users can also unstar general info/tips.

- Journaling application powered by GPT generated prompts (Mirna)
    - Users can create journal entries/reflection under various categories (personal, health, work/school, creative)
    - New entries can be written to respond to prompts generated using previous journal entries for a certain time period (ex. the past week)
    - Provide insights/stats/summaries for personal or creative entries for the user to view
    - Send reminders for updating journals or keeping up a streak
    - Maybe make it mulit-modal by allowing easy insertion of images?

- Video Games and Game Server - Cody’s thinking
    Game Info:
    Game titles, genres, release dates, supported platforms.
    Game server details: IP addresses, regions, player counts, server status (online/offline).
    Keep track of player scores, leaderboards, player profiles, in-game achievements, etc.
    Create (C):
    Game Info: Add a new game to the database with its genre, release date, and supported platforms.
    Server Info: Register a new game server for a specific game, specifying the IP address, region, and current player count.
    Player Profile: Create a new player profile with their username, email, and in-game stats.
    Read (R):
    Game Info: View details of specific games, including its genre, release date, and supported platforms.
    Server Info: View all active servers for a chosen game, or search for servers by region or status.
    Player Profile: View a player's profile, their game stats, and any achievements they have unlocked.
    Update (U):
    Game Info: Update game details, such as its genre or supported platforms.
    Server Info: Update a server's details, like its IP address, region, player count, or server status.
    Player Profile: Update player details, including their email or in-game stats.
    Delete (D):
    Game Info: Remove a game from the database.
    Server Info: Delete a server registration if it's no longer available or relevant.
    Player Profile: Delete a player's profile if they request account removal or violate terms of service.
    - Other Thinking:
    Cross-platform Integration: Ensure our system can manage games from different platforms (e.g., PC, Nintendo Switch, PlayStation). [Increase the project's usability and appeal]
    Server Health Monitoring: Apart from just tracking the server status (online/offline), having metrics for latency, uptime, etc., to provide a comprehensive understanding of the server's     performance.
    Social Features: Incorporate features like adding friends, messaging, or creating gaming clans/groups.
    Game Reviews and Ratings: Allow users to leave reviews and ratings for games, which can be read by other users.
    Security: Implement password encryption, two-factor authentication, and other security measures.
    Notifications: Players can receive notifications for new game releases, server downtimes, friend requests, etc.
    Integration with External Game APIs: To fetch real-time data from games and platforms that offer public APIs.

--------------------------------------------------------------------------------------------------------------------------

# Functional Requirements (for Journaling app):

- Create journal entries 
- Provide prompts to users based on previous journal 
- Update a journal entry 
- Categorize entries into different categories (personal, health, work/school, creative)
- Read previous entries written by users
- Delete a journal entry that the user no longer needs
- Relocation of an entry to another category
- Show/Hide date/time stamps
- Updating journal entry titles (by default null or date)
- Removal/Creation of categories
- A simple searching mechanism to find journal entries
- Duplicate a journal entry
- User can indicate whether or not they want a generated prompt for a new entry
- Recommend personlized prompts to the user within the categories
- Can discard/regenerate personalized prompts 
- Insert images inline within entries 
- Order entries alphabetically by title or by date
- Recovery of deleted categories (recursive)/journal entries


## Overview for Storage 

| User_id  | Name      | Category   | title     | Prompt   | Date      | Entry     |
| -------- | --------  | --------   | --------  | -------- | --------  | --------  |
| ........ | ........  | ........   | ........  | ........ | ........  | ........  | 


## Potential Endpoints

- USER BASED
    - Create user account
    - Retrieve user account information 
    - Retreive categories for a user
    - Retrieve journal entries within a category for a user

- OPEN AI API 
    - Generate prompt from Open AI api given specific parameters 
    - Retrieve previous entries with category as context for a prompt 

- GENERAL UPDATES TO DATABASE
    - update a specific entry  
    - modify title of an entry
    - update category of an entry
    - Add/remove images to an entry
    - Add to/retrieve from trash folder (of deleted categories/journal entries)

    
