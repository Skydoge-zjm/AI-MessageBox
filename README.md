# Welcome to our AI Message Box for XDUer!
## Introduction

This is a website service of a AI assistant to help you summarize your campus news and messages. However, the AI model is **NOT** in the repo. If you want to have a full experience, you can deploy the open souce model **ChatGLM3-6B** and replace the empty file in the folder **model**. You should also change the path of the model in the file **app.py**.
## Framework

We use the **selenium** framework to help us build our reptile. So that we have an access to news and messages(Users should login in advance.)   
Mysql is used to store the data. And the data will be output from the database in chronological order to become a list in python.
We use **Flask** framework to construct a website for the users.
## We hope you will give us a hand!