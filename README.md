# IMPORTANT - READ ME BEFORE USING THIS CODE

- Basic web server written in python using the flask framework, 
 This web server contains a home page, login page, signup page and a user dashboard and interacts with a MySQL database
 whilst using best practises to prevent possible security vulnerabilities such as SQL injection, XSS, session fixation and much more.

- This is meant to be used as a template to build complete web applications by already implementing best practises to prevent security vulnerabilities 

- feel free to implement any new features! Just make a pull request and I will take a look at the code, if it is to a high standard it will be accepted,
  also let me know if theres any ways which I can improve my code to make it more efficient, im always looking for ways to imrpove!
  
to install flask, run pip3 install flask on your terminal

for this project I used; Python (with Flask), SQL (with MySQL), HTML, CSS, and Javascript

IMPORTANT

- This program assumes you are using a MySQL database, if you are not then make changes to the code accordingly.
  This program also assumes the database contains the columns; 'passwords', 'usernames', and 'recovery_keys' and assumes
  that the 'passwords' column and 'recovery_keys' columns are case sensitive and the usernames column is case insensitive
    
- This code works best in a python 3.11 environment
