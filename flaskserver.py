from flask import Flask, redirect, url_for

app = Flask(__name__) # assign webpage to 'app'

# frontend
@app.route('/') # first page available on the site
def frontpage():
    
    # render HTML on the page
    return ''' 
<html>

<div style="
    text-align: center;
    background-color: blue;
    color: white;
    width: 100%;
    height: 100%;
    ">

    <head>
        <title> First web server </title>
        <h1> <u> First web server </u> </h1>
        <p1> Hey! <br> This is my first web server </p1>
    </head>

    <body>
        <header>
            <h1> <b> Come back later! </b> </h1>
        </header>

        <main>
            <img src="https://th.bing.com/th/id/OIP.vyeL1KIJpbGdWaeHh5HfDAHaEq?w=270&h=180&c=7&r=0&o=5&dpr=2&pid=1.7" 
                 width="400" height="300">
        </main>
    </body>
</div>
'''

@app.route('/home') # /home redirects to front page
def home():
    return redirect(url_for('frontpage'))

# initiate the webpage
if __name__ == '__main__': 
    app.run()
