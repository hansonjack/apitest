#### DDD - Python & FLASK-RESTFUL  


### Installation
- python3 -m venv demo-env
- source demo-env/bin/activate
- pip3 install -r requirements.txt

### to run project
- python app.py

- view on browser url : http://127.0.0.1:5000/


### 框架使用步骤
####
    先在domain 中定义model，然后在infrastructure中定义异常，然后在domain中定义factory
####
    写完domain,接着写infrastructure 中的respository,然后在持久化层persistence中的mapping中添加model
####
    写完infrastructure后，写application层，controller为业务逻辑处理层，resource为接口层，处理接收前端参数

##  nginx 在mime.types文件中，添加以下两种文件的传输类型，以便在浏览器查看
### text/plain                                       log;
### text/plain                                       yml;


