email_service
=============

A Python library to send emails by accepting JSON data through HTTP POST requests.

Installation Instructions
=========================

1. Install Git

  * Linux
  
    ```bash
     $ sudo apt-get install git-core
    ```

  * Windows
  
    [Click here](http://git-scm.com/book/en/Getting-Started-Installing-Git#Installing-on-Windows) for instructions on installing Git for Windows

2. Install virtualenv and pip

  * Linux
  
    ```bash
     $ sudo apt-get install python-setuptools
     $ sudo easy_install virtualenv
    ```

  * Windows
  
    [Click here](http://arunrocks.com/guide-to-install-python-or-pip-on-windows/) for instructions on installing virtualenv and pip for Windows

3. Create a directory for your projects (replace {PROJECT_HOME} with your desired directory path and name: for instance /email_service or /home/{username}/email_service)

    ```bash
     $ mkdir /{PROJECT_HOME}
     $ cd /{PROJECT_HOME}
    ```
    
4. Pull down the project from github

  * Linux
    
    ```bash
     $ git clone https://github.com/darshanrp/email_service.git
    ```

  * Windows (use Git Bash)
    
    ```bash
     $ cd /{PROJECT_HOME}
     $ git clone https://github.com/darshanrp/email_service.git
    ```
    
5. Create virtual Python environment for the project

  * Linux and Windows(use Powershell or Command Prompt)
    
    ```bash
     $ cd /{PROJECT_HOME}/email_service
     $ virtualenv ENV
    ```
    
6. Activate your virtual environment

  * Linux
    
    ```bash
     $ source ENV/bin/activate
    ```

  * Windows
    
    ```bash
     $ cd ENV/Scripts
     $ activate
     $ cd /{PROJECT_HOME}/email_service
    ```

7. Install dependencies

  * Linux and Windows(use Powershell or Command Prompt)
    
    ```bash
     (ENV)$ pip install -r requirements.txt
    ```

8. Update values in settings.py file

  * Replace `{MAILGUN_DOMAIN}` with the appropriate mailgun domain for Mailgun account
  * Update `API_KEY` with Mailgun api key for your account
  * Update `ALT_API_KEY` with Mandrill api key for your account
  * Update `SERVER_PORT` with appropriate port number
  * Update `TIMEZONE` (Eg. 'US/Pacific' or 'US/Eastern')

9. Start webservice

  * Linux and Windows(use Powershell or Command Prompt)
    
    ```bash
     (ENV)$ python email_service.py
    ```


Usage Instructions
==================
In order to make a HTTP POST request to the webservice you can use the following curl command

  ```bash
   $ curl -i -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"to":"darshan@gwu.edu","to_name":"Darshan Pandhi","from":"noreply@uber.com","from_name":"Uber","subject":"Test message from Uber","body":"Your bill is $10."}' http://localhost:8081/email
  ```

  * Delayed email delivery

    For delayed email delivery add the param 'send_at'
 
    ```bash
    $ curl -i -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"to":"darshan@gwu.edu","to_name":"Darshan Pandhi","from":"noreply@uber.com","from_name":"Uber","subject":"Test message from Uber","body":"Your bill is $10.","send_at":"2014-06-30 10:45:00"}' http://localhost:8081/email
    ```
    
Note: To use curl on Windows, use curl command in git bash or follow installation instructions [here](http://d4dilip.wordpress.com/2013/01/11/setup-curl-on-windows-7-64-bit/)

  
Language and Framework details
==============================
I started reading about Flask framework and I found it nimble and a perfect fit for such small applications. It has a handful of useful modules for building a standalone app. Flask is small yet powerful framwork based on Werkzeug and Jinja2. Flask immediately caught my interest and I wanted to learn and use it. Hence I chose Python and Flask for this task.

