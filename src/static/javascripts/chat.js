var channel = "/chat";

// start socket io connection to server
var socket = io.connect('http://' + document.domain + ':' + location.port + channel);

socket.on("connect", function() {
    socket.emit('joined', {});
    socket.emit('loadUp', {});
});

// on new message
socket.on("message", function (message) {
    loadMessage(message);
});

// on new status (user left/joined)
socket.on("status", function(message) {
    loadStatus(message);
});

// on previous messages
socket.on("previous", function(messages) {
    addMesssages(messages);
});

// load new message to messages
function loadMessage(message) {
    $(".chat").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'
        + message.data.message + '<br/><small class="text-muted">' + message.data.author + ' | '
        + message.data.timestamp + '</small><hr/></div></div></div></li>');

     $(".fixed").animate({scrollTop: $('.fixed').prop("scrollHeight")}, 500);
}

// load new status to messages
function loadStatus(message) {
    $(".chat").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body">'
        + '<br/><small class="text-muted">' + message.data.message + ' | ' + message.data.timestamp +
        '</small><hr/></div></div></div></li>');

    $(".fixed").animate({scrollTop: $('.fixed').prop("scrollHeight")}, 500);
}

// add previous messages to chat
function addMesssages(messages) {

    messages = messages.data;

    for (let i = messages.count - 1; i>=0; i--) {

        let message = messages.messages[i];

        var newElement = '<li class="media"><div class="media-body"><div class="media"><div class="media-body">'
            + message.message + '<br/><small class="text-muted">' + message.author + ' | '
            + message.timestamp + '</small><hr/></div></div></div></li>';

        $(".chat").prepend(newElement);
    }

    // scrolls to top of messages
    $(".fixed").animate({scrollTop: $('.chat li:first-child').position().top}, 500);
}

// jquery init
$(function(){

    // register on clicks and key functions
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

    $('#loadUp').on("click", function() {
        loadUp()
    })

    // send new message to server via sockets on send clicked
    function send() {
        $container = $(".chat");
        $container[0].scrollTop = $container[0].scrollHeight;
        var message = $("#message").val();
        socket.emit("message", {data: {message: message}});
        $("#message").val("");
    }

    // send out user and disconnect socket, redirects to logout
    function signOut() {
        socket.emit("left", {}, function(){
            window.location = "/logout";
            socket.disconnect();
        });
    }

    // load previous messages
    function loadUp() {
        socket.emit("loadUp", {});
    }
})
