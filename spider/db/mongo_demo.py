import pymongo

client = pymongo.MongoClient(host='localhost', port=27018)
# 指定db，没有会自动创建
db = client.test

db.students.drop()
# 集合 类似于sql中的表
collection = db.students

student_1 = {
    'id': '20170101',
    'name': '张三',
    'age': 20,
    'gender': 'male'
}
student_2 = {
    'id': '20170102',
    'name': '李四',
    'age': 25,
    'gender': 'male'
}

result = collection.insert_many([student_1, student_2])
print(result)

for item in collection.find():
    print(item)

for item in collection.find({'age': {'$gt': 20}}):
    print(item)
