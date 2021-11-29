# import requests

# d = {
#   "name": "string",
#   "base_url": "string",
#   "variables": [
#     {}
#   ],
#   "parameters": [
#     {}
#   ],
#   "export": [
#     {}
#   ]


# }

# # u = 'http://localhost:5000/teststep/v1/run_teststep'
# # from dd import mydata
# # r = requests.post(u,json=mydata)
# # print(r.text)
# # import datetime
# # import time
# # print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# kkkk = {
#     "status": 0,
#     "msg": "ok",
#     "data": {
#         "summary": {
#             "name": "\u6d4b\u8bd5\u73af\u5883",
#             "success": 'true',
#             "case_id": "b3e9f725a52e46a1a5ae0395a948f2f7",
#             "time": {
#                 "start_at": 1637231389.000433,
#                 "start_at_iso_format": "2021-11-18T10:29:49.000433",
#                 "duration": 0.06182742118835449,
#                 "start_datetime": "2021-11-18T10:29:49.000433"
#             },
#             "in_out": {
#                 "config_vars": {
#                     "clientType": "mch",
#                     "gztest_url": "http://192.168.50.34:18081",
#                     "phone": "098630001",
#                     "url": "https://postman-echo.com"
#                 },
#                 "export_vars": {}
#             },
#             "log": "hrproject\\hrtmp\\logs\\b3e9f725a52e46a1a5ae0395a948f2f7.run.log",
#             "step_datas": [
#                 {
#                     "success": 'true',
#                     "name": "test",
#                     "data": {
#                         "success": '',
#                         "req_resps": [
#                             {
#                                 "request": {
#                                     "method": "POST",
#                                     "url": "http://192.168.50.34:18081/api/public/token/getSignToken?clientType=mch&phone=098630001&timeStamp=1637231389003",
#                                     "headers": {
#                                         "User-Agent": "python-requests/2.22.0",
#                                         "Accept-Encoding": "gzip, deflate",
#                                         "Accept": "*/*",
#                                         "Connection": "keep-alive",
#                                         "HRUN-Request-ID": "HRUN--389003",
#                                         "Content-Length": "0"
#                                     },
#                                     "cookies": {},
#                                     "body": 'null'
#                                 },
#                                 "response": {
#                                     "status_code": 200,
#                                     "headers": {
#                                         "Server": "nginx/1.16.0",
#                                         "Date": "Thu, 18 Nov 2021 10:29:49 GMT",
#                                         "Content-Type": "application/json;charset=UTF-8",
#                                         "Transfer-Encoding": "chunked",
#                                         "Connection": "keep-alive",
#                                         "Access-Control-Allow-Origin": "*",
#                                         "Access-Control-Allow-Credentials": "true",
#                                         "Access-Control-Allow-Methods": "*",
#                                         "Access-Control-Allow-Headers": "Content-Type,Access-Token,login-token,verify-type",
#                                         "Access-Control-Expose-Headers": "*"
#                                     },
#                                     "cookies": {},
#                                     "encoding": "UTF-8",
#                                     "content_type": "application/json;charset=UTF-8",
#                                     "body": {
#                                         "code": 200,
#                                         "datas": {
#                                             "token": "054fa4b39f16453d96c12d803b427d7c-1637231389203"
#                                         }
#                                     }
#                                 }
#                             }
#                         ],
#                         "stat": {
#                             "content_size": 0,
#                             "response_time_ms": 8.84,
#                             "elapsed_ms": 8.105
#                         },
#                         "address": {
#                             "client_ip": "192.168.50.129",
#                             "client_port": 1286,
#                             "server_ip": "192.168.50.34",
#                             "server_port": 18081
#                         },
#                         "validators": {
#                             "validate_extractor": [
#                                 {
#                                     "comparator": "equal",
#                                     "check": "status_code",
#                                     "check_value": 200,
#                                     "expect": 200,
#                                     "expect_value": 200,
#                                     "message": "",
#                                     "check_result": "pass"
#                                 }
#                             ]
#                         }
#                     },
#                     "export_vars": {}
#                 }
#             ]
#         },
#         "report_name": "524.yml.html",
#         "report_path": "hrproject\\hrtmp\\reports\\524.yml.html"
#     }
# }



# # from utils import run_testcases

# # a = ['D:\\广州智购\\代码\\接口平台\\apitest\\hrproject\\hrtmp\\testcases\\189.yml', 'D:\\广州智购\\代码\\接口平台\\apitest\\hrproject\\hrtmp\\testcases\\149.yml']
# # i = 'D:\\广州智购\\代码\\接口平台\\apitest\\hrproject\\hrtmp'
# # s = run_testcases(a,i)


# from utils import create_httprunner_projiect

# print(create_httprunner_projiect('testtt'))


# import requests

# u = 'http://192.168.50.129:5000/debugtalk/v1/get_debugtalk?project_id=2ccd4ee0eb8b422085e89b81beeaa3d4'
# print(requests.get(u).text)
a = '6/reports/testcase_5_20211129130654688.html'
b = a.split('/')[:-1]
print('/'.join(b))