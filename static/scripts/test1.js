document.addEventListener('DOMContentLoaded', () => {
    // How to connect to the socketio server
    var socket = io();

    let room;
    // Create event buckets
    // socket.on('connect', () => {
      // Send the message to server when client connects
        // socket.send("Iam connected!");
    // });

    // Displays incoming messages
    // Define message event for the client
    socket.on('message', data => {
      //console.log(`Message received: ${data}`);

      // Display message
      const p = document.createElement('p');
      // Display username
      const span_username = document.createElement('span');
      const span_timestamp = document.createElement('span');
      const br = document.createElement('br');

      span_username.innerHTML = data.username;
      span_timestamp.innerHTML = data.time_stamp;

      p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

      document.querySelector('#display-message-section').append(p);

    });

    // Send Message
    document.querySelector('#send_message').onclick = () => {
      socket.send({'msg': document.querySelector('#user_message').value, 'username': username, 'room': room});
    }

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            // If user is already in the room he wants to join
            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
              // Leave current room to join new room
              leaveRoom(room);
              joinRoom(newRoom);
              room = newRoom;

            }
        }
    })

    // Leave room
    function leaveRoom(room) {
      socket.emit('leave', {'username': username, 'room': room});
    }

    // Join room
    function joinRoom(room) {
      socket.emit('join', {'username': username, 'room': room});
      // Clear message area
      document.querySelector('#display-message-selection').ininnerHTML = ''
    }

    // Print system message
    function printSysMsg(msg) {
      const p = document.createElement('p');
      p.innerHTML = msg;
      document.querySelector('#display-message-selection').append(p);
    }
})
