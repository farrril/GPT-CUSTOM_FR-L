from flask import Flask, request, jsonify
import os
import openai
from rag_utils import retrieve_context
from prompts import build_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    q = data.get('query')
    context = retrieve_context(q)
    prompt = build_prompt(q, context)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'system', 'content': prompt}],
        max_tokens=512,
        temperature=0.2
    )
    return jsonify(response.choices[0].message['content'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
