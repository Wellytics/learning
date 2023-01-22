from transformers import pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS


# KEYWORDS_THRESHOLD = 0.7
# EMOTIONS_THRESHOLD = 0.7

KEYWORDS_MODEL = "yanekyuk/bert-uncased-keyword-extractor"
EMOTIONS_MODEL = "joeddav/distilbert-base-uncased-go-emotions-student"

keywords_pipeline = pipeline("ner", model=KEYWORDS_MODEL)

emotions_pipeline = pipeline(
    "text-classification",
    model=EMOTIONS_MODEL,
    return_all_scores=True,
)

app = Flask(__name__)
CORS(app)


def _get_keywords(text: str):
    outputs = keywords_pipeline(text)
    outputs = sorted(outputs, key=lambda x: x["start"])

    _outputs = []
    for output in outputs:
        if len(_outputs) == 0:
            _outputs.append(output)
        else:
            last_merged_output = _outputs[-1]
            if output["start"] == last_merged_output["end"]:
                x = last_merged_output["word"].replace("#", "")
                y = output["word"].replace("#", "")
                last_merged_output["word"] = x + y
                last_merged_output["end"] = output["end"]
            else:
                _outputs.append(output)

    outputs = sorted(_outputs, reverse=True, key=lambda x: x["score"])

    return outputs


def _get_emotions(text: str):
    outputs = emotions_pipeline(text)[0]
    outputs = sorted(outputs, reverse=True, key=lambda x: x["score"])
    return outputs


@app.route("/keywords", methods=["POST"])
def keywords():
    return jsonify(_get_keywords(request.json["text"]))


@app.route("/emotions", methods=["POST"])
def emotions():
    return jsonify(_get_emotions(request.json["text"]))
