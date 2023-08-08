import requests
import io


class api:
    #
    def __init__(self):
        self.lens = None

    def add_(self,lens):
        self.lens = lens
    def api_(self, text, id, lenth, emotion):
        url = f'http://192.168.193.23:23456/voice/vits?text={text}&id={id}&format=wav&lang=zh&length={lenth}&noise={emotion}'
        r = requests.get(url)
        stream = io.BytesIO(r.content)
        temp_wav_file = f"temp{self.lens}.wav"
        self.lens -= 1
        with open(temp_wav_file, "wb") as f:
            f.write(stream.getvalue())

        return temp_wav_file
        # return temp_wav_file
