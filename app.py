from flask import Flask, session, render_template, redirect, request
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "THISISECRETKEY"

socketio = SocketIO(app, manage_session=True)

#all channel information is stored in this dict
channels = {}


# Initial route
@app.route("/")
def index():
    if 'username' in session:
        return render_template("index.html",channels=channels.keys())
    else:
        return redirect("/login")

    
#Login route
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        session["username"] = username
        return redirect("/")
    else:
        if 'username' in session:
            return "Already Login"
        else:
            return render_template("login.html")

        
# Logout route
@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop("username", None)
        return redirect("/login")
    else:
        return "Already Logout"

    
    
# Channel route
@app.route("/channel/<channel>")
def active_channel(channel):
    session["active_channel"] = channel
    return render_template("channel.html", messages=channels[channel], channels=channels.keys() )



# This is POST route, used to get all information of current channel
@app.route("/get_current_channel_info", methods=["POST"])
def get_current_channel_info():
    return {"current_channel":session["active_channel"], "username":session["username"], "messages":channels[session["active_channel"]]}



# This is socketio event "delete message" triggers when any user delete any of their messages
@socketio.on("delete message")
def delete_message(data):
    
    message_info= ""
    #find the message which nedded to be deleted from active_channel
    for e in channels[session["active_channel"]]:
        
        username =e["username"]
        time = e["time"]
        message = e["message"]
        
        message_info = f"{username} ({time}) : {message}"
        if(message_info == data["message_info"]):
            channels[session["active_channel"]].remove(e)
            break
 
    emit("announce delete message", {"channel_name":session["active_channel"], "messages":channels[session["active_channel"]]}, broadcast=True)

    
    
# This is socketio event "send message" triggers when any user send a message on a channel
@socketio.on("send message")
def send_message(data):
    
    message = data["message"]
    username = session["username"]
    
    x = datetime.datetime.now()
    
    message_info = {"username":username, "time":x.strftime("%X") , "message":message}
    channels[session["active_channel"]].append(message_info)
    
    total_messages = len(channels[session["active_channel"]])
    if(total_messages>100):
        channels[session["active_channel"]] = channels[session["active_channel"]][total_messages-100:total_messages]

    emit("announce message", {"channel_name":session["active_channel"], "message":message_info}, broadcast=True)

    

# This is socketio event "create channel" triggers when any user creates a new channel
@socketio.on("create channel")
def create_channel(data):
    
    channel_name = data["channel_name"]
    if channel_name in channels:
        return
    
    channels[channel_name] = []
    emit("announce channel", {"channel_name":channel_name}, broadcast=True)
