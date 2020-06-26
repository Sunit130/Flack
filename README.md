# Flack
Flack is chatting app created using Flask in which the user just needs to login with their username and can chat on any channel which is created on the server. This application uses Flask-SocketIO which gives Flask applications access to low latency bi-directional communications between the clients and the server. In this applicaion user can view messages already sent on that channel, can send his own message and can delete any message sent by him.

### Login
This page asks username which is used with the message sent by the user. This page is loaded if the user ever logs out.
![alt text](https://github.com/Sunit130/Flack/blob/master/demo/Screenshot%20(66).png)

### Home Page
This images shows the home screen of two users, with username "User1" and "User2" respectively. "Available channel" shows all the channels created since the server was started.
![alt text](https://github.com/Sunit130/Flack/blob/master/demo/Screenshot%20(67).png)

### Channel Created
When any of the users creates/adds a channel then that channel is announced to all the users in "Available channel" section. This channel will exist even if the user logout. The top of the message window shows the selected channel.
![alt text](https://github.com/Sunit130/Flack/blob/master/demo/Screenshot%20(68).png)

### Messaging
A message shows the username with which the user login, time when the message was sent, and the message. Messages are sent instantly means there is no need to refresh the page just to view the new messages. Users can chat in any channel, all the messages are kept separately in their respective channel.
![alt text](https://github.com/Sunit130/Flack/blob/master/demo/Screenshot%20(69).png)

### Deleting a message
Messages can be only deleted by its true user. The process of deletion is also instantaneous.
This image shows what happens when "User1" delets "Message3".
![alt text](https://github.com/Sunit130/Flack/blob/master/demo/Screenshot%20(70).png)




