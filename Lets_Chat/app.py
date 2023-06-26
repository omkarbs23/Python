# s
from flask import *
from db import *

app = Flask(__name__)
app.secret_key = "Welcome1?"

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")

        # print(fname,lname,email,password)
        query = f"insert into users (first_name,last_name,email,password) values ('{fname}','{lname}','{email}','{password}')"
        universal_function(query)

        msg1 = f" Welcome {fname} {lname}"
        msg2 = "We hope you would like our services ...! "

        query1 = f"insert into messages (sender,reciever,msg) values ('LetsChat','{email}','{msg1}') "
        universal_function(query1)

        query2 = f"insert into messages (sender,reciever,msg) values ('LetsChat','{email}','{msg2}') "
        universal_function(query2)

        session['user'] = email

        return redirect("/dashboard?person_1=LetsChat")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    # email = session['user']
    # msg = f"select * from messages where (sender = {session['user']} or reciever = {session['user']})"
    # data = universal_function(msg,1)

    if ('user' in session):
# 1
# creating a contact list which should be shown in left panel --------------- start
        contact = f"select sender,reciever from messages where (sender = '{session['user']}' or reciever = '{session['user']}' ) order by date DESC"
        data = universal_function(contact,1)
        contact_list = []
        for i in data:
            for j in i:
                contact_list.append(j)
        contact_list = list(dict.fromkeys(contact_list))
        contact_list.remove(session['user'])
# creating a contact list which should be shown in left panel --------------------end

# 2
# creating a msg list which should be shown in righ panel --------------- start
        person_1 = request.args.get('person_1')
        session['reciever'] = person_1
        # print(person_1)
        person_2 = session['user']
        msg = f"select sender,reciever,msg,date,id from messages where (sender = '{session['user']}' or reciever = '{session['user']}' ) order by date"
        data1 = universal_function(msg,1)
        msg = []
        for i in data1:
            if( (i[0]== person_1 and i[1]==person_2) or (i[1]== person_1 and i[0]==person_2)): 
                    msg.append(i)
# creating a msg list which should be shown in righ panel --------------- end

# 3
# Creating a list of email of all users for adding a new user to check wweater a new user you want to communicate with is already existing in the db-------------- start
        users = f"select email from users"
        data2 = universal_function(users,1)
        users = []
        for i in data2:
            for j in i:
                users.append(j)
        session['all_user_email'] = users
        # print(session['all_user_email'])
# Creating a list of email of all users -------------- end



        return render_template("dashboard.html",contacts = contact_list, message = msg)

# if user user not in session
    elif (request.method == "POST"):

        uname = request.form["uname"]
        password = request.form["password"]

        query = f"select email,password from users"
        data = universal_function(query,1)
        t=(uname,password)

        if(t in data):
            session['user'] = uname
            return redirect("/dashboard")

    else:    
        return redirect("/")


# getting msg from an logged in user
@app.route("/send_msg",methods=["GET","POST"])
def send_msg():
    if request.method == "POST":
        msg_body = request.form.get("data")
        # print(msg_body)
        # print(session['reciever'])
        if (session['reciever'] != "None"):
            query = f"insert into messages (sender,reciever,msg) values ('{session['user']}','{session['reciever']}','{msg_body}') "
            universal_function(query)
    return redirect(f"/dashboard?person_1={session['reciever']}")


# getting msg for a new user
@app.route("/modal_msg",methods=["GET","POST"])
def modal_msg():
    if request.method == "POST":
        recipient = request.form.get("rec")
        msg_body = request.form.get("msg")

        # print(msg_body)
        # print(recipient)

        if (recipient in session['all_user_email']):
            if (recipient != "None" and msg_body != "None"):
                query = f"insert into messages (sender,reciever,msg) values ('{session['user']}','{recipient}','{msg_body}') "
                universal_function(query)
    return redirect(f"/dashboard?person_1={recipient}")


# delete a msg
@app.route("/delete_msg",methods=['GET','POST'])
def delete_msg():
    if request.method == "POST":
        sender_id = request.form.get("sender")
        # print(sender_id)
        if (sender_id != None):
            query = f"delete from messages where id={sender_id} "
            universal_function(query)
    return redirect(f"/dashboard?person_1={session['reciever']}")









if (__name__ == "__main__"):
    app.run(debug=True)