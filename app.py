from flask import Flask, session, render_template, redirect, request
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "THISISECRETKEY"

socketio = SocketIO(app, manage_session=True)

channels = {}

@app.route("/")
def index():
    print("index : ",session)
    # for i in range (35):
    #     channels[i]=[]
    if 'username' in session:
        # if 'active_channel' in session:
        #     active_channel = session["active_channel"]
        #     return redirect(f"/channel/{active_channel}")
        return render_template("index.html",channels=channels.keys())
    else:
        return redirect("/login")

@app.route("/login", methods=["POST", "GET"])
def login():
    print("login : ",session)
    if request.method == "POST":
        username = request.form.get("name")
        session["username"] = username
        return redirect("/")
    else:
        if 'username' in session:
            return "Already Login"
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    print("logout : ",session)
    if 'username' in session:
        sesssion.pop("username", None)
        return redirect("/login")
    else:
        return "Already Logout"

@app.route("/channel/<channel>")
def active_channel(channel):
    session["active_channel"] = channel
    return render_template("temp.html", messages=channels[channel], channels=channels.keys() )

@app.route("/get_current_channel", methods=["POST"])
def get_current_channel():
    print("get_current_channel ",session["active_channel"])
    return {"current_channel":session["active_channel"]}

@socketio.on("send message")
def send_message(data):
    message = data["message"]
    username = session["username"]
    x = datetime.datetime.now()
    channels[session["active_channel"]].append(f"{username} ({x.hour}:{x.minute}): {message}")
    channels[session["active_channel"]].append([{"username":username}, {"time":x} , {"message":message}])
    total_messages = len(channels[session["active_channel"]])
    if(total_messages>100):
        channels[session["active_channel"]] = channels[session["active_channel"]][total_messages-100:total_messages]
    print("session.get(username) ",session.get("username"), " total_messages ",total_messages, "channels[session[active_channel]] ",channels[session["active_channel"]])
    emit("announce message", {"channel_name":session["active_channel"], "message":f"{username} ({x.hour}:{x.minute}): {message}"}, broadcast=True)


@socketio.on("create channel")
def create_channel(data):
    print("create channel : ",session)
    channel_name = data["channel_name"]
    if channel_name in channels:
        return
    channels[channel_name] = []
    # for i in range (35):
    #     channels[channel_name].append(f"message {i} {channel_name}")
    emit("announce channel", {"channel_name":channel_name}, broadcast=True)
