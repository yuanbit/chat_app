## Single Channel Chat Application with Sentiment Analysis

### Features:
• Implemented with Python Flask-SocketIO

• Database using PostgreSQL

• Sentiment Analysis using AYLIEN Text Analysis API
  * The emojis :), :(, or :| will be displayed at the end of each message depending on the detected emotion
  * The credentials will expire on Jan 28, 2020

• Deployed using Heroku: https://flask-chat-yuan.herokuapp.com/

### Files:

**• app.py:** Main application file for the route of the registration and login page as well as the Flask-SocketIO communication with the client

**• db.py:** Defines the model using Flask-SQLAlchemy for user data

**• wtform_fields.py:** Defines the registration and login forms as classes using Flask-WTForms and validators for input verification (length, duplicate detection, etc.)

**• Procfile:** Specifies the commands for Heroku

**• requirements.txt:** Required python packages

**• templates/:** HTML files
  * **main_layout.html:** General layout set-up for the forms
  * **macros.html:** Helper template for the forms
  * **login.htmlL** Login page
  * **index.html:** Registration page
  * **chat.html:** Chat page
  * **404.html:** Not found page
  
**• static/:** Javascript and CSS files
  * **scripts/chat_page.js:** Sending messages on keypress
  * **scripts/socketio.js:** SocketIO communication with the server and displaying chat data 
  * **style/style.css:** Style for registration, login,and 404 pages
  * **style/chat_style.css:** Style for chat page
  
