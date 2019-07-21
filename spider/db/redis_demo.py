from redis import StrictRedis

redis = StrictRedis(host='localhost', port=6379, db=0)
redis.set('name', '张三')
print(redis.get('name'))
print(str(redis.get('name'), encoding='utf8'))
