function sendMessageToServer(message) {
    fetch('http://localhost:5000/webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data && Array.isArray(data)) {
            data.forEach(response => {
                addMessage('bot', response.text);
            });
        }
    })
    .catch(error => console.error('Error:', error));
}
