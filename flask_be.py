from flask import Flask

app = Flask(__name__, static_folder='app')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")

@app.route('/name')
def name():
    return {'Name': "Stephanie"}


if __name__ == '__main__':
    app.run(debug=True)