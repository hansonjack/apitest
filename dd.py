mydata = {
  "method": "GET",
  "content_type": "application/x-www-form-urlencoded",
  "env": "3385c24af78b4cc9af0edc2abfd316e7",
  "name": "测试接口",
  "url": "/get",
  "headers": [
    {
      "key": "User-Agent",
      "value": "HttpRunner/${get_httprunner_version()}"
    }
  ],
  "variables": [
    {
      "value_type": "string",
      "key": "foo1",
      "value": "bar11"
    },
    {
      "value_type": "string",
      "key": "foo2",
      "value": "bar21"
    },
    {
      "value_type": "string",
      "key": "sum_v",
      "value": "${sum_two(1, 2)}"
    }
  ],
  "normal": [
    {
      "value_type": "string",
      "key": "foo1",
      "value": "$foo1"
    },
    {
      "value_type": "string",
      "key": "foo2",
      "value": "$foo2"
    },
    {
      "value_type": "string",
      "key": "sum_v",
      "value": "$sum_v"
    }
  ],
  "validate": [
    {
      "value_type": "int",
      "func": "eq",
      "value1": "status_code",
      "value2": "200"
    },
    {
      "value_type": "string",
      "func": "eq",
      "value1": "body.args.foo1",
      "value2": "bar11"
    }
  ],
  "extract": [
    {
      "key": "foo3",
      "value": "body.args.foo2"
    }
  ]
}

cccc =  {
    "id": "3385c24af78b4cc9af0edc2abfd316e7",
    "name": "测试环境",
    "verify": "False",
    "base_url": "https://postman-echo.com",
    "variables": [
      {
        "key": "foo1",
        "desc": "foo1",
        "value": "config_bar1"
      },
      {
        "key": "foo2",
        "desc": "foo2",
        "value": "config_bar2"
      },
      {
        "key": "expect_foo1",
        "desc": "expect_foo1",
        "value": "config_bar1"
      },
      {
        "key": "expect_foo2",
        "desc": "expect_foo2",
        "value": "config_bar2"
      }
    ],
    "parameters": [],
    "export": [
      {}
    ],
    "path": "string",
    "weight": 1,
    "status": 1,
    "createtime": "2021-09-26 16:35:10",
    "updatetime": "2021-09-27 15:46:45"
  }


jj = {
    "status": 0,
    "msg": "ok",
    "data": {
        "summary": {
            "name": "测试环境",
            "success": 'True',
            "case_id": "",
            "time": {
                "start_at": 1632900209.3393197,
                "start_at_iso_format": "2021-09-29T07:23:29.339320",
                "duration": 1.2727253437042236
            },
            "in_out": {
                "config_vars": {
                    "expect_foo1": "config_bar1",
                    "expect_foo2": "config_bar2",
                    "foo1": "config_bar1",
                    "foo2": "config_bar2"
                },
                "export_vars": {}
            },
            "log": "",
            "step_datas": [
                {
                    "success": 'True',
                    "name": "cxzvcxz",
                    "data": {
                        "success": 'True',
                        "req_resps": [
                            {
                                "request": {
                                    "method": "GET",
                                    "url": "https://postman-echo.com/get",
                                    "headers": {
                                        "User-Agent": "python-requests/2.22.0",
                                        "Accept-Encoding": "gzip, deflate",
                                        "Accept": "*/*",
                                        "Connection": "keep-alive",
                                        "HRUN-Request-ID": "HRUN--209343",
                                        "Content-Length": "11",
                                        "Content-Type": "application/json"
                                    },
                                    "cookies": {},
                                    "body": {
                                        "da": "1"
                                    }
                                },
                                "response": {
                                    "status_code": 200,
                                    "headers": {
                                        "Date": "Wed, 29 Sep 2021 07:23:31 GMT",
                                        "Content-Type": "application/json; charset=utf-8",
                                        "Content-Length": "384",
                                        "Connection": "keep-alive",
                                        "ETag": "W/\"180-GcrkMP3vB5m9CiFLqMBT9E0xNus\"",
                                        "Vary": "Accept-Encoding",
                                        "set-cookie": "sails.sid=s%3Ax5LEZOFosVdObbRrqOmoJGJpA9nPxulz.Zv6G7%2BW2%2BcMoEM47WKbYcuQFagpp0wBrtkF0zremS5g; Path=/; HttpOnly"
                                    },
                                    "cookies": {
                                        "sails.sid": "s%3Ax5LEZOFosVdObbRrqOmoJGJpA9nPxulz.Zv6G7%2BW2%2BcMoEM47WKbYcuQFagpp0wBrtkF0zremS5g"
                                    },
                                    "encoding": "utf-8",
                                    "content_type": "application/json; charset=utf-8",
                                    "body": {
                                        "args": {
                                            "da": "1"
                                        },
                                        "headers": {
                                            "x-forwarded-proto": "https",
                                            "x-forwarded-port": "443",
                                            "host": "postman-echo.com",
                                            "x-amzn-trace-id": "Root=1-61541473-35e3574b40e033c576dbbb05",
                                            "content-length": "11",
                                            "user-agent": "python-requests/2.22.0",
                                            "accept-encoding": "gzip, deflate",
                                            "accept": "*/*",
                                            "hrun-request-id": "HRUN--209343",
                                            "content-type": "application/json"
                                        },
                                        "url": "https://postman-echo.com/get"
                                    }
                                }
                            }
                        ],
                        "stat": {
                            "content_size": 0,
                            "response_time_ms": 1254.99,
                            "elapsed_ms": 254.151
                        },
                        "address": {
                            "client_ip": "N/A",
                            "client_port": 0,
                            "server_ip": "N/A",
                            "server_port": 0
                        },
                        "validators": {
                            "validate_extractor": [
                                {
                                    "comparator": "equal",
                                    "check": "status_code",
                                    "check_value": 200,
                                    "expect": 200,
                                    "expect_value": 200,
                                    "message": "",
                                    "check_result": "pass"
                                }
                            ]
                        }
                    },
                    "export_vars": {}
                }
            ]
        }
    }
}


