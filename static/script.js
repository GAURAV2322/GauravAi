
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const question = messageInput.value.trim();

    if (!question) return;

    // Display the user's message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = question;
    chatBox.appendChild(userMessage);

    messageInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Display a temporary loading message
    const loadingMessage = document.createElement("div");
    loadingMessage.className = "message assistant";
    
loadingMessage.innerHTML = `
    <span class="thinking">
        <span></span>
        <span></span>
        <span></span>
    </span>
`;
chatBox.appendChild(loadingMessage);


    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }
        console.log(data.answer);
        
        loadingMessage.innerHTML = DOMPurify.sanitize(
        marked.parse(data.answer)
);



    } catch (error) {
        loadingMessage.textContent =
            "Sorry, something went wrong: " + error.message;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
});

document.querySelectorAll(".suggestion").forEach((button) => {
    button.addEventListener("click", () => {
        messageInput.value = button.textContent;
        chatForm.requestSubmit();
    });
});
