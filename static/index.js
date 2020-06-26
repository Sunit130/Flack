document.addEventListener('DOMContentLoaded', ()=>{
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on("connect",()=>{
        document.getElementById('create_channel').onclick = ()=>{
            var channel_name = document.getElementById('channel_name').value;
            document.getElementById('channel_name').value = "";
             socket.emit("create channel", {"channel_name":channel_name});
        };

        document.getElementById('send_message').onclick = ()=>{
            var message = document.getElementById('message').value;
            document.getElementById('message').value = "";
            socket.emit("send message", {"message":message});
        };


    });

    socket.on("announce channel", data=>{
        var channel_name = data.channel_name;
        const li = document.createElement("li");
        const a  = document.createElement("a");
        a.innerHTML = channel_name;
        a.href = `/channel/${channel_name}`;
        li.appendChild(a);
        document.getElementById("channels").append(li);
    });



});
