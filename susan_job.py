import csv
import pandas as pd

def sizeChecker(df, client_id):
	client_ids = []

	cur_id = 0
	max_id = 0
	repeat_id = 0
	#Df non-inlusive 
	for row in df1.itertuples():
		if row[client_id] not in client_ids:
			client_ids.append(row[client_id])
			cur_id = 1
		else:
			cur_id += 1

		if cur_id > max_id:
			max_id = cur_id
			repeat_id = row[client_id]

	print("Max ID? " , max_id)
	print("RepeatID = " , repeat_id)

	print("Client Ids // Length")
	print(client_ids)
	print(len(client_ids))

	max_length = 0
	cur_length = 0
	max_id = 0
	cur_id = 0

	#121 Unique User Ids

	dis_count = 0
	dis_max = 0
	dis_id = 0


	# # of unique visits - Max 6
	for row in df1.itertuples():
		userid = row[1]
		dis_det = row[7]
		if cur_id == 0:
			cur_id = userid
		if cur_id != userid:
			cur_length = 0
			cur_id = userid
			dis_count = 0
		cur_length += 1

		if dis_det == "Yes (HUD)":
			dis_count += 1
		if dis_count > dis_max:
			dis_max = dis_count
			dis_id = userid
		if cur_length > max_length:
			max_id = userid
			max_length = cur_length
	print("Max ID // Length")
	print(max_id)
	print(max_length)
	print("Dis ID // Length")
	print(dis_id)
	print(dis_max)

#create list of column names
def columnGrabber(df):
	columns = []
	for col in df.columns:
		columns.append(col)
	return(columns)

def columnSplitter(columns, uid_col, static_cols, variable_cols, num_repeats, sheet_name):

	#Split columns into static names and variable names (many-to-many relationship)
	uid_head = columns[uid_col]

	first_headers = []
	for a in static_cols:
		first_headers.append(columns[a])
	last_headers = []
	for b in variable_cols:
		last_headers.append(columns[b])

	final_columns = first_headers

	#Create # of many-many variable colums
	for x in range(1,num_repeats):
		tf = uid_head + "." + sheet_name + "." + str(x)
		final_columns.append(tf)
		for y in last_headers:
			final_columns.append(y + "." + str(x))

	return(final_columns)

def dataMaker(df, u_id,cl_id, stat_cols, var_cols):
	final_array = []
	row_array = []
	type_array = []
	start_array = []
	f_client_id = 0
	f_uid = 0	

	for row in df.itertuples():
		current_cli = row[cl_id]
		current_uid = row[u_id]

		#Default State
		if f_client_id == 0:
			f_client_id = current_cli
		if f_uid == 0:
			f_uid = current_uid

		#Change of UID concat variable columns
		if f_uid != current_uid:
			row_array += type_array
			type_array = []
			f_uid = current_uid

		#If ID changes, add static columns and variable columns to creat erows
		if f_client_id != current_cli:
			final_array.append(start_array + row_array)
			start_array = []
			row_array = []
			f_client_id = current_cli

		#Create temporary array for variable rows, then appened onto top variable column list
		tt_ar = []
		for y in var_cols:
			tt_ar.append(row[y])
		tt_ar.insert(0, f_uid)
		type_array += tt_ar

		start_array = [current_cli]
		for xx in stat_cols:
			start_array.append(row[xx])

	return(final_array)

#Import multi-sheet excel file
xls = pd.read_excel('C:/Users/colto/Documents/susan_job.xlsx', sheet_name = None)

#Check Sheet Names
for key, val in xls.items():
	print(key)

df1 = xls["Disab Info"]

#List of Column names for sheet
columns = columnGrabber(df1)
sizeChecker(df1,2)
#Generate proper column framework // columns, uid_col, static_cols, variable_cols, num_repeats
final_columns = columnSplitter(columns, 0, [1,2,3,4], [5,6,7,8,9,10], 93, "Disab")
#Returns data array for df construction // df, u_id,cl_id, stat_cols, var_cols
final_array = dataMaker(df1,1,2,[3,4,5],[6,7,8,9,10,11])
#Disability dataframe
disab_df = pd.DataFrame(data = final_array, columns = final_columns)

#Change dataframe to "Demographic"
df1 = xls["Demo Info"]
columns = columnGrabber(df1)
final_columns = columnSplitter(columns, 0, [1,2,3,13,14,15,16],[4,5,6,7,8,9,10,11,12,17,18,19,20,21,22,23,24,25], 7, "Demo")
final_array = dataMaker(df1,1,2,[4,13,14,15,16,17],[5,6,7,8,9,10,11,12,17,18,19,20,21,22,23,24,25,26])

demo_df = pd.DataFrame(data = final_array, columns = final_columns)

#Change dataframe to "Income Info"
df1 = xls["Income Info"]
columns = columnGrabber(df1)
sizeChecker(df1,2)
final_columns = columnSplitter(columns, 0, [1,3],[2,4,5,6,7,8,9,10],135, "Income")
final_array = dataMaker(df1,1,2,[4],[3,5,6,7,8,9,10,11])
income_df = pd.DataFrame(data = final_array, columns = final_columns)

