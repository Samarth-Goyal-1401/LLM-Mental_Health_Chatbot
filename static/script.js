// script.js

document.addEventListener("DOMContentLoaded", function() {
  const chatOutput = document.getElementById('chatOutput');
  const userInput = document.getElementById('userInput');
  const sendBtn = document.getElementById('sendBtn');

  // Append message to the chat area
  function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = (sender === 'user' ? "You: " : "Bot: ") + text;
    chatOutput.appendChild(msgDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  // Send the user message to the /chat endpoint
  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Append the user's message and clear the input
    appendMessage('user', message);
    userInput.value = '';
    
    // Fetch the bot's response
    fetch('/chat?msg=' + encodeURIComponent(message))
      .then(response => response.json())
      .then(data => {
        appendMessage('bot', data.response);
      })
      .catch(error => {
        console.error('Error:', error);
        appendMessage('bot', "Sorry, there was an error processing your request.");
      });
  }

  // Event listeners for the send button and Enter key press
  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  });
});
