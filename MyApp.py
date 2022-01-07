from flask import Flask

app=Flask(__name__)

@app.route('/')
def homepage():
    return "First time using Flask, Woohooo~"

if __name__ == '__main__':
    app.run(debug=True)