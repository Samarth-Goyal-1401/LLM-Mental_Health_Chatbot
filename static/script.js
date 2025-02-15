
document.addEventListener("DOMContentLoaded", function() {
    // Get DOM elements
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
  
    // Store chat message in database via POST request
    function storeChat(sender, message) {
      const timestamp = new Date().toISOString();
      const data = { sender: sender, message: message, timestamp: timestamp };
      fetch('/storeChat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      .then(response => response.text())
      .then(result => {
        console.log('Chat stored:', result);
      })
      .catch(error => {
        console.error('Error storing chat:', error);
      });
    }
  
    // Send user message to LLM endpoint and handle response
    function sendMessage() {
      const message = userInput.value.trim();
      if (!message) return;
  
      // Append user message and store it in the database
      appendMessage('user', message);
      storeChat('user', message);
      userInput.value = '';
  
      // Send message to your LLM model endpoint
      fetch('/get?msg=' + encodeURIComponent(message))
        .then(response => response.text())
        .then(data => {
          // Append bot response and store it
          appendMessage('bot', data);
          storeChat('bot', data);
        })
        .catch(error => {
          console.error('Error:', error);
          const errorMsg = "Sorry, there was an error processing your request.";
          appendMessage('bot', errorMsg);
          storeChat('bot', errorMsg);
        });
    }
  
    // Add event listeners for the send button and Enter key press
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });
  });
  