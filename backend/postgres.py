import psycopg2

try:
	conn = psycopg2.connect(" dbname='techcrunch' host = 'techcrunch1.c4zgnitpovl7.us-west-2.rds.amazonaws.com' user='mudy' password='techcrunch' ")

except:
    print "I am unable to connect to the database."

cur = conn.cursor()
try:
    cur.execute("""SELECT * from test_table""")
except:
    print "I can't SELECT from bar"

rows = cur.fetchall()
print "\nRows: \n"
for row in rows:
    print "   ", row