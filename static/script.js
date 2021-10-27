var sendMessage = document.getElementById('sendMessage')
var input = document.getElementById("messageText")
var messages = document.getElementById('messages')
var array = new Array();
            
var ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (event) => {
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)

};


insert = (val) =>{

    array[array.length]=val;

    let input = document.getElementById("messageText")
    let string = input.value
    let message = string
    let messageId = array.length

    let fullMessageStr = `${messageId}. ${message}`;
    let fullMessage = JSON.stringify(fullMessageStr)

    ws.send(JSON.parse(fullMessage));
    input.value = ''
}

