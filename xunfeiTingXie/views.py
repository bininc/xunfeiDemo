#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import urllib
import urllib3
import time
import json
import hashlib
import base64

# Create your views here.
def index(request):
    return render(request,'index.html')

def tingXie(request):
    file = request.FILES.get('data')
    file_content = file.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'fd2f8731d4358e24e6372da8ea324615'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5b44d31f'
    param_json = json.dumps(param).replace(' ', '');
    x_param = base64.b64encode(param_json.encode('utf-8')).decode('utf-8')
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5((api_key + str(x_time) + x_param).encode('utf-8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum,
                'Content-Type':'application/x-www-form-urlencoded; charset=utf-8'}
    http = urllib3.PoolManager()
    req =  http.request("POST", url, body=body, headers= x_header)
    req_str = req.data.decode('utf-8');
    req_dic = json.loads(req_str);
    sstr=req_dic['data']
    if req_dic['code']!='0':
        sstr='转换失败'
    return HttpResponse(sstr)