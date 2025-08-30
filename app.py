from flask import Flask ,render_template,redirect,url_for, request, session 
app=Flask(__name__)
app.secret_key="your_key"
from database import get_connection,init_db
from werkzeug.security import check_password_hash,generate_password_hash
import sqlite3 
@app.route('/')
def home():
    result=[]
    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("SELECT * FROM jobs")
    title="Recommend Jobs "
    result=cur.fetchall()
    conn.close()
    return render_template('home.html', result=result, title=title)
 
@app.route('/signup',methods=['GET','POST'])
def signup():
    
    if request.method==   'POST' :
        name=request.form.get('name')
        mobile=request.form.get('mobile')
        email=request.form.get('email')
        password=request.form.get('password')
        hashed_password=generate_password_hash(password)
        try:
            conn=get_connection()
            cur =conn.cursor()
            cur.execute("INSERT INTO user(name,mobile, email, password)VALUES(?,?,?,?)",(name,mobile, email, hashed_password))
            conn.commit()
            return f"user data inserted {name} ,{mobile} successfully"
        except sqlite3.IntegrityError:
            return f"user {name} already exists"
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])                        
def login():
    if request.method=='POST':
        email__or__mobile=request.form.get('email__or__mobile')
       
        password=request.form.get('password')
        print("entered email is ",email__or__mobile)
        print("elnterd pasword is ", password)
        conn=get_connection()
        conn.row_factory = sqlite3.Row
        cur=conn.cursor()
        cur.execute("SELECT id,name,email,mobile, password FROM user WHERE email=? or mobile=?",(email__or__mobile,email__or__mobile))
        result=cur.fetchone()
        conn.close()
        print("database mobile is", result["email"])
        print("saved password is", result["password"])
        if result and check_password_hash(result["password"], password):
          
            user_id=result['id']
            session['user_id']=user_id
            return redirect('/')
        else:
                return f"user not registered"
    return render_template('login.html')
   
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    id= session['user_id']  
    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()             
    cur.execute("SELECT * FROM user WHERE id=?",(id,))
    user=cur.fetchone()
    conn.close()
    return render_template('profile.html',user=user)
    
@app.route('/post_job', methods=['GET','POST'])
def post_job():
    if request.method == "POST":
        if 'user_id' not in session:
            return redirect('/login')
        user_id = session.get("user_id")   # session से login user_id

        # form fields
        title = request.form.get("title")
        department = request.form.get("department")
        company = request.form.get("company")
        location = request.form.get("location")
        work_mode = request.form.get("work_mode")
        job_type = request.form.get("job_type")
        experience = request.form.get("experience")
        salary_min = request.form.get("salary_min")
        salary_max = request.form.get("salary_max")
        currency = request.form.get("currency")
        description = request.form.get("description")
        responsibilities = request.form.get("responsibilities")
        requirements = request.form.get("requirements")
        skills = request.form.get("skills")
        apply_url = request.form.get("apply_url")
        apply_email = request.form.get("apply_email")
        deadline = request.form.get("deadline")
        logo = request.form.get("logo")
        visa_supported = 1 if request.form.get("visa_supported") else 0
        urgent = 1 if request.form.get("urgent") else 0
        disability_friendly = 1 if request.form.get("disability_friendly") else 0
  
        try:
            conn=get_connection()
            cur=conn.cursor()
            cur.execute("INSERT INTO jobs(user_id, title, department, company, location, work_mode, job_type, experience,salary_min, salary_max, currency, description, responsibilities, requirements,skills, apply_url, apply_email, deadline, logo, visa_supported, urgent,disability_friendly) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, title, department, company, location, work_mode, job_type, experience,
              salary_min, salary_max, currency, description, responsibilities, requirements,
              skills, apply_url, apply_email, deadline, logo, visa_supported, urgent,
              disability_friendly))
            conn.commit()
               
        except sqlite3.IntegrityError:
            return f"user data is unsaved"
        except Exception as e:
            return f"unexpected {e}"
        finally:
            conn.close()
        return redirect('/')
    return render_template('post_job.html')
@app.route('/show_jobs')
def show_jobs():
    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()          
    cur.execute("SELECT * FROM jobs") 
    alljobs=cur.fetchall()
    return render_template('show_jobs.html',alljobs=alljobs)
    
@app.route('/search',methods=['GET','POST'])    
def search():
    result=[]
    if request.method== 'POST':
          
        title=request.form.get('query')
        conn=get_connection()
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("SELECT * FROM jobs WHERE title LIKE ?",('%'+title +'%',))
        title= "Search Results"
        result=cur.fetchall()
    return render_template('home.html',result=result, title=title)
    
from flask import  jsonify

@app.route('/suggest')
def suggest():
    q = request.args.get('query', '').strip()
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT title FROM jobs WHERE title LIKE ? LIMIT 5", ('%' + q + '%',))
    rows = cur.fetchall()
    conn.close()
    suggestions = [r['title'] for r in rows]   # Row को dict की तरह access करना
    return jsonify(suggestions)
    
@app.route('/chat', methods=['GET','POST'])    
def chat():
    return render_template('chat.html')
@app.route('/forgot', methods=['GET','POST']) 
def forgot():
    if request.method=='POST':
        name=request.form.get('name')
        mobile=request.form.get('mobile')
        email=request.form.get('email')
        password=request.form.get('password')
        conn=get_connection()
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()
        cur.execute("SELECT name,mobile, email FROM user WHERE name =? and mobile=? and email=?",(name, mobile, email))
        result=cur.fetchone()
        if result['name'] == name and result['email']==email and result['mobile']==mobile  :
            hash_password=generate_password_hash(password)
            cur.execute("UPDATE user SET password =? WHERE mobile =?",(hash_password, mobile))
            conn.commit()
            
            return redirect('/login')
        else:
            return f"Dear User Credentials Enterd by You {name} , {mobile}, {email} is invalid"
         
    return render_template('forgot.html')
@app.route('/reset', methods=['GET','POST'])    
def reset():
    if request.method=='POST':
        mobile=request.form.get('mobile')
        current_password=request.form.get('password')
        new_password=request.form.get('new_password')
        confirm_password=request.form.get('confirm_password')
        hashes_password=generate_password_hash(new_password)
        if new_password == confirm_password:
            conn=get_connection()
            conn.row_factory=sqlite3.Row
            cur=conn.cursor()
            cur.execute("SELECT password,mobile FROM user WHERE  mobile=?",(mobile,))
            result=cur.fetchone()
            if mobile == result['mobile'] and check_password_hash(result['password'], current_password):
                cur.execute("UPDATE user SET password=? WHERE mobile=? ",(hashes_password,mobile))
                conn.commit()
                conn.close()
                return redirect('/login')
            else:
                return f"hey Dear User credentials is invalid"
        else:
            return "new password and confirm password mismatch "
    return render_template('reset.html')     
if __name__==('__main__') :
    app.run(debug=True)