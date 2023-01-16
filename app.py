from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from codes.ner import predict
from codes.chat import get_chat_gpt_response
from markupsafe import Markup
import json
import time
import markdown

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
def chat_process():
    html_id_css = 'kg.css'
    processed_text_kg = ''
    if request.method == 'POST':
        input_text_kg = request.form['input_text_kg']
        # processed_text_re = process(input_text)
        print(input_text_kg)
        with open('kg_sampel.json', 'r') as fr:
            json_data = json.load(fr)
        # json.loads(json.dumps(json_data))
        # processed_text_kg = json.dumps(json_data)
        processed_text_kg = json_data
        
        print(type(processed_text_kg))
    else:
        print('Nothing')
    return render_template('kg.html', html_id_css=html_id_css, processed_text_kg=processed_text_kg)



@app.route('/chat', methods=['GET', 'POST'])
def kg_process():
    html_id_css = 'stylechat.css'
    processed_text_chat = ''
    input_text_chat = ''
    time_cost = ''
    st_time = time.time()
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables','markdown.extensions.toc']
    try:
        if request.method == 'POST':
            input_text_chat = request.form['input_text_chat']
            # processed_text_re = process(input_text)
            if input_text_chat != '':
                processed_text_chat = get_chat_gpt_response(input_text_chat)
            # processed_text_chat = 'ceshi测试哦ceshi测试哦' * 80
            if '#include' in processed_text_chat and '```' not in processed_text_chat:
                processed_text_chat = '```Cpp\n' + processed_text_chat + '\n```'
            # elif 'import' in processed_text_chat:
            #     processed_text_chat = '```Python\n' + processed_text_chat + '\n```'
            elif '# ' in processed_text_chat and '```' not in processed_text_chat:
                processed_text_chat = '```Python\n' + processed_text_chat + '\n```'
            else:
                processed_text_chat = processed_text_chat
            print('-' * 20)
            remote_addr = request.remote_addr
            with open('request_log.txt', 'a') as fa:
                fa.write('-' * 20)
                fa.write('\n' + remote_addr + '\n' + input_text_chat + '\n' + processed_text_chat + '\n')
                fa.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                fa.write('\n')
                fa.write('-' * 20)
            print(remote_addr)
            print(input_text_chat)
            print(type(processed_text_chat))
            print(processed_text_chat)
            print('-' * 20)
            # processed_text_chat += '\n' + str(round(time.time() - st_time, 5))
            time_cost = 'Time cost: ' + str(round(time.time() - st_time, 5)) + ' s'
            print(processed_text_chat)
            # processed_text_chat = markdown.markdown(processed_text_chat, extensions=exts)
            md=markdown.Markdown(extensions=exts)
            processed_text_chat=md.convert(processed_text_chat)
            # print(processed_text_chat)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            # processed_text_chat = Markup(html)
        else:
            print('Nothing input')
    except:
        processed_text_chat = 'API 出了点问题，稍后再试。'
    return render_template(
        'chatgpt.html',
        html_id_css=html_id_css,
        input_text_chat=input_text_chat,
        processed_text_chat=Markup(processed_text_chat),
        time_cost=time_cost
    )




if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=8080, host='0.0.0.0', debug=True)
    print('load success.')
