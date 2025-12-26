# Vocabulary Log App
#### Video Demo: https://youtu.be/0zvwzDG-s3w?si=9QkZmCY8_FvKyZWA
#### Description:


This is a simple flask application that help users store, organize and manage their vocabulary collections, therefore serving not only as a record for learning but also a second brain. Being built with a flask framework combined with languages like python and SQLite, users can insert and categorize words in decks, be it by the type of vocabulary or difficulty. After creating the deck, users can enter vocabulary along with the meaning and example to learn the usage of the word or the phrase. Upon the entry of words, the interface also supports features such as searching, editing and deleting words. Users must log into their account to ensure personalized usage and access control. The application is ideal for language learners and students looking to enrich their vocabulary due to the distraction-free layout with Bootstrap style to support both desktop and mobile devices.

The app contains several files which will be listed and explained below.

App.py

This is the main backend file of the application which uses a flask framework and written in python. It includes all the routes and carry out multiple tasks like rendering templates, validating the data submitted through HTML forms, interacting with the sqlite database and managing user sessions. So, it handles all the features of the app such as creating decks, adding words into the deck, viewing and editing words and decks.

Helpers.py

This file is a module that app.py uses to access reusable utility functions. Key functionalities include rendering user-friendly error messages or apologies to the user and ensuring user-specific content access by handling sessions. By modularizing these functions, different routes within app.py can reuse the same functionality.

Projects.db

This SQLite database plays a central role as it serves as the back storage of the application. It contains multiple tables for different features of the app. For instance, the table, users, stores user id, name and password which enables the functionality of user accounts. The tables "words" and "decks" store all the vocabularies by linking to each other with primary keys and foreign keys. When loading the data, each route uses different database queries to filter the required words and decks through the tables.

Let us now move on to the templates directory where all the pages for the app are stored.

Layout.html

This is the base template that all other pages are extended with Jinja's {% extends layout.html %} syntax. It provides a consistent layout and style across all pages because not only does the template centralize the main html structure such as <head> and <body> but the bootstrap conclusion is also unified.

Register.html

This is where the users create a new account. The template contains a registeration form with fields for username, password and password confirmation. Submitting the form sends the data to the register route where the credentials are inserted into the database. Potential errors such as existing username or mismatched passwords are handle and error messages are rendered.

Login.html

This template includes a form through which the user enter their username and password, and access their personalized contents. Clicking on the button sends the data to the login route. Then app.py search through the database for the username and password. Not to mention, relevant error messages are rendered if the provided credentials are invalid. Then, a successful login redirects users to the home page, index.html.

Index.html

This is the home page after loggin in which shows all the decks the user has created. It includes a welcome message by name, displaying the list of decks in a bootstrap-styled table. The table contains the deck name, description and a bunch of actions add words, edit the deck details to view the words inside.

Create_deck.html

This page is accessed via the "+New Deck" button in index.html. Get method will render the template but entering the new deck's name and description or using Post method will send the data to create_deck route where the data is inserted into the deck table of the database.

Add.html

Similar to create_deck.html, this page is used to add words to a specific deck. It lets the user to enter a word, its meaning and its example usage while passing the
deck_id as a query parameter to ensure the word is added to a correct deck. A successful addition redirects to the view page.

View.html

This page shows all words within a specific deck. It can be accessed via the view button on home page or redirected from the add page after a successful addition. It displays a searchable table with the columns word, meaning, example and actions buttons. Searching for a word will filter out the word list in real time using JavaScript.

Edit_deck.html and edit_word.html

These pages allow user to modify existing deck and word details. When loaded, the pages shows form inputs with existing values pre-filled. Submitting the forms sends data to the corresponding routes and update the database.


