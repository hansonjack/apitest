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


##  docker 部署
### dockerfile，每个dockerfile的工作目录要唯一，这样的好处是在docekr compose文件中，共享目录时，不会被覆盖
### docker compose文件
####    nginx容器
    端口要大于1024，并且要用root运行，故要修改nginx.conf文件，要挂载此配置文件。
    mime.types文件中，加了两种文件(.log\.yml)的传输类型为text/plain，故要挂载此配置文件
####    hr_task容器
    执行hrun任务，生成hr report.后续简化api容器功能，把api容器生成yml文件功能放到hr_task容器中，这样hr项目目录问题就不会那么复杂化。
    并且可以彻底解耦。后续，api、api_web 一个docker compose;hr_task,hr_report,nginx 一个docker compose；redis 单独、mysql单独
####    hr_report 容器
    执行hr_report 地址写入数据库


