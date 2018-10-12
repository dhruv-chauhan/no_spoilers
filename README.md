No Spoilers !
=============

## A python script to save the community from all the spoilers of their favourite tv series hovering around.

___
## Input : 
> The [script](https://github.com/dhruv-chauhan/no_spoilers/blob/master/no_spoilers.py) requires email address and list of favourite TV series for multiple users as input.

> Store the input data in MySQLdb table(s).

## Output :
> An email is sent to the input email address with all the appropriate response for every TV series.
___
## Development Environment :
```
git clone https://github.com/dhruv-chauhan/no_spoilers.git  //Clone the repository
make all                                                    //sets up the development environment
./run.sh                                                    //launches the script
```
```
make clean                                                  //deletes the installed dependencies
```
___
# Demo :
1. After setting up development environment, launch the script `./run.sh` to get a prompt asking for Email Address and a list of TV Series : 

![alt text]( "Input Demo")

2. The given input is stored as MYSQLdb table :

3. A template, which is generated using [API](https://www.tvmaze.com/api) to fetch all required information about the TV Series, is sent in the email given Email Addresses as :

  + Before and after the script is run :
  
  ![alt_text]( "Before Script Demo")
  
  ![alt_text]( "Inbox Demo")
  
  + Template :
  Tv series name:
    - Link to the Series' IMDB page.
  Format for Status :
    - Exact date is mentioned for next episode.
    - Only year is mentioned for next season.
    - All the seasons are finished and no further details are available.
  
  ![alt_text]( "Template Demo")
  
  + For Shows with exact date mentioned for next episode, there appears a link, using which the user can schedule the episode airing to their Google Calendar (with exact airing date and time, considering time zones).
  
  ![alt_text]( "Calendar Demo")

____
## Assumptions :

1. Usage of API doesn't ensure availibility of all the data, but it solves our purpose quite well; and it's well faster than webscraping.

2. For demo, use any of the following dummy email id's created for this project :

>ID : nospoilers.demo@gmail.com

>PASS : N0sp0ilers

>ID : nospoilers.demo1@gmail.com

>PASS : N0sp0ilers

>ID : nospoilers.demo2@gmail.com

>PASS : N0sp0ilers

This is because Google recommend turning access OFF for unrecognised apps, OR, if you wish to use some other gmail ID, go to this [link](https://myaccount.google.com/lesssecureapps) and turn "Allow less secure apps:" ON.

3. Sender's email address is set as :

>ID : nospoilers.demo@gmail.com

>PASS : N0sp0ilers

It can be changed through the script variables.
