import sqlite3


#The purpose of this file is to run and test my database to see for myself whats inside as i am building

conn = sqlite3.connect('nne/database/mama1.db')

c = conn.cursor()
records = c.execute("select * from Workers")

for record in records:

    print (record)

conn.commit()
conn.close()



