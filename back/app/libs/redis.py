from typing import Optional, Union, Callable
import json
from redis import Redis
from rq import Queue

from app.envs import envs

redis_client = Redis(host="redis", port=6379, db=0)
queue = Queue(envs['NAME_QUEUE'], connection=redis_client)

def save_redis(key: str, data: Optional[Union[dict, list, str]], exp: int = 60 * 5):
    if not data:
        return
    
    if isinstance(data, (dict, list)):
        value = json.dumps(data)
    else:
        value = str(data)
    
    redis_client.set(key, value, ex=exp)
    
def get_redis(key: str):
    value = redis_client.get(key)
    
    if not value:
        return None
    
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value.decode('utf-8')

def delete_redis(key: str):
    redis_client.delete(key)    
    
def insert_queue(queue_fn: Callable ,data: Union[int, dict]):
    queue.enqueue(queue_fn, data)