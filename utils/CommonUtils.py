# coding: utf-8
import subprocess
import time
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

try:
    PCJS = execjs.compile(open("../static/hhuPC.js", "r", encoding='utf-8').read())
except:
    PCJS = execjs.compile(open("static/hhuPC.js", "r", encoding='utf-8').read())

try:
    VisitorPCJS = execjs.compile(open("../static/hhuVisitor.js", "r", encoding='utf-8').read())
except:
    VisitorPCJS = execjs.compile(open("static/hhuVisitor.js", "r", encoding='utf-8').read())

try:
    GraduateJS = execjs.compile(open(r'../static/hhuGraduatePC.js', 'r', encoding='utf-8').read())
except:
    GraduateJS = execjs.compile(open(r'static/hhuGraduatePC.js', 'r', encoding='utf-8').read())

try:
    FingerJS = execjs.compile(open(r'../static/finger.js', 'r', encoding='utf-8').read())
except:
    FingerJS = execjs.compile(open(r'static/finger.js', 'r', encoding='utf-8').read())


def generateFingerPrint():
    return FingerJS.call("generateFingerPrint")

def generatePCpwdDefaultEncrypt(password, salt):
    return PCJS.call("encryptAES", password, salt)

def generateVisitpwdDefaultEncrypt(xy, key):
    return VisitorPCJS.call("encryptCaptcha", xy, key)

def generateGraduatepwdDefaultEncrypt(encryStr):
    return GraduateJS.call("getDAesString", encryStr)

def get_current_data():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def get_next_data():
    return time.strftime('%Y-%m-%d', time.localtime(time.time() + 24 * 60 * 60))

if __name__ == '__main__':
    print(generatePCpwdDefaultEncrypt("1", "2"))
    print(get_next_data())
    print(generateFingerPrint())