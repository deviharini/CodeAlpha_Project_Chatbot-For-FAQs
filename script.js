const userInput = document.getElementById("userInput");

const chatBox = document.getElementById("chatBox");


function addMessage(message, sender) {

    const messageDiv =
        document.createElement("div");

    messageDiv.classList.add("message");


    if (sender === "user") {

        messageDiv.classList.add(
            "user-message"
        );

    } else {

        messageDiv.classList.add(
            "bot-message"
        );
    }


    messageDiv.textContent = message;


    chatBox.appendChild(messageDiv);


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


async function sendMessage() {

    const question =
        userInput.value.trim();


    if (question === "") {
        return;
    }


    // Display user's message
    addMessage(
        question,
        "user"
    );


    // Clear input
    userInput.value = "";


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        const data =
            await response.json();


        // Display chatbot response
        addMessage(
            data.answer,
            "bot"
        );


    } catch (error) {

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

        console.error(error);
    }
}


// Press Enter to send
userInput.addEventListener(
    "keypress",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);
