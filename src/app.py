import gradio as gr
from backend import chat_with_llm, build_faiss_index

# Custom CSS for Azulejo-style borders, background, and button
custom_css = """
.azulejo-border {
    position: relative;
    padding: 20px;
    background: white;
    border: 30px solid transparent;
    border-image: linear-gradient(45deg, #3a75c4, #ffffff, #3a75c4) 30;
    border-image-slice: 30;
    border-radius: 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.page-background {
    background-color: #f0ebe3;  /* Soft beige background */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    padding: 40px;
}

/* Fancy border using CSS Grid */
.azulejo-wrapper {
    display: grid;
    grid-template-rows: 50px auto 50px;
    grid-template-columns: 50px auto 50px;
    gap: 10px;
    background-color: white;
}

.tile {
    background: repeating-linear-gradient(45deg, #3a75c4, #3a75c4 10px, white 10px, white 20px);
    width: 100%;
    height: 100%;
    border-radius: 5px;
}

.gr-button {
    background-color: #3a75c4 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

.gr-button:hover {
    background-color: #2d5fa3 !important;

}
.gr-chatbot {
    background-color: #d0e0ee!important; /* Light beige background */
    border: 2px solid #3a75c4 !important; /* Blue border */
    border-radius: 10px !important;
    color: #002d62 !important; /* Dark blue text */
    font-weight: bold !important;
}

.gr-textbox {
    background-color: #e7e7e7!important; /* White background */
    border: 2px solid #3a75c4 !important; /* Blue border */
    border-radius: 10px !important;
    color: #002d62 !important; /* Dark blue text */
    font-size: 16px !important;
    padding: 8px !important;
}
.gr-chatbot .bot {
    background-color: #e7e7e7!important; /* Blue AI message */
    color: white !important; /* White text */
    border-radius: 10px !important;
    font-size: 16px !important;
    border: 1px solid #3a75c4
}

/* Style User messages */
.gr-chatbot .user {
    background-color: #ffffff !important; /* White user message */
    text-color: #002d62 !important; /* Dark blue text */
    border-radius: 10px !important;
    font-size: 16px !important;
    border: 1px solid #3a75c4 !important; /* Blue border */
}

.gr-textbox::placeholder {
    color: #888888 !important; /* Lighter gray placeholder text */
}

"""

# HTML layout with CSS grid-based tile borders
html_layout = """
<div class="azulejo-wrapper">
    <div class="tile"></div> <div class="tile"></div> <div class="tile"></div>
    <div class="tile"></div> 
    <div class="azulejo-border">
        <h1 style="text-align:center; color:#002d62;">🍽️ Welcome to the Portuguese Recipe Chat! 🍽️</h1>
        <p style="text-align:center;">Ask me anything about Portuguese recipes!</p>
    </div>
    <div class="tile"></div>
    <div class="tile"></div> <div class="tile"></div> <div class="tile"></div>
</div>
"""

# Gradio interface with custom styling
with gr.Blocks(css=custom_css) as demo:
    gr.HTML(html_layout)  # Add the custom HTML border
    
    chat_history = gr.State([])

    chatbot_output = gr.Chatbot(label="🤖 AI's Response", height=400, elem_classes="gr-chatbot", type="messages")
    user_input = gr.Textbox(label="👤 Your Question", placeholder="Ask me about Portuguese recipes...", lines=1, elem_classes="gr-textbox")
    send_button = gr.Button("🍽️ Ask the Chef!",elem_classes="gr-button")

    send_button.click(
        fn=chat_with_llm,
        inputs=[user_input, chat_history],
        outputs=[chat_history]
    ).then(
        lambda h: h, inputs=[chat_history], outputs=[chatbot_output]  # Sync chatbot display
    ).then(
        lambda: "", outputs=user_input  # Clear input
    )


if __name__ == "__main__":
    build_faiss_index() 
    demo.launch()
