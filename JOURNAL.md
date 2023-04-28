# Initial thoughts on the project
## Choose which paradigme to use
A RESTful API seemed like a good choice.
Microservices are all the rage but for such a little application it would be overkill.
Plus I have never worked with this paradigm.
But I understand the attraction and as I have three services to implement it is still a valid choice.
As I am to focus on the back-end I also chose to setup a SQLite db and use it directly if come to the front-end instead of local data.
Two tables seem sufficient, one for the feedbacks and the other for the reactions to the feedback

## Choose a technology stack
As I have never used NodeJS I decided to implement the service in Python.

I have used Flask in the past and I knew it is simple enough to setup.
A quick search confirmed it would provide all I need for a REST implementation.
If installed with [async], we can get Flask to respond asynchronically to requests.
Flask-SQLAlchemy will be used as an ORM to interact with the DB.

As for  the db, I will use SQLite as it is adequate for a small project like this.

# Development process
## Preparation
### Venv and PIP
I setup a virtual env to install necessary Python package with PIP, listed in requirements.txt
I do this to not mix between python packages managed by my OS package manager and those that I must install with PIP.
It also make the project easily portable.
### Git
Init a git repo and switch to a dev branch

## Code
### Basic Flask server
Create a working Flask server, responding to HTTP queries and verify it's working.
### Base module with classes
I setup a module model with two classes, one for the feedback table and the other for the reaction table
Reactions can be a comment about a feedback,