#Change dataframe to "Non-Cash Info"

df1 = xls["Non-Cash Info"]
columns = columnGrabber(df1)
sizeChecker(df1,2)
final_columns = columnSplitter(columns,0,[1,2],[3,4,5,6,7,8,9,10], 35, "Non-Cash")
final_array = dataMaker(df1,1,2,[3],[4,5,6,7,8,9,10,11])
non_cash_df = pd.DataFrame(data = final_array, columns = final_columns)

#Change df to "Health Insur"

df1 = xls["Health Insur"]
columns = columnGrabber(df1)
sizeChecker(df1,2)
final_columns = columnSplitter(columns,0,[1,3],[2,4,5,6,7,8], 96, "Health")
final_array = dataMaker(df1,1,2,[4],[3,5,6,7,8,9])
health_df = pd.DataFrame(data = final_array, columns = final_columns)

#Change df to "VI-SPDAT"
df1 = xls["VI-SPDAT"]
columns = columnGrabber(df1)
sizeChecker(df1,2)
t_arr = []
tn_arr = []

#So many columns...
for x in range(3,62):
	t_arr.append(x)
	tn_arr.append(x+1)

final_columns = columnSplitter(columns,0,[1,2],t_arr, 10, "VI-SPDAT")
final_array = dataMaker(df1,1,2,[3],tn_arr)
vispdat_df = pd.DataFrame(data = final_array, columns = final_columns)

#Change df to VI-SPAT v2

df1 = xls["VI-SPAT v2"]
columns = columnGrabber(df1)
sizeChecker(df1,40)

t_arr = []
tn_arr = []
for x in range(1,39):
	t_arr.append(x)
	tn_arr.append(x+1)
t_arr += [41,42,43,44]
tn_arr += [42,43,44,45]

final_columns = columnSplitter(columns,40,[39],t_arr,7,"VI-SPATv2")
final_array = dataMaker(df1,41,40,[],tn_arr)
vispat2_df = pd.DataFrame(data = final_array, columns = final_columns)


#Change df to "Family VI-SPDAT" // 0-index, uid @ 60

df1 = xls["Family VI-SPDAT"]
columns = columnGrabber(df1)
sizeChecker(df1,60)

t_arr = []
tn_arr = []

for x in range(1,59):
	t_arr.append(x)
	tn_arr.append(x+1)
t_arr += [61,62,63,64]
tn_arr += [62,63,64,65]

final_columns =columnSplitter(columns,60,[59],t_arr,3,"Family VI-SPDAT")
final_array = dataMaker(df1,61,60,[],tn_arr)
fam_vispat = pd.DataFrame(data = final_array, columns = final_columns)


#Change df to "Tay VI-SPDAT" // 0-index, uid @ 46

df1 = xls["TAY VI-SPDAT"]
columns = columnGrabber(df1)
sizeChecker(df1,46)

t_arr = []
tn_arr = []

for x in range(1,45):
	t_arr.append(x)
	tn_arr.append(x+1)
t_arr += [47,48,49,50]
tn_arr += [48,49,50,51]

final_columns =columnSplitter(columns,46,[45],t_arr,3,"TAY-SPDAT")
final_array = dataMaker(df1,47,46,[],tn_arr)
tay_vispdat = pd.DataFrame(data = final_array, columns = final_columns)


#Make CSVs
demo_df.to_csv(r'C:/Users/colto/Documents/susan_demo_data.csv', index = False)
disab_df.to_csv(r'C:/Users/colto/Documents/susan_disab_data.csv', index = False)
income_df.to_csv(r'C:/Users/colto/Documents/susan_income_data.csv', index = False)
non_cash_df.to_csv(r'C:/Users/colto/Documents/susan_noncash_data.csv', index = False)
health_df.to_csv(r'C:/Users/colto/Documents/susan_health_data.csv', index = False)
vispdat_df.to_csv(r'C:/Users/colto/Documents/susan_vispdat_data.csv', index = False)
vispat2_df.to_csv(r'C:/Users/colto/Documents/susan_vispdat2v2_data.csv', index = False)
tay_vispdat.to_csv(r'C:/Users/colto/Documents/susan_tay_vispdat_data.csv', index = False)


ee = 'Entry Exit Client Id'

final_df = pd.merge(demo_df, disab_df, left_on='Client Uid', right_on = 'Entry Exit Client Id')
final_df = pd.merge(final_df, non_cash_df, on = ee)
final_df = pd.merge(final_df, health_df, on = ee)
final_df = pd.merge(final_df, vispdat_df, on = ee)
final_df = pd.merge(final_df, vispat2_df, on = ee)
final_df = pd.merge(final_df, fam_vispat, on = ee)
final_df = pd.merge(final_df, tay_vispdat, on = ee)

print(final_df)

final_df.to_csv(r'C:/Users/colto/Documents/susan_final_data.csv', index = False)

