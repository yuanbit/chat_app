document.addEventListener('DOMContentLoaded', () => {
  // Make 'enter' key submit message
  let msg = document.querySelector('#user_message');
  // Check if the last key pressed was 'enter'
  msg.addEventListener('keyup', event => {
    event.preventDefault();
    // Check keycode for 'enter'
    if (event.keyCode == 13) {
      document.querySelector('#send_message').click();
    }
  })
})
