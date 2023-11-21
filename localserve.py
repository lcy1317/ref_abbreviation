# %%
import re
import pandas as pd
df = pd.read_excel('abbreviation.xlsx')
abbreviations = df['abbreviation'].tolist()
replacements = df['replacement'].tolist()

def getStr(reference):
    # reference = 'Proceedings of the 2020 conference on Computer Vision'
    prep = ["on", "in", "of", "and", "but", "at", "the", "or", "On", "In", "Of", "And", "But", "At", "The", "Or"]
    # 将预置词列表转换为正则表达式模式
    prep_pattern = r'\b(?:' + '|'.join(map(re.escape, prep)) + r')\b'
    reference = re.sub(prep_pattern, '', reference, flags=re.IGNORECASE)
    reference = reference.strip()
    # replace word A in string reference to word B
    def replace(str,A,B):
        str = re.sub(r'\b'+A+r'\b',B,str,flags=re.IGNORECASE)
        return str
    for i in range(0,len(df)):
        A = abbreviations[i]
        B = replacements[i]
        reference = replace(reference,A,B)
    return reference

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import traceback

data = {'result': 'this is a test'}
host = ('0.0.0.0', 12345)
# 从文件加载abi定义
BadRequest = 400

class Resquest(BaseHTTPRequestHandler):
    # def end_headers(self):
    #     self.send_header('Access-Control-Allow-Origin', '*')
    #     self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    #     self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
    #     BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()

        # Respond with an empty body to the pre-flight request
        self.wfile.write(b'')

    def sendsuccess(self,content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        # self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()
        # 构造json错误响应
        res = {
            "code": 200,
            "message": content
        }
        json_data = json.dumps(res)

        # 发送json响应体
        self.wfile.write(json_data.encode())
    def sendpostsuccess(self,content):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # 构造json错误响应
        res = {
            "code": 200,
            "message": content
        }
        json_data = json.dumps(res)

        # 发送json响应体
        self.wfile.write(json_data.encode())

    def sendfailed(self,reason):
        # 设置响应格式为json
        self.send_response(BadRequest)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # 构造json错误响应
        error = {
            "code": 400,
            "message": reason
        }
        json_data = json.dumps(error)

        # 发送json响应体
        self.wfile.write(json_data.encode())



    def do_GET(self):
        # self.send_response(200)
        url = urlparse(self.path)
        print(url.path)
        if url.path == '/getAbbr':
            params = parse_qs(url.query)
            if 'input' in params:
                try:
                    res = getStr(params['input'][0])
                    self.sendsuccess(str(res))
                except:
                    self.sendfailed("获取缩写错误！")  # Bad request
            else:
                self.sendfailed("未包含input参数！")
        else:
            self.send_response(500)
            self.wfile.write(json.dumps(data).encode())
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            self.end_headers()


    def do_POST(self):
        pass
        # datas = self.rfile.read(int(self.headers['content-length']))

        # print('headers', self.headers)
        # print("do post:", self.path, self.client_address, datas)

        # url = urlparse(self.path)

        # if url.path == "/insertsync":
        #     params = parse_qs(url.query)
        #     if 'mtype' in params and 'mcontent' in params:
        #         try:
        #             pass
        #         except Exception as e:
        #             self.sendfailed(str(e))  # Bad request
        #             print("An error occurred while running the script in the background: ", str(e))
        #     else:
        #         self.sendfailed("检查是否包含mtype及mcontent参数")
        # else:
        #     self.sendfailed("Post请求错误")

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