kkk = {
    "status": 0,
    "msg": "ok",
    "data": {
        "summary": {
            "name": "\u6d4b\u8bd5\u73af\u5883",
            "success": 'True',
            "case_id": "b3e9f725a52e46a1a5ae0395a948f2f7",
            "time": {
                "start_at": 1637231389.000433,
                "start_at_iso_format": "2021-11-18T10:29:49.000433",
                "duration": 0.06182742118835449,
                "start_datetime": "2021-11-18T10:29:49.000433"
            },
            "in_out": {
                "config_vars": {
                    "clientType": "mch",
                    "gztest_url": "http://192.168.50.34:18081",
                    "phone": "098630001",
                    "url": "https://postman-echo.com"
                },
                "export_vars": {}
            },
            "log": "hrproject\\hrtmp\\logs\\b3e9f725a52e46a1a5ae0395a948f2f7.run.log",
            "step_datas": [
                {
                    "success": 'True',
                    "name": "test",
                    "data": {
                        "success": 'True',
                        "req_resps": [
                            {
                                "request": {
                                    "method": "POST",
                                    "url": "http://192.168.50.34:18081/api/public/token/getSignToken?clientType=mch&phone=098630001&timeStamp=1637231389003",
                                    "headers": {
                                        "User-Agent": "python-requests/2.22.0",
                                        "Accept-Encoding": "gzip, deflate",
                                        "Accept": "*/*",
                                        "Connection": "keep-alive",
                                        "HRUN-Request-ID": "HRUN--389003",
                                        "Content-Length": "0"
                                    },
                                    "cookies": {},
                                    "body": ''
                                },
                                "response": {
                                    "status_code": 200,
                                    "headers": {
                                        "Server": "nginx/1.16.0",
                                        "Date": "Thu, 18 Nov 2021 10:29:49 GMT",
                                        "Content-Type": "application/json;charset=UTF-8",
                                        "Transfer-Encoding": "chunked",
                                        "Connection": "keep-alive",
                                        "Access-Control-Allow-Origin": "*",
                                        "Access-Control-Allow-Credentials": "'True'",
                                        "Access-Control-Allow-Methods": "*",
                                        "Access-Control-Allow-Headers": "Content-Type,Access-Token,login-token,verify-type",
                                        "Access-Control-Expose-Headers": "*"
                                    },
                                    "cookies": {},
                                    "encoding": "UTF-8",
                                    "content_type": "application/json;charset=UTF-8",
                                    "body": {
                                        "code": 200,
                                        "datas": {
                                            "token": "054fa4b39f16453d96c12d803b427d7c-1637231389203"
                                        }
                                    }
                                }
                            }
                        ],
                        "stat": {
                            "content_size": 0,
                            "response_time_ms": 8.84,
                            "elapsed_ms": 8.105
                        },
                        "address": {
                            "client_ip": "192.168.50.129",
                            "client_port": 1286,
                            "server_ip": "192.168.50.34",
                            "server_port": 18081
                        },
                        "validators": {
                            "validate_extractor": [
                                {
                                    "comparator": "equal",
                                    "check": "status_code",
                                    "check_value": 200,
                                    "expect": 200,
                                    "expect_value": 200,
                                    "message": "",
                                    "check_result": "pass"
                                }
                            ]
                        }
                    },
                    "export_vars": {}
                }
            ]
        },
        "report_name": "524.yml.html",
        "report_path": "hrproject\\hrtmp\\reports\\524.yml.html"
    }
}