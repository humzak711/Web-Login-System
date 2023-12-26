# IMPORTANT - READ ME BEFORE USING THIS CODE
- Basic web server written in python using the flask framework, 
 This web server contains a home page, sign up page and a login page which interact with a MySQL database
 whilst maintaining a high level of security to prevent possible security vulnerabilities such as SQL injection, XSS and much more.

- This is meant to be used as a template to build complete web servers by already having a secure login and sign-up page which prevent;
 Security vulnerabilities, users having the same username or email associated with their stored credentials, and users having weak credentials

- feel free to implement any new features! Just make a pull request and I will take a look at the code, if it is to a high standard it will be accepted,
  also let me know if theres any ways which I can improve my code to make it more efficient, im always looking for ways to imrpove!
  
to install flask, run pip3 install flask on your terminal

IMPORTANT

- change all instances of 'your localhost' on the html templates to your localhost,
  e.g. if your localhost runs on port 1111, change all occorrunces of 'http://your localhost' to 'http://127.0.0.1:1111'
  and keep the same url extension, e.g change 'http://your localhost/login' to 'http://127.0.0.1:1111/login'
  This is crucial for the web server to be able to run properly and for the url redirects to work,
  the default localhost + port for flask is 127.0.0.1:5000

- This program assumes you are using a MySQL database, if you are not then make changes to the code accordingly.
  This program also assumes the database contains the columns; 'passwords', 'usernames', and 'emails' and assumes
  that the 'passwords' column is case sensitive whereas both the 'usernames' and 'emails' columns are case insensitive
  
- This code works best in a python 3.11 environment
