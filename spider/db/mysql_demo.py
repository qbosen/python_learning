import pymysql

db = pymysql.connect(host='localhost', user='abosen', password='abosen', port=3306)
cursor = db.cursor()
cursor.execute('select version()')
data = cursor.fetchone()
print('Database version:', data)

cursor.execute('drop database if exists spiders')
cursor.execute('create database spiders default character set UTF8MB4')

cursor.execute('use spiders')
create_table_sql = 'create table if not exists students' \
                   '(id varchar(255) not null,name varchar(255) not null,age int not null,primary key (id))'

cursor.execute(create_table_sql)
db.close()
