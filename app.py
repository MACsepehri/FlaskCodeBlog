from flask import Flask, render_template, render_template_string, redirect, request, session
import json

app = Flask(__name__)
app.secret_key = "ridam be internet / interanet / filternet"

@app.route("/", methods=["GET", "POST"])
def index():
    method = request.method
    if method == "GET":
        if not session:
            session["username"] = "Anonymous User"
            session["is_new"] = "true"
        return render_template("index.html", session=session, message=json.load(open("static/message/message.json", "r"))["message"])
    else:
        with open("static/user/user.json", "r") as file:
            data = json.load(file)
            for user in data["users"]:
                if user["username"] == request.form.get("username") or user["password"] == request.form.get("password"):
                    if user["username"] == request.form.get("username") and user["password"] == request.form.get("password"):
                        session["username"] = request.form.get("username")
                        session["password"] = request.form.get("password")
                        session["is_new"] = "false"
                        return redirect("/")
                    else:
                        return redirect("/error-of-login")
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        session["is_new"] = "false"
        data["users"].append({"username":request.form.get("username"), "password":request.form.get("password")})
        json.dump(data, open("static/user/user.json", "w"))
        return redirect("/")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/send-message", methods=["POST"])
def send_message():
    method = request.method
    if method == "POST":
        user_mesasge = request.form.get("message")
        with open("static/message/message.json", "r") as file:
            data = json.load(file)
            data["message"].append({"msg" : f"{session['username']} :\n{user_mesasge}"})
            json.dump(data, open("static/message/message.json", "w"))
            return redirect("/")
        
@app.route("/dashboard")
def dashboard():
    return "درحال ساخت"

@app.route("/contact")
def contact_us():
    return "درحال ساخت"

@app.route("/about-us")
def about_us():
    return "درحال ساخت"

@app.route("/error-of-login")
def error_of_login():
    return render_template_string("""<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فروم برنامه نویسی</title>

    <style>
        @font-face {
            font-family: vazirmatn;
            src: url("/static/font/Vazirmatn-Black.woff2");
        }

        * {
            font-family: vazirmatn;
            color: white;
        }

        body {
            background-color: #121212;
            overflow-x: hidden;
        }

        a {
            text-decoration: none;
            color: #9a9a9a;
        }

        input,
        textarea {
            background: #212121;
        }

        .message-box {
            width: 350px;
            height: 150px;
            resize: none;
        }

        .messages {
            transform: translateY(-240px);
        }

        .links {
            transform: translateY(-60px);
            margin-right: 300px;
        }

        .contants {
            padding-right: 20px;
            padding-top: 5px;
        }

        .header {
            width: 80%;
            height: 100px;
            border-radius: 10px;
            background: #212121;
        }

        .login-form {
            transform: translateX(-1030px);
            margin-top: -80px;
        }

        @media (max-width: 480px) {
            .messages {
                transform: translateY(0px);
            }

            .header {
                width: 80%;
                height: 100px;
                border-radius: 10px;
                background: #212121;
                transform: translateY(-130px);
                margin-right: 200px;
            }
        }
    </style>
</head>

<body>

    <h1>اکانتی با همچین اطلاعاتی وجود دارد.</h1>
</body>

</html>""")
    
app.run(debug=True)