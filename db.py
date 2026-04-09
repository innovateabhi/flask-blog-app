import MySQLdb

db = MySQLdb.connect(
    host="localhost",
    user="root",      # default XAMPP user
    passwd="",        # empty password
    db="blog_db"      # your database name
)

cursor = db.cursor()