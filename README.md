# weather_bot
A weather bot that runs on Line platform.
This document will show you how to set up the environment for my weather bot.

Create line bot account
------------------------------
1.First, go to this webpage https://business.line.me/en/services/bot and click "Start using Messaging API" to create an account for the weather bot.  
2.After finishing the account settings, click the "Accounts" tab above and go to LINE@ MANAGER of the account you just created.  
3.On the left side of the page, just right below the bot name is the id of the bot, which begins with an "@".
  You can friend the account using this id. But be aware that there is a limit of 50 for the number of friends that the bot can have.  
4.Go to Settings -> Bot Settings to enable API.  
5.Change the setting of Use webhooks from don't allow to allow.  
6.Go back to the "Accounts" tab, you can see that there is a messaging API, click LINE Developers to get your channel id, channel secret and channel access token for later use. You can also see the QR code of the account.

Django the web framework
--------------------------------
For python, simply just 
pip3 install line-bot-sdk
There are also other versions for java, go, ruby, php and perl.

#Create a project
django-admin startproject projectName
My project name is line_echobot

#Create an app
python3 manage.py startapp appName
My app name is echobot


Heroku the web server
-------------------------------
1.Go to https://www.heroku.com/ and create an account.  
2.Go to your dashboard, click New -> Create New APP to create an app.  
3.Install Heroku CLI
  If you are using Debian or Ubuntu, type the following commands
  sudo add-apt-repository "deb https://cli-assets.heroku.com/branches/stable/apt ./"
  curl -L https://cli-assets.heroku.com/apt/release.key | sudo apt-key add -
  sudo apt-get update
  sudo apt-get install heroku
  For other operating systems, check https://devcenter.heroku.com/articles/heroku-cli for more informations.  
4.In line_echobot directory, type
  heroku login
  heroku git:remote -a herokuAppName
  
In line_echobot/settings.py, I don't want my django secret key, line channel access token and line channel secret to reveal to the public on github, so I added them to the environment variables by
clicking Settings -> Config Variables -> Reveal Config Vars on the dashboard to set the variable name and value.

In Procfile, 
web: gunicorn line_echobot.wsgi --log-file -
remember to change line_echobot to your Django project name.

After all things done, type
git push heroku master 
to push your project to Heroku.

------------------------------------------
And then go back to LINE Developers of your bot, set the webhook url to
the web page of the project you just push but add /echobot/callback/ in the end.
(echobot is my heroku app name)
------------------------------------------
For usage, enter any sentence including "天氣" and any counties in Taiwan in Chinese.
And the weather bot will response to you the weather with the corresponding counties.
If the sentence you entered did not contain any counties in Taiwan but including "天氣", then the weather bot will tell you the weather of Tainan(in Chinese).
If you enter any other text messages, the weather bot simply just echos what you typed.
You can chat with the weather bot now!
If you just want to experience the function of the bot, my weather bot id is @mpj7236c, welcome to friend me! 

