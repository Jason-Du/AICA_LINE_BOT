from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello ATCA!!'    #回傳字串，讓使用看到

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)