function appendMessage(sender, text) {
    const messages = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.textContent = sender + ': ' + text;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}
function sendMessageToDeepSeek() {
    const input = document.getElementById('chat-input');
    const userMsg = input.value.trim();
    if (!userMsg) return;
    appendMessage('You', userMsg);
    input.value = '';
    fetch('/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
        },
        body: 'message=' + encodeURIComponent(userMsg)
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            appendMessage('Sourabh', data.response);
        } else {
            appendMessage('Sourabh', 'No response from DeepSeek.');
        }
    })
    .catch(() => appendMessage('Sourabh', 'Error contacting DeepSeek.'));
}
// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.getElementById('chat-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessageToDeepSeek();
    }
});
