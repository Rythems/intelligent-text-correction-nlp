from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = Flask(__name__)

MODEL_NAME = "prithivida/grammar_error_correcter_v1"

print("Loading NLP Grammar Correction Model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print("Model Loaded Successfully")

def correct_text(text):

    input_text = "gec: " + text

    tokenized = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=128,
        truncation=True
    ).to(device)

    outputs = model.generate(
        tokenized,
        max_length=128,
        num_beams=5,
        early_stopping=True
    )

    corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/correct", methods=["POST"])
def correct():

    data = request.json
    text = data["text"]

    corrected = correct_text(text)

    return jsonify({
        "corrected_text": corrected
    })


if __name__ == "__main__":
    app.run(debug=True)