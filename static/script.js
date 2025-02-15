document.addEventListener("DOMContentLoaded", function() {
  const chatOutput = document.getElementById('chatOutput');
  const userInput = document.getElementById('userInput');
  const sendBtn = document.getElementById('sendBtn');

  function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = (sender === 'user' ? "You: " : "Bot: ") + text;
    chatOutput.appendChild(msgDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    appendMessage('user', message);
    userInput.value = '';

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

  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  });
});
