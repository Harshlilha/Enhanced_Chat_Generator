# Import required libraries
from groq import Groq
import gradio as gr
import requests
import os

# Initialize the Groq client
client = Groq(api_key="Replace with your api key")  # Replace with your actual API key


# Function to handle Groq API chat completions
def perform_task(chat_history, task_type):
    try:
        # Define system message
        system_message = {
            "role": "system",
            "content": "You are a helpful assistant designed to perform complex tasks with precision."
        }
        # Add user input
        user_message = {"role": "user", "content": chat_history}
        messages = [system_message, user_message]

        # Customize stop sequence and model based on the task
        model = "llama3-8b-8192"
        stop_sequence = ", 6" if task_type == "Count Example" else None

        # Call Groq API
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=stop_sequence,
            stream=False
        )

        # Extract the result
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {e}"

# Build Gradio UI
def build_ui():
    title = "🌟 Claude.ai-Style Enhanced Generator 🌟"
    description = (
        "💻 **Welcome to the Enhanced Chat Generator!**\n"
        "This AI tool uses the Groq API to:\n"
        "- 🤖 Generate content like **MCQs**, **articles**, or handle **counting tasks**.\n"
        "- 🚀 Experience an intuitive, Claude.ai-inspired interface.\n"
        "Provide a prompt and select a task to begin!"
    )

    with gr.Blocks() as demo:
        # Title and description
        gr.Markdown(f"# {title}")
        gr.Markdown(description)

        # Input fields
        with gr.Row():
            chat_input = gr.Textbox(
                label="📝 Enter Chat History",
                placeholder="Type or paste chat history or instructions here...",
                lines=6
            )

        # Task selector
        with gr.Row():
            task_selector = gr.Radio(
                ["Generate MCQs 📝", "Write an Article ✍️", "Count Example 🔢"],
                label="🎯 Select Task Type",
                value="Generate MCQs 📝"
            )

        # Submit button
        with gr.Row():
            submit_button = gr.Button("💡 Generate")

        # Output display
        output = gr.Textbox(
            label="🌈 AI-Generated Output",
            placeholder="Your result will appear here...",
            lines=10
        )

        # Footer
        gr.Markdown("✨ Designed by HARSH for **Absolute Intelligence Inc.**")

        # Link button action
        submit_button.click(
            fn=perform_task,
            inputs=[chat_input, task_selector],
            outputs=output
        )

    return demo

# Launch the Gradio app
ui = build_ui()
# Get the port from the environment variable (default to 8080 if not set)
port = int(os.environ.get("PORT", 8080))

# Launch Gradio on the specified port
ui.launch(server_port=port, server_name="0.0.0.0")
