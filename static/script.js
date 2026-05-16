async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value;

    if (!message) return;

    // USER MESSAGE
    chatBox.innerHTML += `
        <div class="message user">
            ${message}
        </div>
    `;

    input.value = "";

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        console.log(data);

        // AI RESPONSE
        if (data.response) {

            chatBox.innerHTML += `
                <div class="message bot">
                    ${data.response}
                </div>
            `;

        }

        // ERROR RESPONSE
        else if (data.error) {

            chatBox.innerHTML += `
                <div class="message bot">
                    ERROR: ${data.error}
                </div>
            `;
        }

        else {

            chatBox.innerHTML += `
                <div class="message bot">
                    Unknown server response
                </div>
            `;
        }

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        console.error(error);

        chatBox.innerHTML += `
            <div class="message bot">
                Failed to connect to backend
            </div>
        `;
    }
}
