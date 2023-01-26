# Flask API 

import openai
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route('/', methods=['POST'])
def generate_response():
    try:
        data = json.loads(request.data)
        message = data['message']
        # api_key = data['api_key']
        # organization = data['organization']
    except KeyError as e:
        return jsonify({'error': f'{e} not provided in request'}), 400
    except json.JSONDecodeError as e:
        return jsonify({'error': 'Invalid JSON provided in request'}), 400

    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.organization = os.environ["OPENAI_ORG_KEY"]

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(f"Pretend your name is Ana. You're pretty much a genius however an arogant genius. You will respond to each question with the most confidence. If you are unsure what someone is asking you should respond by asking them a question to further understand their question.  You are also an expert at things like computer programming, cooking, giving advice, telling jokes that are philosphical"
                    f"Person: {message}?"
                    f"Ana:"),
            max_tokens=100,
            temperature=0,
        )
        if response.choices[0].text:
            return jsonify({'message': response.choices[0].text}), 200
        else:
            return jsonify({'message': 'Sorry, please clarify what you mean.'}), 200
    except openai.exceptions.OpenAiError as e:
        logging.error(e)
        return jsonify({'error': 'Error communicating with OpenAI, check logs for more information'}), 500

@app.route('/chef', methods=['POST'])
def generate_recipe():
    try:
        data = json.loads(request.data)
        message = data['message']
        api_key = data['api_key']
        organization = data['organization']
    except KeyError as e:
        return jsonify({'error': f'{e} not provided in request'}), 400
    except json.JSONDecodeError as e:
        return jsonify({'error': 'Invalid JSON provided in request'}), 400

    openai.api_key = api_key
    openai.organization = organization

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(f"Pretend you are the best Chef in the world with tons of expertise across all cuisines."
                    f"Answers should list out recipes based on the ingredients a person responds with. The Chef should also be able to answer questions about the recipe."
                    f"Provide at least 5 to 10 different recipes for each ingredient combination. The list should be in json format."
                    f"Chef: What ingredients would you like to use in your recipe?"
                    f"Chicken and Broccoli Alfredo."
                    f"Chicken and Broccoli Mushroom Casserole."
                    f"Person: {message}?"
                    f"Ana:"),
            max_tokens=250,
            temperature=0,
        )
        if response.choices[0].text:
            return jsonify({'message': response.choices[0].text}), 200
        else:
            return jsonify({'message': 'Sorry, please clarify what you mean.'}), 200
    except openai.exceptions.OpenAiError as e:
        logging.error(e)
        return jsonify({'error': 'Error communicating with OpenAI, check logs for more information'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
