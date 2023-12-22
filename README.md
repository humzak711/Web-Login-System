# WebServer
basic web server written in python using the flask framework

to install flask, run pip3 install flask on your terminal

IMPORTANT
- change all instances of 'your localhost' on the html templates to your localhost,
  e.g. if your localhost runs on port 1111, change all occorrunces of 'http://your localhost' to 'http://127.0.0.1:1111'
  and keep the same url extension, e.g change 'http://your localhost/login' to 'http://127.0.0.1:1111/login'
  This is crucial for the web server to be able to run properly and for the url redirects to work

- This program assumes you are using a MySQL database, if you are not then make changes to the code accordingly

- This code works best in a python 3.11 environment
