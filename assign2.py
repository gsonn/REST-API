from flask import Flask, jsonify,abort
import  csv
import time
import hashlib
import re
from flask import make_response
import datetime
from flask import request

app=Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}),404)

#list all categories
@app.route('/api/v1/categories',methods=['GET'])
def list_cat():
    list={}
    with open('categories.csv') as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            list[row[0]]=int(row[1])
    return jsonify(list)

#list all get_users
@app.route('/api/v1/users',methods=['GET'])
def list_all_users():
    users=[]
    with open('users.csv') as csv_file:
        csv_reader=csv.reader(csv_file)
        for row in csv_reader:
            users.append(row[0])
    return jsonify(users)

#2 Add a category
from flask import request
@app.route('/api/v1/categories',methods=['POST'])
def add_cat():
	if not request.json :
		abort(400)
	data=request.json
	aa=len(data)
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==data[0]):
				flag=1
			if(flag==1):
				return make_response(jsonify({}),400)
	if(aa>1):
		return make_response(jsonify({}),400)
	with open('categories.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=[data[0],0]
		writer.writerow(r)
	return jsonify({}), 201



#delete category
@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])
def delete_cat(categoryName):
    with open('categories.csv') as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        delete_flag=0
        for row in csv_reader:
            if(row[0]==categoryName):
                delete_flag=1
        if(delete_flag==0):
            return make_response(jsonify({'Error': ' Resource does not exist'}),400)
    list=[]
    with open('categories.csv','rb') as file:
        reader=csv.reader(file)
        #list1=list(reader)
        #print(list1)
        for line in reader:
            if(line[0]!=categoryName):
                list.append(line)
    print(list)
    with open("categories.csv", "wb") as f:
        writer=csv.writer(f)
        writer.writerows(list)
    return jsonify({}), 200

#add users
@app.route('/api/v1/users',methods=['POST'])
def adde_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    data=request.json
    cred={'username':data['username'],'password':data['password']}
    print(data)
    with open('users.csv') as users:
        user_reader=csv.reader(users,delimiter=',')
        user_flag=0
        for row in user_reader:
            if(row[0]==cred['username']):
                user_flag=1
            if(user_flag==1):
                return make_response(jsonify(),400)
    pass_hash=cred['password']
    pattern=re.compile(r'\b[0-9a-f]{40}\b')
    match=re.match(pattern,pass_hash)
    flag=0
    try:
        if(match.group(0)==pass_hash):
            flag=1
    except:
        pass
    if(flag==1):
        with open('users.csv','a') as csv_file:
            writer=csv.writer(csv_file)
            appe=[cred["username"],cred["password"]]
            writer.writerow(appe)
        return jsonify({}),201
    else:
        return jsonify(),400
#5 Delete a user
@app.route('/api/v1/users/<username>', methods=['DELETE'])
def delete_user(username):
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==username):
				flag=1
		if(flag==0):
			return make_response(jsonify(),400)
	tl=[]
	with open('users.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=username):
				tl.append(line)
	print(tl)
	with open("users.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	return jsonify({}), 200


#11 Add and act
@app.route('/api/v1/acts',methods=['POST'])
def add_act():
	if not request.json or not 'actId' in request.json or not 'username' or not 'timestamp' in request.json or not 'caption' in request.json or not 'imgB64' in request.json or not 'categoryName' in request.json:
		abort(400)
	d=[]
	actId=request.json['actId']
	category=request.json['categoryName']
	username=request.json['username']
	timestamp=request.json['timestamp']
	caption=request.json['caption']
	base64=request.json['imgB64']
	upvote=0
	try:
		datetime.datetime.strptime(timestamp, '%d-%m-%Y:%S-%M-%H')
		#print("valid")
	except ValueError:
		return make_response(jsonify(timestamp),400)
	d.append(actId)
	d.append(category)
	d.append(username)
	d.append(timestamp)
	d.append(caption)
	d.append(upvote)
	d.append(base64)
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(int(row[0])==int(d[0])):
				flag=1
			if(flag==1):
				return make_response(jsonify(),400)
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[2]==d[2]):
				flag=1
			if(flag==1):
				return make_response(jsonify(),400)
	data=category
	ll1=[]
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(row[0]==data):
			flag=1
		if(flag==1):
			row[1]=int(row[1])+1
	if(flag==0):
		return make_response(jsonify(flag),400)
	with open('categories.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()


	with open('acts.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=d
		writer.writerow(r)
	return jsonify({}), 201


#10 Remove an act
@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
	category="temp"
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==actId):
				flag=1
				category=row[1]
		if(flag==0):
			return make_response(jsonify(),400)
	tl=[]
	with open('acts.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=actId):
				tl.append(line)
	#print(tl)
	with open("acts.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	data=category
	ll1=[]
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(row[0]==data):
			flag=1
		if(flag==1):
			row[1]=int(row[1])-1
	if(flag==0):
		return make_response(jsonify(flag),400)
	with open('categories.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()
	return make_response(jsonify({}), 200)

#9 upvote an act
@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote_act():
	if not request.json :
		abort(400)
	data=request.json
	data=int(data[0])
	ll1=[]
	with open('acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(int(row[0])==data):
			flag=1
		if(flag==1):
			row[5]=int(row[5])+1
	if(flag==0):
		return make_response(jsonify(flag),400)
	with open('acts.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)
	csvFile.close()
	return make_response(jsonify(flag),200)


#6 List acts for a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def list_acts_cat(categoryname):
	ll=[]
	with open('acts.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
	for line in l:
		details={}
		if(line[1]==categoryname):
			details["actId"]=int(line[0])
			details["category"]=line[1]
			details["username"]=line[2]
			details["timestamp"]=line[3]
			details["caption"]=line[4]
			details["upvotes"]=int(line[5])
			details["imgB64"]=line[6]
			ll.append(details)
	if(len(ll)>500):
		return make_response(jsonify({}),400)
	if(len(ll)==0):
		return make_response(jsonify({}),204)
	return make_response(jsonify(ll),200)


#7 list number of acts in a given category
@app.route('/api/v1/categories/<categoryname>/acts/size', methods=['GET'])
def list_num_acts_cat(categoryname):
	with open('categories.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==categoryname):
				flag=1
			if(flag==1):
				return make_response(jsonify([row[1]]),200)


	return make_response(jsonify({}),204)

#8 Acts in range of a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def list_acts_cat_range(categoryname,start,end):
	ll=[]
	start=int(request.args.get('start'))
	end=int(request.args.get('end'))
	with open('acts.csv', 'rb') as f:
		next(f)
		reader = csv.reader(f)
		l = list(reader)
	for line in l:
		if(line[1]==categoryname):
			ll.append(line)
	ll.sort(key=lambda x: x[3][12])
	ll.sort(key=lambda x: x[3][11])
	ll.sort(key=lambda x: x[3][15])
	ll.sort(key=lambda x: x[3][14])
	ll.sort(key=lambda x: x[3][18])
	ll.sort(key=lambda x: x[3][17])
	ll.sort(key=lambda x: x[3][0])
	ll.sort(key=lambda x: x[3][1])
	ll.sort(key=lambda x: x[3][3])
	ll.sort(key=lambda x: x[3][4])
	ll.sort(key=lambda x: x[3][3])
	ll.sort(key=lambda x: x[3][9])
	ll.sort(key=lambda x: x[3][8])
	ll.sort(key=lambda x: x[3][7])
	ll.sort(key=lambda x: x[3][6])
	ll.reverse()
	a=end-start+1
	#if(a>500):
	return make_response(jsonify({start}),200)















if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)
