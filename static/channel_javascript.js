document.addEventListener('DOMContentLoaded', ()=>{

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    socket.on("connect",()=>{
        // Send channel name to server
        document.getElementById('create_channel').onclick = ()=>{
            var channel_name = document.getElementById('channel_name').value;
            document.getElementById('channel_name').value = "";
             socket.emit("create channel", {"channel_name":channel_name});
        };

        // Send new message by user to server
        document.getElementById('send_message').onclick = ()=>{
            var message = document.getElementById('message').value;
            document.getElementById('message').value = "";
            socket.emit("send message", {"message":message});
        };


    });


    // Announce new channel which is created
    socket.on("announce channel", data=>{

        var channel_name = data.channel_name;
        const li = document.createElement("li");
        const a  = document.createElement("a");
        a.innerHTML = channel_name;
        a.href = `/channel/${channel_name}`;
        li.appendChild(a);
        // li is created in which new channel hyperlink is stored
        document.getElementById("channels").append(li);
    });


    // Delete the message if deleted by sender
    socket.on("announce delete message", data=>{
        const request = new XMLHttpRequest;
        //get all the information about current channel
        request.open("POST", '/get_current_channel_info');
        request.onload = ()=>{
            const response = JSON.parse(request.responseText);
            if(response.current_channel == data.channel_name){
                var messages = response.messages;
                var ul = document.getElementById("messages");
                ul.innerHTML="";
                for(message of messages){
                    const li = document.createElement("li");
                    const div = document.createElement("div");
                    const del = document.createElement("button");

                    div.innerHTML = `<p>${message["username"]} (${message["time"]}) : ${message["message"]}</p>`;
                    div.className ="message_info";
                    del.className = "delete";
                    del.innerHTML = "delete";

                    // Add delete button only if current user had send that message
                    del.onclick = ()=>{
                        socket.emit("delete message", {"message_info":del.parentElement.firstElementChild.innerHTML});
                    };

                    if(response.username == message["username"]){
                        div.appendChild(del);
                    }
                    li.appendChild(div);
                    document.getElementById("messages").append(li);
                }

            }
        };
        request.send();

    });


    // Announce new message send by any user
    socket.on("announce message", data=>{
        const request = new XMLHttpRequest;
        request.open("POST", '/get_current_channel_info');
        request.onload = ()=>{
            const response = JSON.parse(request.responseText);
            if(response.current_channel == data.channel_name){

                var username = data.message.username;
                var time = data.message.time;
                var message = data.message.message;

                const li = document.createElement("li");
                const div = document.createElement("div");
                const del = document.createElement("button");

                div.innerHTML = `<p>${username} (${time}) : ${message}</p>`;
                div.className ="message_info";
                del.className = "delete";
                del.innerHTML = "delete";
                del.onclick = ()=>{
                    socket.emit("delete message", {"message_info":del.parentElement.firstElementChild.innerHTML});
                };

                if(response.username == username){
                    div.appendChild(del);
                }
                li.appendChild(div);
                document.getElementById("messages").append(li);


                var objDiv = document.getElementsByClassName("all_messages")[0];
                objDiv.scrollTop = objDiv.scrollHeight;
            }
        };
        request.send();


    });


    // After DOM is loaded fill message section with messages
    const request = new XMLHttpRequest;
    request.open("POST", '/get_current_channel_info');
    request.onload = ()=>{
        const response = JSON.parse(request.responseText);
        document.getElementsByClassName("current_channel")[0].innerHTML = response.current_channel;
        var messages = response.messages;
        var ul = document.getElementById("messages");
        for(message of messages){
            const li = document.createElement("li");
            const div = document.createElement("div");
            const del = document.createElement("button");

            div.innerHTML = `<p>${message["username"]} (${message["time"]}) : ${message["message"]}</p>`;
            div.className ="message_info";
            del.className = "delete";
            del.innerHTML = "delete";
            del.onclick = ()=>{
                socket.emit("delete message", {"message_info":del.parentElement.firstElementChild.innerHTML});
            };

            if(response.username == message["username"]){
                div.appendChild(del);
            }
            li.appendChild(div);
            document.getElementById("messages").append(li);
        }
        var objDiv = document.getElementsByClassName("all_messages")[0];
        objDiv.scrollTop = objDiv.scrollHeight;

    };
    request.send();


});
