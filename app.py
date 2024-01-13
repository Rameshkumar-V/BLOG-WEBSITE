from flask import Flask,render_template,request,jsonify,redirect,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from database import (
	db,
	add_document,
	create_documents_table,
	get_document_details_all,
	delete_document,
	email_store_db,
	email_data_db_allget,
	get_document_details,
	get_document,email_del_by_id
)
from io import BytesIO


app=Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rameshkumar@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

  # Disable Flask-SQLAlchemy modification tracking


# 1 HOME PAGE
@app.route('/')
@app.route('/home')

def Home():
	return render_template("home.html")

# HOME PAGE END


# 2 ABOUT PAGE
@app.route('/about')

def About():
	return render_template("about.html")

# ABOUT PAGE END


# 3 PROFESSIONAL ACTS PAGE
@app.route('/professionalacts')

def Profession_acts():
	return "P. acts page"

# PROFESSIONAL ACTS PAGE end

# 4 LEARNING RESROUCES PAGE
@app.route('/learningresources')

def Learning_Resources():
	document_details=get_document_details("PUBLICATION")
	if document_details:
		return render_template("resource.html",document_details=document_details)

	else:
		return "failed"
# LEARNING RESROUCES PAGE end

# 5 ENGLISH ESSAY
@app.route('/essay')
def Essay():
	return "Essary page"

# ENGLISH ESSAY end


# 6 PUBLICATION
@app.route('/publications')
def Publication():
	document_details=get_document_details("RESOURCES")
	if document_details:
		return render_template("publication.html",document_details=document_details)

	#return render_template("publication.html")
# PUBLICATION end

# 7 CONTACT
@app.route('/contact')
def Contact():
	return render_template("contact.html")


# DATABASE OPERATIONS 
# ADMIN PAGE SENDING

@app.route('/admin')
def Admin():
	return render_template('adminpannel_login.html')


# SECURITY FUNCTION FOR ADMIN

@app.route('/adminsecurity',methods=['POST'])
def Admin_password():

	if request.method=='POST':
		try:
			username=str(request.form['username'])
			password=str(request.form['password'])

			if username=='rkking' and password=='rkking1234':
				return redirect(url_for('upload_documnent_page'))
			else:
				return jsonify('Password Incorrect')
		except Exception as e:
			return f'{e}'





@app.route('/uploaddoc',methods=['GET'])

def upload_documnent_page():
	return render_template('ap_interface.html')




# learning resources page getting binary datg to send file.
@app.route('/getfile/<int:id>', methods=['GET'])
def get_file(id):
    print("id is:", id)
    document = get_document(id)
    if document:
    	file_data = BytesIO(document['ddata'])
    	return send_file(
    		file_data,
    		as_attachment=True,
    		mimetype='application/pdf',
    		download_name=str(document['dname'])
    		)
    else:
    	abort(404)

# DOCUMENT DELETE PAGE.




@app.route('/docdelete',methods=['GET'])

def doc_del_page():

	if request.method=='GET':
		document_details=get_document_details_all()
		print("doc details = ",document_details)
		if document_details:
			#[{"document_id":1,"document_name":"NAME OF DOCUMENT"}]
			return render_template('ap_delete_i.html',document_details=document_details)
		else:
			document_details=[{"document_id":None,"document_name":"NAME OF DOCUMENT"}]

			return render_template('ap_delete_i.html',document_details=document_details)



	
# DELETE A DOCUMENT WITH THEIR DOC ID
@app.route('/deldoc',methods=["POST"])

def del_publication():

	if request.method=='POST':
		try:
			document_id=int(request.args.get('docid'))
			result=delete_document(document_id)
			print("result is : ",result)

			if result:
				#"DELETED"
				return jsonify({"result":result})
			else:
				#"UN DELETED"
				return jsonify({"result":str(result)})


			
		except Exception as e:
			result=f"ERROR {type(e)}"
			return jsonify({"result":str(result)})
	else:
		return jsonify("INVALID METHOD")




# UPLOAD DOCUMENT S DATAS COLLECT AREA.

@app.route('/upldoc',methods=["POST"])

def Upload_doc():
	if request.method=='POST':
		try:
			if 'document' in request.files:
				document=request.files['document']
				image=request.files['image']
				section=request.form['section']

				if document:
					

					doc_blob_data=document.read()
					img_blob_data=image.read()
					doc_name=str(document.filename)
					doc_sec=str(section)
					result=add_document(dname=str(doc_name),ddata=doc_blob_data, dimage=img_blob_data, dtype=str(doc_sec))

					if result:
						print({"result":result})
						#"UPLOADED"
						return jsonify({"result":result})
					else:
						print("un unloaded")
						return jsonify({"result":result})




			else:
				return jsonify("FILE NOT FOUND")

		except Exception as e:

			return jsonify(f"ERROR :  {e}")
	else:

		return jsonify("wrong method")



# FOR EMAIL ADDRESS GETTER and store to database

@app.route('/email',methods=["POST"])

def email_db_store():
	if request.method=="POST":
		try:
			emailid=request.args.get('emailid')
			message=request.args.get('message')
			print("emailidl=",emailid)
			print("msg=",message)
			result= email_store_db(emailid,message)
			if result:
				return jsonify({"result":f"MESSAGE SENDED"})
			else:
				return jsonify({"result":f"MESSAGE SENDEDING ISSUE !"})



		except Exception as e:
			return jsonify({"result":f"{type(e).__name__}"})
	else:
		return "Invalid Method !"


@app.route('/emaildetails',methods=["GET"])

def get_emails():
	if request.method=='GET':
		try:
			result=email_data_db_allget()
			print("result: ",result)
			if result:
				return render_template("admin_user_msg.html",result=result)
			else:
				return jsonify({"result":f"ISSUE !"})
		except Exception as e:
			return jsonify({"result":f"{type(e).__name__}"})
	else:
		return "Invalid Method !"


# EMAIL DELETE FUNCTION
@app.route('/emaildelete/<int:id>',methods=["POST"])
def Delete_email(id):

	if request.method=='POST':
		try:
			document_id=int(id)
			result=email_del_by_id(document_id)
			print("result is : ",result)

			if result:
				#"DELETED"
				return jsonify({"result":result})
			else:
				#"UN DELETED"
				return jsonify({"result":str(result)})


			
		except Exception as e:
			result=f"ERROR {type(e)}"
			return jsonify({"result":str(result)})
	else:
		return jsonify("INVALID METHOD")


# This for redirect email to a person.
@app.route('/compose_email/<emailid>')
def compose_email(emailid):
    # Add your logic here to retrieve additional data or perform any necessary processing
    subject = "Subject of the email"
    body = "Body of the email"

    # Redirect to the Gmail compose URL with the pre-filled data
    return redirect(f"https://mail.google.com/mail/?view=cm&fs=1&to={emailid}&su={subject}&body={body}")


if __name__=='__main__':
	create_documents_table()
	app.run(debug=True)



