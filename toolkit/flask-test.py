from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    html = 'HERE CAN BE PHISHING PAGE FOR  {}'.format(request.base_url)
    return html


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)