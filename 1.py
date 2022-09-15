import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM users")
tmp = res.fetchall()
for i in tmp:
	print(i)
con.commit()
