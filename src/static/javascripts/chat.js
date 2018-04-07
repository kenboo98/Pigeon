var channel = "/chat";

var socket = io.connect('http://' + document.domain + ':' + location.port + channel);

socket.on("connect", function() {
    socket.emit('joined', {});
});

socket.on("message", function (message) {
    loadMessage(message);
});

socket.on("status", function(message) {
    loadStatus(message);
});

function loadMessage(message) {
    $(".chat").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'
        + message.data.message + '<br/><small class="text-muted">' + message.data.author + ' | '
        + message.data.timestamp + '</small><hr/></div></div></div></li>');
}

function loadStatus(message) {
    $(".chat").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'
        + '<br/><small class="text-muted">' + message.data.message + ' | ' + message.data.timestamp +
        '</small><hr/></div></div></div></li>');
}

$(function(){

    $("#send").on("click", function() {
        send()
    });

    $("#message").keyup(function(e) {
        if (e.keyCode == 13) {
            send();
        }
    });

    $("#signOut").on("click", function() {
        signOut();
    });

    function send() {
        $container = $(".chat");
        $container[0].scrollTop = $container[0].scrollHeight;
        var message = $("#message").val();
        socket.emit("message", {data: {message: message}});
        $("#message").val("");
        $container.animate({ scrollTop: $container[0].scrollHeight }, "slow");
    }

    function signOut() {
        socket.emit("left", {}, function(){
            socket.disconnect();
            window.location = "/";
        })
    }
})
