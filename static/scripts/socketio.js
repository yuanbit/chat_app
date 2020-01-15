document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Get username
    const username = document.querySelector('#get-username').innerHTML;

    // Set default room
    let room = "Chatroom"
    // Join Chatroom
    joinRoom("Chatroom");

    // Send messages
    document.querySelector('#send_message').onclick = () => {

        // Send message
        socket.emit('message', {'msg': document.querySelector('#user_message').value,
            'username': username, 'room': room});

        // Clear typed message once it's sent
        document.querySelector('#user_message').value = '';
    };

    // Display all incoming messages
    socket.on('message', data => {

        // Display current message
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')

            // Display user's own message
            if (data.username == username) {
                    p.setAttribute("class", "my-msg");
                    // Username
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Timestamp
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                    // Append and display in right panel
                    document.querySelector('#display-message-section').append(p);
            }
            // Display other users' messages
            else if (typeof data.username !== 'undefined') {

                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#display-message-section').append(p);
            }
            // Display system message - user activities
            else {
                printSysMsg(data.msg);
            }

        }
        // Scroll chat window down
        scrollDownChatWindow();
    });

    // Leave the chatroom
    document.querySelector("#logout-btn").onclick = () => {
        leaveRoom(room);
    };

    // Send leave event to server
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    // Send join event to server
    function joinRoom(room) {

        // Join room
        socket.emit('join', {'username': username, 'room': room});

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Focus on text box
        document.querySelector("#user_message").focus();
    }

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Print system messages - user activities
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        // Display on the side panel
        document.querySelector('#display-online-users').append(p);

        scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
});
