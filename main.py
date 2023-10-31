from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def home_test():
    return "<p>hi</p>"

if __name__ == '__main__':
    app.run()