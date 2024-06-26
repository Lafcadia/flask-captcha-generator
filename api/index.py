from captcha.image import ImageCaptcha
from flask import Flask, render_template, request
import string
import random
import base64
import io

app = Flask(__name__)

def generator(name="code.png"):
    token = string.digits + string.ascii_letters
    cap = random.sample(token,8)
    token_str = ''.join(cap)
    img = ImageCaptcha(width=400,height=150)
    image = img.generate_image(token_str)
    image.save(name)
    return token_str

@app.route('/', methods=['GET','POST'])
def index():
    global real_str
    if request.method == 'POST':
        result = request.form
        r = result.get('yanzheng').lower() == real_str.lower()
        if r:
            return "1"
        else:
            return "0"
    else:
        return render_template('index.html', img_stream=streamer())

@app.route('/code.png')
def view():
    return streamer()

def streamer():
    global real_str
    token = string.digits + string.ascii_letters
    cap = random.sample(token,4)
    token_str = ''.join(cap)
    img = ImageCaptcha(width=400,height=100)
    image = img.generate_image(token_str)
    b = io.BytesIO()
    image.save(b, format="JPEG")
    real_str = token_str
    return base64.b64encode(b.getvalue()).decode()

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='2333')