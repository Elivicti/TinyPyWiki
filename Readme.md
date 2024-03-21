# TinyPyWiki

使用`Django`构建的小型Wiki网站框架，**Web综合设计实践**课程的作业。



## 部署

本项目使用`Django`作为服务器后端，因此需要安装`Python`和`Django`模块。
+ `Python`: 3.10.13
+ `Django`: 5.0.3

安装`Django`：

```shell
pip install django==5.0.3
```

安装`Django`的`sslserver`应用（可选）：

```shell
pip install django-sslserver
```

>  **注意**：`sslserver`用于开启使用`https`协议的服务器，若选择不安装此模块，应在`wiki/settings.py`的`INSTALLED_APPS`中移除`sslserver`应用。



在启动服务器前，需要先对数据库进行迁移：

```shell
python manage.py makemigrations
python manage.py migrate
```

之后使用命令开启服务器：

```shell
python manage.py startserver
```

若要开启`https`协议，则使用命令：

```shell
python manage.py startsslserver
```



### 关于脚本

`start_server.sh`提供快捷启动服务器的方式，若第一个参数指定为`ssl`，则会启动`https`协议的服务器。



## 开源协议

[License](LICENSE)

