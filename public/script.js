
const API_URL = "http://127.0.0.1:8000";

let currentDocumentId = null;

const pdfFile = document.getElementById("pdfFile");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const chatMessages = document.getElementById("chatMessages");
const chatStatus = document.getElementById("chatStatus");
const documentInfo = document.getElementById("documentInfo");


// Display a message
function addMessage(text, sender) {
    const message = document.createElement("div");

    message.classList.add("message");

    message.classList.add(
        sender === "user" ? "user-message" : "ai-message"
    );

    message.textContent = text;

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Display retrieved sources
function addSources(sources) {

    if (!sources || sources.length === 0) {
        return;
    }

    const container = document.createElement("div");
    container.className = "sources-container";

    const heading = document.createElement("h4");
    heading.textContent = "Sources used";
    container.appendChild(heading);

    sources.forEach((source) => {

        const sourceBox = document.createElement("div");
        sourceBox.className = "source-box";

        const title = document.createElement("strong");

        title.textContent =
            `Source ${source.source_number}`;

        const content = document.createElement("p");
        content.textContent = source.content;

        const similarity = document.createElement("small");

        similarity.textContent =
            `Similarity score: ${source.similarity}`;

        sourceBox.appendChild(title);
        sourceBox.appendChild(content);
        sourceBox.appendChild(similarity);

        container.appendChild(sourceBox);
    });

    chatMessages.appendChild(container);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Upload PDF
uploadBtn.addEventListener("click", async () => {

    const file = pdfFile.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF file.";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        uploadStatus.textContent = "Only PDF files are allowed.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadBtn.disabled = true;
    uploadStatus.textContent = "Uploading and processing document...";

    try {

        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed.");
        }

        currentDocumentId = data.document_id;

        uploadStatus.textContent =
            `Upload successful! ${data.total_chunks} chunks stored.`;

        documentInfo.textContent =
            `Document: ${data.filename} | ID: ${data.document_id}`;

        chatMessages.replaceChildren();

        addMessage(
            `Document "${data.filename}" uploaded successfully. You can now ask questions.`,
            "ai"
        );

    } catch (error) {

        uploadStatus.textContent = error.message;

    } finally {

        uploadBtn.disabled = false;

    }

});


// Send question
async function sendQuestion() {

    const question = questionInput.value.trim();

    if (!question) {
        chatStatus.textContent = "Please enter a question.";
        return;
    }

    if (!currentDocumentId) {
        chatStatus.textContent = "Please upload a PDF first.";
        return;
    }

    addMessage(question, "user");

    questionInput.value = "";

    sendBtn.disabled = true;
    chatStatus.textContent = "Generating answer...";

    try {

        const response = await fetch(`${API_URL}/chat`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                document_id: currentDocumentId
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Chat request failed.");
        }

        addMessage(data.answer, "ai");

        // Display source references
        addSources(data.sources);

        chatStatus.textContent =
            `Retrieved chunks: ${data.retrieved_chunks}`;

    } catch (error) {

        chatStatus.textContent = error.message;

        addMessage(
            "Sorry, I couldn't process your question. Please try again.",
            "ai"
        );

    } finally {

        sendBtn.disabled = false;

    }

}


// Send button
sendBtn.addEventListener("click", sendQuestion);


// Enter key
questionInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        sendQuestion();
    }

});
