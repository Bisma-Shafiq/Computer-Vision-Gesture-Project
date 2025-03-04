function updateAIResponse() {
    fetch('/get_ai_response')
        .then(response => response.json())
        .then(data => {
            document.getElementById("ai-result").innerText = data.response;
        });
}

// Update AI response every 2 seconds
setInterval(updateAIResponse, 2000);
