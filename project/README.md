# CS50 Final Project - FlashWord

## URL:https://youtu.be/4Ojn8qqiCGg

Game of quick lateral and associative thinking.

You get a word of the day and questions whose answers need to contain what the word of the day sounds like. This game was born out of a game I really like to play.

The premise is simple, there are questions and you need to answer the questions. However the catch comes in where the answer needs to contain the sound for the word of the day.

Technologies used:
- Python
- Flask
- sqlite3
- HTML
- Werkzeug
- other small libraries or packages

## How the webpage works?

You get a word of the day and questions whose answers need to contain what the word of the day sounds like. This game was born out of a game I really like to play.

The premise is simple, there are questions and you need to answer the questions. However the catch comes in where the answer needs to contain the sound for the word of the day.

You land on the homepage and it shows you what the FlashWord of the day is. It also presents the user with an example. From this page the user can decide to play or view their history

On the Play page the user is presented with the FlashWord of the day again, as well as an example. Added now there is the questions based on the FlashWord of the day

### Routing

There are only two routes for the game. The index route. The second route is for the game section of the app

### Example:
Sounds like: OAR
Words that sound like OAR. This can be phonetic, spelt the same, sound the same. But must contain the sound OAR.
Example question: Something you do in a game of soccer to earn points.
Answer: SCORE

### Sessions

I must still implement a session that is stored on the users machine. This is going to be used to track the users stats and present a graph of best score, worst score, fastest time etc.

### Database

Database stores the FlashWord and its associated questions and answers. I am using SQLite3 to implement the db

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- Serve to homepage is too chatty. I must find a way to reduce this
- Functionality needs to be embedded on the page instead of in the controller
- I must still complete the My History portion of the game
- Will need to create and store a session on the users device
- It needs the functionality to move to the next word of the day

## How to launch application

1. Check that you have necessary libraries installed
1.1 This is shown inthe  section above
2. Clone the code:
3. Run flask run
4. In your browser go to `localhost:50000`
6. You are ready to go!
