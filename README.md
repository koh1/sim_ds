# Message Based Simulator GUI

* Message Based Simulator (MBS) のGraphical User Interface.
* 以下の操作を可能とする（予定）
  - MBS結果の管理
  - MBS結果からChartを描く
  - MBS設定を与えて実行する



## 1. Setup

### 1.1. Requirements

||Version|
|------|-----|
|Python||
|Python Django||
|Python pandas||
|pymongo||
|python-redis||
|MySQL||
|Redis||

### 1.2. 環境構築


### 1.3. ソースの取得




### 1.4. Data Storeの準備

#### 設定

##### MySQL

```python:settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sim_ds',
        'USER': 'root',
        'PASSWORD': 'svn123',
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

#### DB作成

```bash:
$ python manage.py syncdb
```

### 1.5. 起動

```bash:
$ cd xxx
$ python manage.py runserver 0.0.0.0:8000
```



## 2. Usage


## 3. Documents



----