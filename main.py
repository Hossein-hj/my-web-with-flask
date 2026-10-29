from flask import Flask, render_template, session, redirect,request
from database import *
from datetime import timedelta



app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.secret_key ="ijgspjdpfjrpsjg mmmmm dddd eeee ppppp 444 5okdpkpskfdsmc"

app.config['MONGO_URI'] ='mongodb://localhost:27017/blog'
init_db(app)

 
@app.route("/")
def index():
    posts = get_posts()
    print(posts)
    return render_template('index.html',posts = posts)




@app.route("/login" , methods = ['GET' , 'POST'])
def login():
    myuser = 'admin'
    mypass = '11'
    if request.method == 'POST':
        if myuser == request.form['username'] and mypass == request.form['password']:
            session['admin'] = True
            session['user'] = 'administrator'
            return redirect('/')
        return render_template('login.html',errormsg ='invalid Username or Password')
    return render_template('login.html',errormsg ='')

@app.route("/logout")
def logout():
    session.pop('admin')
    session.pop('user')
    return redirect('/')


@app.route("/newpost" , methods = ['GET' , 'POST'])
def create_post():
    import os
    import time
    if 'admin' not in session:
        return redirect('/login')
        
    if request.method =='POST':
        title = request.form['title']
        content = request.form['description']
        image = None

        
        if 'img' in request.files and request.files['img'].filename !='':
            
            file = request.files['img']
            file_name = f"{int(time.time())}_{file.filename}"
            file_path = os.path.join(app.root_path,'static','uploads',file_name)
            file.save(file_path)
            print(request.files['img'].filename , file_path)
            image = file_name
        else:
            image = "nopic.png"

        add_post(title,content,image)

        return redirect("/")
    return render_template('newpost.html')


@app.route('/edit_post/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    if 'admin' not in session:
        return redirect('/login')
    post = get_post_by_id(post_id)
    if request.method =='POST':
        updated_title = request.form['title']
        updated_content = request.form['content']
        update_post(post_id = post_id, title=updated_title ,content=updated_content)
        return redirect('/')
        
    return render_template('edit_post.html', post=post)           




@app.route('/delete_post/<int:post_id>', methods=['GET','POST'])
def delete_post(post_id):
    if 'admin' not in session:
        return redirect('/login')
    success = delete_post_from_db(post_id)
    if success:
        return redirect("/")
    return "post not found" , 404


# -----------comments----------


@app.route('/view_comments/<int:post_id>', methods=['GET', 'POST'])
def view_comments(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    is_admin = session.get('admin', False)
    if request.method == 'POST':
        if not is_admin:
            author = request.form['author'] 
           
            text = request.form['text']
            add_comment(post_id, author, text)
            return redirect(f'/view_comments/{post_id}')
    
    comments = post.get("comments", [])
    if not is_admin:
        comments = [comment for comment in comments if comment.get("is_active", False)]
    
    return render_template(
        'comments.html' , 
        post = post ,
        comments = comments ,
        is_admin=is_admin
    )



@app.route('/toggle_comment/<int:post_id>/<int:comment_index>', methods=['POST']) 
def toggle_comment(post_id   , comment_index):
    if 'admin' not in session:
        return redirect('/login')
    
    success = update_comment_status(post_id, comment_index)
    
    if not success:
        return "Comment not found or invalid index", 404
    
    
    return redirect(f'/view_comments/{post_id}')
   




@app.route('/delete_comment/<int:post_id>/<int:comment_index>', methods=['POST'])
def delete_comment(post_id, comment_index):
    if 'admin' not in session:
            return redirect('/login')
    success = delete_comment_from_db(post_id, comment_index)
    if not success:
        return "Comment not found or invalid index", 404
    return redirect(f'/view_comments/{post_id}')




    

if __name__ == "__main__":
    app.run(debug=True)
