import base64
import configparser
import os
import requests
import sys
import time

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(os.path.dirname(script_dir), "..", "..")
config_dir = os.path.join(root_dir, "Config", "t10x")
captcha_dic_path = os.path.join(config_dir, "captcha.dict")


def get_captcha_string(captcha_img_data):
    comp_str = str(captcha_img_data)

    if ".jpg" in captcha_img_data:
        result = requests.get(url=captcha_img_data)
        comp_str = base64.b64encode(result.content).decode('utf-8')
    else:
        comp_str = str(captcha_img_data)[23:]

    captcha_str = find_captcha(captcha_dic_path, comp_str)

    return str(captcha_str)


def gen_captcha_dict(captcha_dic_path):
    captcha_list = {
                    "polish":"http://192.168.1.1/img/1.70e4cc76.jpg",
                    "loss":"http://192.168.1.1/img/73.84c0544c.jpg",
                    "parce":"http://192.168.1.1/img/40.6419e938.jpg",
                    "spring":"http://192.168.1.1/img/77.28f958df.jpg",
                    "past":"http://192.168.1.1/img/2.b8d1918b.jpg",
                    "adjust":"http://192.168.1.1/img/65.c8030831.jpg",
                    "expert":"http://192.168.1.1/img/38.ccc1831e.jpg",
                    "news":"http://192.168.1.1/img/47.c204956f.jpg",
                    "sound":"http://192.168.1.1/img/21.67fa7203.jpg",
                    "this":"http://192.168.1.1/img/54.64eaf17c.jpg",
                    "muscle":"http://192.168.1.1/img/87.be69fa95.jpg",
                    "crime":"http://192.168.1.1/img/27.2840b59e.jpg",
                    "brain":"http://192.168.1.1/img/46.37e3c900.jpg",
                    "weight":"http://192.168.1.1/img/17.56279326.jpg",
                    "every":"http://192.168.1.1/img/86.d1a4ac03.jpg",
                    "snake":"http://192.168.1.1/img/93.d965d58c.jpg",
                    "glove":"http://192.168.1.1/img/8.7dd2d669.jpg",
                    "skirt":"http://192.168.1.1/img/53.ab3c1cbe.jpg",
                    "sleep":"http://192.168.1.1/img/29.c5ba2b33.jpg",
                    "canvas":"http://192.168.1.1/img/31.d53afe1e.jpg",
                    "when":"http://192.168.1.1/img/4.02c2723d.jpg",
                    "poison":"http://192.168.1.1/img/97.5b57a56d.jpg",
                    "mine":"http://192.168.1.1/img/71.f1844c49.jpg",
                    "small":"http://192.168.1.1/img/19.bce8d145.jpg",
                    "harp":"http://192.168.1.1/img/56.0d7cd65d.jpg",
                    "rain":"http://192.168.1.1/img/49.e810753c.jpg",
                    "screw":"http://192.168.1.1/img/79.5538bc7b.jpg",
                    "bucket":"http://192.168.1.1/img/99.f3071637.jpg",
                    "mother":"http://192.168.1.1/img/70.2493281e.jpg",
                    "desire":"http://192.168.1.1/img/78.ae781580.jpg",
                    "sticky":"http://192.168.1.1/img/9.cfec7cc4.jpg",
                    "knot":"http://192.168.1.1/img/57.8a84b440.jpg",
                    "pocket":"http://192.168.1.1/img/68.2b5afd4c.jpg",
                    "right":"http://192.168.1.1/img/88.66991d78.jpg",
                    "waste":"http://192.168.1.1/img/42.136c465b.jpg",
                    "bent":"http://192.168.1.1/img/81.cf7c1694.jpg",
                    "army":"http://192.168.1.1/img/44.589a9b44.jpg",
                    "butter":"http://192.168.1.1/img/90.6f504801.jpg",
                    "soap":"http://192.168.1.1/img/7.3912ed1c.jpg",
                    "collar":"http://192.168.1.1/img/13.bd9c39d8.jpg",
                    "mine":"http://192.168.1.1/img/32.4c500180.jpg",
                    "degree":"http://192.168.1.1/img/35.adc0b03c.jpg",
                    "flag":"http://192.168.1.1/img/23.03f6580d.jpg",
                    "again":"http://192.168.1.1/img/16.40ef3eef.jpg",
                    "tooth":"http://192.168.1.1/img/98.95a88f99.jpg"
                    }

    for item in captcha_list.items():
        key = item[0]
        url = item[1]
        result = requests.get(url=url)
        base64_str = base64.b64encode(result.content).decode('utf-8')
        save_captcha_item(key, base64_str)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def save_captcha_item(key, value):
    if not os.path.exists(captcha_dic_path):
        print("The captcha dictionary file not exist. Exit!!!")
        return

    f = open(captcha_dic_path, "a")
    f.write(str(key + " = " + value + "\n"))
    f.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_captcha(captcha_list, base64_str):
    if not os.path.exists(captcha_dic_path):
        print("The captcha dictionary file not exist. Exit!!!")
        return

    captcha = read_captcha_dic(captcha_dic_path)
    for i in range(0, len(captcha)):
        key, value = captcha[i].popitem()
        if (base64_str == value):
            return key

    save_captcha_item(str("Unknown_" + str(int(time.time()))), base64_str)
    return str("___NOT_FOUND___")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_captcha_dic(captcha_dic_path):
    if not os.path.exists(captcha_dic_path):
        print("The config file not exist. Exit!!!")
        return

    captcha_list = []
    with open(captcha_dic_path) as f:
        list = f.readlines()

    for i in range(0, len(list)):
        item = str(list[i]).strip()
        element = item.split(" = ")
        if len(element) == 2:
            key = element[0].strip()
            base64_str = element[1].strip()
            cap_i = {key: base64_str }
            captcha_list.append(cap_i)
    return captcha_list
