import psycopg2, db_connect as d, pandas as pd 
snr = pd.read_excel("sgcn_e.xlsx")
fnh = {}
scins = {}

#Create Common Name keys for later
for x in snr.itertuples():
	names = x[1].split(" ")
	tname = ""
	for y in range(2,len(names)):
		tname += names[y] + " "
	fnh[tname[:-1]] = []
	scins[tname[:-1]] = names[0] + " " + names[1]

try:

	connection = psycopg2.connect(user = d.dbu, password = d.dbp, host = d.dbh, port = d.dbpo, database = d.dbd)
	cursor = connection.cursor()
	range_query = "SELECT tr.id, tr.taxon_id, t.common_name, h.name FROM taxon_range as tr INNER JOIN taxon as t " \
	+ "on tr.taxon_id = t.id INNER JOIN huc as h ON tr.huc_id = h.id;"
	cursor.execute(range_query)
	records = cursor.fetchall()

	#If common name in tdic, append huc name to val list
	for row in records:
		print(row[2])
		if(row[2] in fnh):
			#print(row[2])
			if(row[3] not in fnh[row[2]]):
				fnh[row[2]].append(row[3])

except(Exception, psycopg2.Error) as error:
	print("Error while connecting", error)

finally:
    #closing database connection.
    if(connection):
       	cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

#Add Common / Sci name to list & all hucs & create df
finarr = []
for key in fnh:
	tarr = [scins[key],key]
	tarr += fnh[key]
	finarr.append(tarr)
df = pd.DataFrame(finarr)
df.to_csv('sgcn_ranges.csv')