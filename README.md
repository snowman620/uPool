# uPool
一个整合了协程和数据库连接池的非阻塞框架。

python对数据库的操作，大多是ORM，或者基于多进程+协程的现开现用，已经ok了。

本框架把连接池、uwsgi和gevent进行整合，可以一用。

#### 整合思路
uwsgi中，启用延时加载，按需配置多进程、每个进程里不再开多线程，直接用协程，每个进程建一个数据库连接池实例。

#### 配置说明
1. 只适用于linux环境

2. flask + uwsgi + gevent + pymysql

3. 安装uwsgi，参数配置见 uPool/confs/uwsgi.ini
```
pip install uwsgi
```
```
[uwsgi]
... ...
;启用master
master = true
;进程数
processes = 2
;启用延时加载
lazy-apps=true
;协程数
gevent = 100
... ...
```
4. 安装依赖
```
pip install -r requirements.txt
```
5. 数据库在 uPool/config.py 中配
```
class DevConfig(Config):
    # DB
    DB_HOST = '192.168.217.128'
    DB_PORT = 3306
    DB_NAME = 'uPool'
    DB_USER = 'admin'
    DB_PASS = '123456'
    # DB Pool
    DB_POOL_MAX_CONN = 5
    ... ...
```

#### 使用说明
1. 访问测试 uPool/wsgi.py
```
# 本地测试 http://127.0.0.1:5000/

@app.route('/')
def status():
    return json.dumps({'code': 1, 'msg': 'API is running'})
```
2. 示例代码 uPool/app/user/view.py
```
# 本地测试 http://127.0.0.1:5000/user/list

@user.route('/list', methods=['GET'])
def user_list():
    """demo"""
    try:
        conn = db_pool.get_conn()
        results = conn.query_all('SELECT `id`,`name` FROM `tb1`')
        return json.dumps({'code': 1, 'msg': 'ok', 'data': [{'id': n[0], 'name': n[1]} for n in results]})
    except QueueEmptyException:
        # do something
        return json.dumps({'code': 0, 'msg': 'queue empty'})
    except Exception as e:
        # do something
        return json.dumps({'code': 0, 'msg': 'error'})
```
3. 获取连接 uPool/app/utils/db_helper.py
```
... ...

def get_conn(self, retry=3):
    """取出一个连接"""
    try:
        return self._pool.get_nowait()
    except:
        # 重试3次
        gevent.sleep(0.1)
        if retry > 0:
            retry -= 1
            return self.get_conn(retry)
        else:
            raise QueueEmptyException()

... ...
```
