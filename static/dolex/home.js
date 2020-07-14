var user = {{ usuario }};
textarea = document.querySelector('#chat_log');
var chatSocket = new WebSocket('wss://'+window.location.host+'/ws/home/');
chatSocket.onmessage = function(e){
	var data = JSON.parse(e.data);
	var user_j = data['user'];
	var message = data['message'];
	document.querySelector('#chat_log').value += ( '@'+user_j+': '+ message + '\n');
	textarea.scrollTop = textarea.scrollHeight;				
};
chatSocket.onclose = function(e) {
	console.error('Chat WS closed.');
};
//document.querySelector('#chat_input').focus();
document.querySelector('#chat_input').onkeyup = function(e){
if (e.keyCode === 13) {
	if (document.querySelector('#chat_input').value != '') {
		var messageInputDom = document.querySelector('#chat_input');
		var message = messageInputDom.value;
		chatSocket.send(JSON.stringify({
			'user': user,
			'message': message
		}));
		messageInputDom.value='';
		}else{
			if (document.querySelector('#chat_input').value === '') {
			}
		}

}	
};