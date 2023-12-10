from flask import Flask, redirect, url_for

app = Flask(__name__) # assign webpage to 'app'

# frontend
@app.route('/') # first page available on the site
def frontpage():
    
    # render HTML on the page
    return '''    
<html>
<style> 
    html {
    background-color: blue; width: 100%; height: 100%;
    text-align: center; color: white; font-family: sans-serif; font-size: 20px; 
    }
</style>
    
    <!DOCTYPE html>
<html>
    <head>
        <title> First web server </title>
        <h1> <br> <u> This is my first web server </u> </h1>
    </head>

    <body>
        <header>
            <p1> <b> Come back later! </b> </p1>
        </header>

        <main>
            <img src="https://th.bing.com/th/id/OIP.vyeL1KIJpbGdWaeHh5HfDAHaEq?w=288&h=181&c=7&r=0&o=5&dpr=2&pid=1.7" 
            width:"300" height:"350">
        </main>

        <footer>
            <script src="https://tryhackme.com/badge/2315259"> </script>
        </footer>
    </body>
</html>
'''

@app.route('/home') # /home redirects to front page
def home():
    return redirect(url_for('frontpage'))

# initiate the webpage
if __name__ == '__main__': 
    app.run()
