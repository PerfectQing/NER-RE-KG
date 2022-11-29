from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from codes.ner import predict
from markupsafe import Markup

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    name = say_hello('Pgq')
    age = 25
    # print(url_for('hello_world'))
    processed_text = process('Hello, world!')
    if request.method == 'POST':
        # input_text = form['input_text']
        input_text = request.form['input_text']
        processed_text = process(input_text)
    return render_template('index.html', name=name, age=age, processed_text=processed_text, debug=True)


def say_hello(name):
    return 'Hello, ' + name + '!'

def process(text):
    return text.upper()


@app.route('/ner', methods=['GET', 'POST'])
def ner_process():
    html_id_css = 'ner.css'
    processed_text_ner = ''
    # input_text_ner == 'No input'
    if request.method == 'POST':
        input_text_ner = request.form['input_text_ner']
        if input_text_ner == '':
            processed_text_ner = 'No entities found...'
            input_text_ner = 'Please input a sentence.'
        else:
            processed_text_ner = predict(input_text_ner)
    else:
        input_text_ner = ''
        processed_text_ner = ''
    # if request.method == 'GET':
        # request.form['res_text_ner'] = processed_text
    # Markup(processed_text_ner)
    return render_template('ner.html', html_id_css=html_id_css, processed_text_ner=Markup(processed_text_ner * 10), input_text_ner=input_text_ner)



@app.route('/re')
def re_process():
    html_id_css = 're.css'
    processed_text = 'Function waiting to add..'
    if request.method == 'POST':
        input_text = request.form['input_text']
        processed_text = process(input_text)
        
    return render_template('re.html', html_id_css=html_id_css, processed_text=processed_text)

@app.errorhandler(405)
def not_found(error):
    
    processed_text = 'Function to be added...'
    # return render_template('error.html', ), 405
    return render_template('error.html', res_text=processed_text)

@app.errorhandler(404)
def not_found(error):
    
    processed_text = '404 Not Found'
    # return render_template('error.html', ), 405
    return render_template('404.html', res_text=processed_text)

@app.route('/kg', methods=['GET', 'POST'])
def kg_process():
    html_id_css = 'kg.css'
    processed_text_re = ''
    if request.method == 'POST':
        input_text_kg = request.form['input_text_kg']
        # processed_text_re = process(input_text)
        print(input_text_kg)
        processed_text_re = input_text_kg
    else:
        print('Nothing')
    return render_template('kg.html', html_id_css=html_id_css, processed_text_re=processed_text_re)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=8080, host='0.0.0.0', debug=True)
