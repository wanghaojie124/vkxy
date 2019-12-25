import requests
import base64
from PIL import Image
import uuid
import os

url = "http://47.98.164.173:8081/captcha/v1"


def image2base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def download_sinle(url, name):
    r = requests.get(url)
    with open(name, "wb") as f:
        f.write(r.content)


def download(url="http://202.200.144.65/(gac14yvwcsjrzj45cx1fq4ed)/CheckCode.aspx???", num=100):
    for i in range(num):
        name = "captcha/capt.gif"
        download_sinle(url, name)
        im = Image.open("captcha/capt.gif")
        im.show()
        code = input("code: ")
        im.save(f"captcha/{code}_{uuid.uuid4().hex}.gif")


def test():
    sum = 0
    right = 0
    file_names = os.listdir("./captcha")
    for file_name in file_names:
        sum += 1
        di = "captcha/" + file_name
        with open(di, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        right_code = file_name.split("_")[0]
        code = get_code(image_base64)
        if right_code == code:
            right += 1
        print(right_code, code)
    print(sum, right)


def get_code(image_base64):
    data = {
        "image": image_base64,
        # "model_name": "sell-1-3-CNNX-NoRecurrent-H64-CrossEntropy-C1"
    }
    r = requests.post(url, json=data)
    print(r)
    data = r.json()
    print(data)
    if data["code"] == 0:
        return data["message"]


def resize():
    for fn in os.listdir("captcha/"):
        fn1 = "captcha/" + fn
        im = Image.open(fn1)
        im = im.resize((72, 32))
        im.save(fn1)


def download_and_test():
    url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
    name = "./1.jpg"
    download_sinle(url, name)
    image_base64 = image2base64(name)
    code = get_code(image_base64)
    im = Image.open(name)
    im.show()
    print(code)


if __name__ == '__main__':
    # im = test("http://zhjw.scu.edu.cn/img/captcha.jpg")
    # print(im)
    # get_code(im)
    # download()
    # test()
    # resize()
    for i in range(20):
        download_and_test()
        input()