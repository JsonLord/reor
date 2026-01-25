import gradio as gr
import requests

def answer_question(question):
    response = requests.post("http://localhost:8000/api/query", json={"question": question})
    return response.json()["answer"]

with gr.Blocks(title="Reor AI Assistant") as demo:
    gr.Markdown("# Reor AI Assistant")
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(label="Question")
            answer_button = gr.Button("Answer")
        with gr.Column():
            answer = gr.Textbox(label="Answer")

    answer_button.click(answer_question, inputs=question, outputs=answer)

demo.launch()
