from flask import Flask, request, send_file, render_template, make_response

import requests
from conbined import ffmpeg_
from local_api import api
from cut import cut
import io

app = Flask(__name__)


def get_speaker():
    with open('speaker.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    decoded_string = content.encode().decode('unicode_escape')
    result_list = eval(decoded_string)
    return result_list


def role2id(role):
    speaker = get_speaker()
    import re
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        name = re.sub(pattern, "", speaker[e], re.S)
        if name != speaker[e]:
            speaker[e] = name
    for s in range(len(speaker)):
        if role == speaker[s]:
            return s


def id2role(id):
    import re
    speaker = get_speaker()
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        speaker[e] = re.sub(pattern, "", speaker[e], re.S)
    return speaker[id]


def get_random():
    import random
    import time
    now_seconds = int(time.time())  # 秒
    now_minute = int(now_seconds / 60)  # 分
    now_ten_minute = int(now_minute / 10)
    random.seed(now_ten_minute)
    random_num1 = random.randint(87, 147)
    random_num2 = random.randint(87, 147)
    return random_num1, random_num2, now_ten_minute


def save_random(n1, n2, seed, content):
    n1 = id2role(n1)
    n2 = id2role(n2)
    with open('random.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines:
        last_line = lines[-1].strip()  # 获取最后一行数据
        last_data = last_line.split('|')[0] if '|' in last_line else ''
    else:
        last_data = ''

    if last_data != f'{n1},{n2},{seed}':
        # print('添加')
        with open('random.txt', 'a', encoding='utf-8') as f:
            f.write(f'{n1},{n2},{seed}|{content}\n')


def save_it2(client_ip, speak_text, id_speaker):
    with open('log.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines:
        last_line = lines[-1].strip()  # 获取最后一行数据
        last_data = last_line.split('|')[0] if '|' in last_line else ''
    else:
        last_data = ''

    if last_data != f'{client_ip},{speak_text},{id2role(id_speaker)}':
        # print('添加')
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{client_ip},{speak_text},{id2role(id_speaker)}|{content}\n')


@app.route('/run', methods=['GET'])
def run():
    global indices, content_list
    speak_text = request.args.get('text')
    id_speaker = request.args.get('id_speaker', type=str)
    voice_length = request.args.get('length', type=float)
    voice_noise = request.args.get('noise', type=float)
    noisew = request.args.get('noisew', type=float)
    if noisew is None:
        noisew = 0.4
    if voice_noise is None:
        voice_noise = 0.25
    if voice_length is None:
        voice_length = 1.8

    url = f'http://192.168.193.23:23456/voice/vits?text={speak_text}&id={id_speaker}&format=wav&lang=zh&length={voice_length}&noise={voice_noise}&noisew={noisew}'
    r = requests.get(url)
    stream = io.BytesIO(r.content)
    temp_wav_file = f"temp.wav"

    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    save_it2(client_ip, speak_text, id_speaker)
    with open(temp_wav_file, "wb") as f:
        f.write(stream.getvalue())

    # 其他代码...

    return send_file(temp_wav_file, mimetype='audio/wav')


@app.route('/content', methods=['GET'])
def content():
    with open('log.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    formatted_text = text.replace('\n', '<br>')

    # 返回格式化后的文本
    return formatted_text


@app.route('/random', methods=['GET'])
def ra():
    global indices, content_list
    speak_text = request.args.get('text')
    voice_length = request.args.get('length', type=float)
    voice_noise = request.args.get('noise', type=float)
    content_list, indices = cut.cut_Chinese_double_quotation_marks(speak_text)

    random_num1, random_num2, now_ten_minute = get_random()
    content = ''.join(content_list)
    save_random(random_num1, random_num2, now_ten_minute, content)
    url = f'http://192.168.193.23:23456/voice/vits?text={speak_text}&id={random_num1}&format=wav&lang=zh&length={voice_length}&noise={voice_noise}'
    r = requests.get(url)
    stream = io.BytesIO(r.content)
    temp_wav_file = f"temp.wav"
    with open(temp_wav_file, "wb") as f:
        f.write(stream.getvalue())
    return send_file(temp_wav_file, mimetype='audio/wav')


@app.route('/read', methods=['GET'])
def read():
    with open('random.txt', 'r', encoding='utf-8') as f:
        i = f.read()
    return i


@app.route('/emo', methods=['GET'])
def emo():
    global indices, content_list
    speak_text = request.args.get('text')
    id_speaker = request.args.get('id_speaker', type=str)
    voice_length = request.args.get('length2', type=float)
    voice_noise = request.args.get('noise', type=float)
    url = f'http://192.168.193.23:23456/voice/vits?text={speak_text}&id={id_speaker}&format=wav&lang=zh&length={voice_length}&noise={voice_noise}'
    r = requests.get(url)
    stream = io.BytesIO(r.content)
    temp_wav_file = f"temp.wav"
    with open(temp_wav_file, "wb") as f:
        f.write(stream.getvalue())
    return send_file(temp_wav_file, mimetype='audio/wav')


@app.route('/')
def html():
    return render_template('main.html')


if __name__ == '__main__':
    ffmpeg_ = ffmpeg_()
    api = api()
    cut = cut()
    # print(get_speaker())
    app.run(host='0.0.0.0')
