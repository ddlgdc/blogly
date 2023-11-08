from flask import Flask, request, redirect, render_template
from sqlalchemy import inspect
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blogly.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'Not-A-Secret'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

db.app = app
db.init_app(app)

with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table(User.__tablename__):
        db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_of_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users_list.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user():
    return render_template('new_user.html')\
    
@app.route("/users/new", methods=["POST"])
def new_user_submitted():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

if __name__ == '__main__':
    app.run(debug=True, port=0)