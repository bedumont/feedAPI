# Introduction
This is a toy RESTful API providing an interface to post feedbacks about something.
Those feedbacks can be upvoted or downvoted by other users.
They can also be commented.
Comments are subject to votes as well, but cannot be further commented at a secondary level.
As such the comments tree is linear and related to a single feedback.

# Technical overview
The API is written in Python and based on Flask and SQLAlchemy.
Resources are stored in a SQLite database.
An ORM is used to interact with the DB.

* feedAPI/bootstrap.sh is script used to setup the DB if not found and start the flask server on port 5000 ;
* feedAPI/index.py contains route definitions ;
* feedAPI/model/tables.py contains a declarative mapping of the tables ;
* feedAPI/database.db is the database file (generated by bootstrap.sh - ignored by git) ;
* requirements.txt contains the python packages for easy venv deployment.

## Usage

Routes are defined within Flask to answer different HTTP requests (GET, POST and PUT).
The following route are defined :
* /feedback (GET) to fetch all feedbacks ;
* /feedback/\<id\>/comments (GET) to fetch the comment related to feedback with id \<id\>;
* /feedback/\<id\> (GET) to fetch feedback with id \<id\> ;
* /comment/\<id\> (GET) to fetch comment with id \<id\> ;
* /feedback (POST) to post a feedback ;
* /comment (POST) to post a feedback ;
* /feedback/\<id\> (PUT) to react to feedback with id \<id\> ;
* /comment/\<id\> (PUT) to react to comment with id \<id\>.

Resources are exchanged as JSON with the following data (marked * if needed in POST/PUT calls) :
### Feedback
1. id [int] the id of the resource (and primary key in the related table) ;
2. *source [string] the ip of the host that created the resource ;
3. *text [string] the (optional) text of the feedback ;
4. *grade [int] the grade of the feedback (between 1 and 5) ;
5. score [int] the sum of all the upvotes and downvotes (+ the initial score of 1) ;
6. *datetime [datetime] the timestamp when the feedback was posted.
### Comment
1. id [int] the id of the resource (and primary key in the related table) ;
2. *source [string] the ip of the host that created the resource ;
3. target [int] the id of the feedback it relates to ;
3. *text [string] the text of the comment ;
5. score [int] the sum of all the upvotes and downvotes (+ the initial score of 1) ;
6. *datetime [datetime] the timestamp when the comment was posted.
### Reaction
1. id [int] the id of the resource (and primary key in the related table) ;
2. *source [string] the ip of the host that created the resource ;
3. fb_id [int] the id of the feedback it relates to (if related to feedback) ;
3. cmt_id [int] the id of the comment it relates to (if related to comment) ;
5. *value [int] the upvote or down vote (restricted to -1 and +1) ;
6. *datetime [datetime] the timestamp when the reaction was posted.

#### Example 
```
curl -X POST -H "Content-Type: application/json" -d '{
"source": "0.0.0.0",
"text": "Meh...."
"score": "2",
"datetime": "'$(date +%s)'"
}' http://host:5000/feedback
```

## Improvements
Obviously Flask alone is not production ready and should be complimented with a _true_ web server like GUnicorn.
This would allow for multiple concurrent connections to take place.

Testing should be implemented.
Unit testing, for example, coulb setup to test the different route independetly.

# Journal
## Initial thoughts on the project
### Choose which paradigme to use
A RESTful API seemed like a good choice.
Microservices are all the rage but for such a little application it would be overkill.
Plus I have never worked with this paradigm.
But I understand the attraction and as I have three services to implement it is still a valid choice.
As I am to focus on the back-end I also chose to setup a SQLite db and use it directly if come to the front-end instead of local data.
Two tables seem sufficient, one for the feedbacks and the other for the reactions to the feedback

### Choose a technology stack
A quick search confirmed Flask would provide all I need for a REST implementation.
If installed with [async], we can get Flask to respond asynchronically to requests.
Flask-SQLAlchemy will be used as an ORM to interact with the DB.

As for  the db, I will use SQLite as it is adequate for a small project like this.

## Development process
### Preparation
#### Venv and PIP
I setup a virtual env to install necessary Python package with PIP, listed in requirements.txt
I do this to not mix between python packages managed by my OS package manager and those that I must install with PIP.
It also make the project easily portable.
#### Git
Init a git repo and switch to a dev branch

### Code
#### Basic Flask server
Create a working Flask server, responding to HTTP queries and verify it's working.
#### Model module with classes
I setup a model module with three classes, one for the feedback table, one for the comments table, and ont for the reactions table.
They contain the declarative mapping to the database columns for the ORM. 

I also added a function to instanciate the different classes from a dict (useful with JSON data). This function checks if the key is a column to prevent overwriting methods of the class with string (for example).

__repr__ functions are defined to correctly log event related to the tables.

At last, a function to compute the score of each resource based on the initial score of 1 and the subsequent upvotes and downvotes through the reactions.
Reaction normally update the score of the resource they are related to.
But the idea is to prevent inconsistencies if two simultaneous calls try to update a record (not possible as Flask would not allow to concurrent calls anyway but added for the sake of rigor).
Practically this would be triggered by a cron job or something similar.
#### Routes definition 
I defined the different routes and their methods.
New feedbacks and comments use a POST call.
Reaction to feedbacks or comments use a PUT call.
