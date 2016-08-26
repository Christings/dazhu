$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chatbox")
        var ele = '<article>'+
        		'<p> '+data.handle+' '+data.timestamp+'</p>'+
        		'<div>'+data.message+'</td>'+
        	'</article>';
        chat.append(ele)
    };

    $("#go").on("click", function() {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
    });
});