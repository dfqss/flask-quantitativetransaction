import multiprocessing

from gevent import monkey

monkey.patch_all()


# 绑定的ip和端口
bind = "0.0.0.0:5000"

# 工作模式协程，默认的是sync模式 gevent gthread
# worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
worker_class = "gthread"

# 指定每个进程开启的线程数
threads = 4

# 超时时间
timeout = 200

# 设置守护进程,将进程交给supervisor管理
daemon = False

# 并行工作进程数, int，cpu数量*2+1 推荐进程数
workers = 2
# workers = multiprocessing.cpu_count() * 2 + 1

# 设置最大并发量（每个worker处理请求的工作线程数，正整数，默认为1）
worker_connections = 2000

# 最大客户端并发数量，默认情况下这个值为1000。此设置将影响gevent和eventlet工作模式
max_requests = 2000

# 设置访问日志和错误信息日志路径
pidfile = "/home/mba/mba-service/gunicorn.log"
accesslog = "/home/mba/mba-service/error.log"

# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# loglevel = 'info'

# 是否调试模式
debug = False

# gunicorn启动flask定时任务重复执行的问题
# preload_app = True

