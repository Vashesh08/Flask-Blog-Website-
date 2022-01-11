from flask import Flask, request, render_template, make_response
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/blog")
def hello_blig():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset='utf-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<title>Vashesh Jogani - Profile</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<meta name="google-site-verification" content="ui3ziIfkZgD055_MLteNjq71xKFPdXf5V3GK2SB9jS0" />
<meta name="keywords" content="Vashesh, Jogani, web developer, full stack web developer, thadomal, shahani, engineer, Mumbai"/>
<meta name="description" content="Vashesh Jogani, web developer, full stack web developer, thadomal shahani engineering college, tsec, engineer, Mumbai" />
<meta name="author" content="Vashesh Jogani" />
<meta property="og:title" content="Vashesh Jogani" />
<meta property="og:type" content="website" />
<meta property="og:description" content="Full Stack Web Developer" />
<link rel='stylesheet' type='text/css' media='screen' href='main.css'>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<script src='main.js'></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<style>
.green-color {
    color:green;
}
</style>
</head>
<body>
<h1>Vashesh Jogani</h1>
<span class="material-icons">
search
</span>
<div>
<a href="mailto:vashesh2001@gmail.com" target="_blank" rel="noopener noreferrer"><img src="https://raw.githubusercontent.com/Vashesh08/Vashesh08/main/Gmail.png" alt="Gmail@vashesh-jogani" style="height:20px;" title="Gmail"></a>
<a href="tel:+917678066555" target="_blank" rel="noopener noreferrer"><i class='fa fa-phone green-color'></i></a>
<a href="https://wa.me/917678066555" target="_blank" rel="noopener noreferrer" hreflang="en"><img src="https://raw.githubusercontent.com/Vashesh08/Vashesh08/930313f0ef2b7126a31cd3791b596122ebf8b3fb/whatsapp.svg" alt="Whatsapp@vashesh-jogani" style="height:20px;" title="Whatsapp"></a>
</div>
</body>
</html>"""


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/login')
def login(name=None):
    return render_template('ab.html', name=name)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/parent')
def parent():
    return render_template('parent.html')


if __name__ == "__main__":
    app.run(debug=True)
