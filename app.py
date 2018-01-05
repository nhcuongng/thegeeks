from flask import *
import mlab
from mongoengine import *
from user import User
from tree import Tree
from answer import Answers
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = "Csb~a J]?E3z_mx"
mlab.connect()


@app.route('/')
def index():
    trees = Tree.objects()
    return render_template('index.html', trees = trees)

@app.route('/signup',methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password1 = form['password1']
        password2 = form['password2']
        user = User.objects(username = username).first()
        if user is None and password1 == password2:
            new_user = User(username=username, password=password1, tree_id = "")
            new_user.save()
            flash("Đăng ký Thành công")
            return redirect(url_for('signin'))
        elif password1 != password2:
            flash('Mật Khẩu Không Khớp, vui lòng nhập lại')
            return render_template('signup.html',username = username)
        else:
            flash("Đã tồn tại")
            return render_template('signup.html')

@app.route('/signin',methods = ['GET', 'POST'])
def signin():
    user = User.objects()
    if request.method == 'GET':
        return render_template('signin.html')
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password = form['password']
        user = User.objects(username = username).first()
        if user is None:
            flash('Username không tồn tại')
            return render_template('/signin.html')
        elif user.password != password:
                flash('Password không tồn tại')
                return render_template('/signin.html')
        else:
            session['loggedin'] = True
            session['username'] = username #lưu lại user đã đăng nhập
            return redirect(url_for("index"))
@app.route('/create_tree', methods = ['GET', 'POST'])
def create_tree():
    if session.get('loggedin', False):
        if request.method == "GET" :
            return render_template('create_tree.html')
        elif request.method == "POST" :
            form = request.form
            code = form['code']
            password = form['password']
            username = session['username']
            # images = Image.objects()
            # image = choice(images)
            user = User.objects(username = username).first()
            check_tree = Tree.objects(code = code).first()
            if user.tree_id:
                flash("Bạn Hiện Tại Không Thể tạo nhóm,nếu muốn tạo hay thoát khỏi nhóm hiện tại")
                return render_template('create_tree.html')
            else:
                if check_tree is None:
                    new_tree = Tree(code=code, password=password, owners = [username], point = 0)
                    new_tree.save()
                    flash("Tạo Cây Thành công, mời bạn đăng nhập lại vào cây vừa tạo")
                    return redirect(url_for('signin_to_tree'))
                else:
                    flash("Tên cây đã được sử dụng")
                    return redirect(url_for('create_tree'))
    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session['loggedin'] = False
    flash('Bạn có muốn Đăng nhập lại không?')
    flash('Bạn Muốn Đăng nhập lại không?')
    return redirect(url_for('signin'))


@app.route('/signin_to_tree', methods = ['GET', 'POST'])
def signin_to_tree():
    if session.get('loggedin', False): # người dùng phải đăng nhập
        if request.method == "GET" :
            return render_template('signin_to_tree.html')
        elif request.method == 'POST':
            form = request.form
            code = form['code']
            password = form['password']
            username = session['username']
            user = User.objects(username = username).first() # trả về 1 object
            tree = Tree.objects(code = code, password = password).first() # trả về 1 objects
            if tree is None:
                flash("Cây Không tồn tại")
                return render_template('signin_to_tree.html')
            elif tree.password != password:
                flash("Sai mật khẩu")
                return render_template('signin_to_tree.html')
            else:
                if user.tree_id:
                    flash("Bạn đã Nằm Trong nhóm khác rồi")
                    return render_template('signin_to_tree.html')
                else:
                    flash("Đăng Nhập Thành Công, bạn hãy tạo câu hỏi đầu tiên")
                    tree.update(push__owners = user)
                    user.update(tree_id = str(tree.id), code = code) #khi mà họ join vào,lưu cả code của cây, trường tree_id trong user cũng sẽ được update, note: tree_id phải đc ép sang str
                    return redirect(url_for('create_question'))
    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin')) # bắt họ sign in nếu chưa sigin


@app.route('/create_question', methods = ['GET', 'POST'])
def create_question():
    if session.get('loggedin', False):
        username = session['username'] # lấy thông tin mà user trên đăng nhập
        user = User.objects(username = username).first()
        tree = Tree.objects(code = user.code).first()# trả về 1 object với code phải bằng code cây đã tạo trc đó
        if request.method == 'GET':
            return render_template('create_question.html', username = username, code = user.code)
        elif request.method == 'POST':
            form = request.form
            #lưu câu trả lời và đáp án
            question = form['question']
            answer1 = form['answer1']
            answer2 = form['answer2']
            answer3 = form['answer3']
            answer4 = form['answer4']
            right_answer = form['right_answer']
            #Lưu cả Người đặt ra câu trả lời, đồng thười lưu id của nhóm
            new_answer = Answers(answer1 = answer1,
                                answer2 = answer2,
                                answer3 = answer3,
                                answer4 = answer4,
                                right_answer = right_answer,
                                username = username,
                                question = question, tree_id = str(user.tree_id) )
            new_answer.save()
            flash('Tạo câu hỏi thành công')
            return redirect(url_for('my_tree'))

    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin'))

@app.route('/show_question', methods = ['GET', 'POST'])
def show_question():
    if session.get('loggedin', False):
        username = session['username']
        user = User.objects(username = username).first() # user đang đăng nhập vào
        tree = Tree.objects().with_id(user.tree_id)
        questions = Answers.objects(tree_id = user.tree_id)
        if not questions:
            flash("Hiện Tại chưa có câu hỏi nào,mời bạn tạo mới")
            return redirect(url_for('create_question'))
        else:
            if tree is not None:
                question = choice(questions)
                if request.method == 'GET':
                    if username != question.username:
                        return render_template('show_question.html',username = username, question = question,code = user.code)
                    else:
                        flash("Nếu nhóm chỉ có 1-3 thành viên thì hãy add thêm,nếu không vui lòng click lại")
                        return redirect(url_for('my_tree'))
                elif request.method == 'POST':
                    form = request.form
                    values = form['values'] #lấy id từ form input (từ lần get)
                    get_question = Answers.objects().with_id(values) #(lấy question theo id ở trên)
                    right_answer = form['right_answer']
                    if get_question.right_answer == right_answer: # so sánh với người dùng nhập
                        points_tree_update = tree.point + 1 # lấy điểm trên database + 1 gán vào biến
                        tree.update( point = str(points_tree_update)) # convert sang string rồi update
                        flash('Bạn Đã Đúng và được cộng 1 điểm')
                        return redirect(url_for('my_tree'))
                    else:
                        points_tree_update = tree.point - 1 # lấy điểm trên database - 1 gán vào biến
                        tree.update( point = str(points_tree_update))
                        flash('Bạn Đã Sai và "được" trừ 1 điểm')
                        return redirect(url_for('my_tree'))
            else:
                return redirect(url_for('signin_to_tree'))

    else:
        return redirect(url_for('my_tree'))

@app.route('/my_tree/')
def my_tree():
    if session.get('loggedin', False):
        username = session['username']
        user = User.objects(username = username).first()
        if user.tree_id is '':
            flash("Bạn chưa có cây cho riêng mình")
            return redirect(url_for('create_tree'))
        else:
            tree = Tree.objects().with_id(user.tree_id)
            if tree is not None:
                return render_template('my_tree.html', tree = tree, point = tree.point, code = user.code, username = username)
            else:
                return redirect(url_for('signin_to_tree'))
    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin'))

@app.route('/edit_question', methods = ['GET', 'POST'])
def edit_question():
    if session.get('loggedin', False):
        username = session['username']
        answer = Answers.objects(username = username).first()
        if answer is None:
            flash('Bạn chưa tạo câu hỏi mới')
            return redirect(url_for('create_question'))
        else:
            if request.method == 'GET':
                return render_template('edit_question.html', answer = answer)
            elif request.method == 'POST':
                form = request.form
                question = form['question']
                answer1 = form['answer1']
                answer2 = form['answer2']
                answer3 = form['answer3']
                answer4 = form['answer4']
                right_answer = form['right_answer']
                answer.update(answer1 = answer1,
                              answer2 = answer2,
                              answer3 = answer3,
                              answer4 = answer4,
                              right_answer = right_answer,
                              question = question)
                flash('Đã Sửa Thành công')
                return render_template('edit_question.html', answer = answer)
    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin'))

@app.route('/del_question', methods = ['GET', 'POST'])
def del_question():
    if session.get('loggedin', False):
        username = session['username']
        answer = Answers.objects(username = username).first()
        if answer is None:
            flash('Bạn chưa tạo câu hỏi mới')
            return redirect(url_for('create_question'))
        else:
            if request.method == 'GET':
                return render_template('del_question.html',answer = answer)
            elif request.method == 'POST':
                answer.delete()
                flash('Xóa Thành Công')
                return redirect(url_for('my_tree'))
    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin'))
@app.route('/exit_tree')
def exit_tree():
    if session.get('loggedin', False):
        username = session['username']
        user = User.objects(username = username).first()
        tree = Tree.objects().with_id(user.tree_id)
        answer = Answers.objects(username = username).first()
        tree.update(pull__owners = user)
        user.update(tree_id ='',code ='')
        answer.delete()
        flash("Thoát Nhóm thành công")
        return redirect(url_for('signin_to_tree'))
    else:
        flash('Bạn Chưa Đăng Nhập')
        return redirect(url_for('signin'))

if __name__ == '__main__':
  app.run(debug=True)
