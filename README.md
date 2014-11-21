# Message Based Simulator GUI

* Message Based Simulator (MBS) のGraphical User Interface.
* 以下の操作を可能とする（予定）
  - MBS設定を与えて実行する
  - MBS結果の管理



## 1. Setup

### 1.1. Requirements

||Version|
|------|-----|
|Python|2.7.3|
|Python Django|1.6.5|
|pymongo|2.7|
|python-redis|2.9.1|
|celery|3.1.16|
|(django-celery)|3.1.16|
|MySQL|5.5.38-0ubuntu0.12.04.1|
|mongodb|2.0.4|
|RabbitMQ|3.2.4|


### 1.2. 環境構築

#### python
略

#### MySQL
略

#### MongoDB
略

#### RabbitMQ
略

### 1.3. ソースの取得

```bash:
$ git clone git@distpf2.png.flab.fujitsu.co.jp:dsv-scheduler/message_simulator_gui.git
```

### 1.4. Data Storeの準備 (for UI Server)

#### 1.4.1. 設定

##### MySQL

```python:settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_passwd',
        'HOST': '',
        'PORT': '',
    }
}
```


##### SQLite

```python:settings.py
DATABASES = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### 1.4.2. DB作成

```bash:
$ mysql -uroot -p
Password:
> create database <db_name> default character set utf8;
```

```bash:
$ cd ~/message_simulator_gui
$ python manage.py syncdb
```

### 1.5. 起動

#### 1.5.1. UI Server

* UI serverの起動
```bash:
$ cd ~/message_simulator_gui
$ python manage.py runserver 0.0.0.0:8000
```

* MAIN Workerの起動
```bash:
$ cd ~/message_simulator_gui
$ celery -A sim_dashboard worker -l info -Q MAIN
```


#### 1.5.2. Worker

* シミュレーション実行workerの起動
```bash:
$ cd ~/message_simulator_gui
$ celery -A sim_dashboard worker -l info 
```

## 2. Documents

http://distpf1.png.flab.fujitsu.co.jp/projects/mbsgui/wiki

----
