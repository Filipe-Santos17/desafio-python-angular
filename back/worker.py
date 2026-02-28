from redis import Redis
from rq import Queue, Worker

listen = ["products"]

redis_conn = Redis(host="redis", port=6379)

if __name__ == "__main__":
    queues = [Queue(name, connection=redis_conn) for name in listen]

    worker = Worker(queues, connection=redis_conn)
    worker.work()