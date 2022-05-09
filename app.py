from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()


"""
User routes
"""
@app.route('/')
def home():
    """Redirect to Register route"""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """
    Check if user is in the session
    If not - Show registration form and register a new user on form submission
    If user in the session, redirect to user's page
    """
    if "username" in session:
        return redirect(f"users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already in use')
            return render_template('register.html', form=form)

        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('Email address already taken')
            return render_template('register.html', form=form)


        session['username'] = new_user.username
        flash ('Welcome! Successfully created your account!', "success")

        return redirect(f'/users/{session["username"]}')

    else:
        return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Show login form and handle form submission"""

    if "username" in session:
        return redirect(f"users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f'Welcome back {user.first_name} {user.last_name}!', "primary")

            session['username'] = user.username
            return redirect(f"/users/{user.username}")

        else:
            flash("invalid username or password. Please try again", "danger")
            form.username.errors = ['Invalid username or password']

    return render_template('login.html', form=form)



@app.route('/users/<username>')
def show_user(username):
    """
    Show user's page if user is logged in
    If no user in the session, returns to register page
    """

    if username != session['username'] or "username" not in session:
        # flash('Sorry, you are not authorized to view that page')
        return redirect('/')
    form = DeleteForm()
    user = User.query.get(username)

    return render_template('show_user.html', user=user, form=form)



@app.route('/logout')
def logout_user():
    """Log out current user in session"""

    session.pop('username')
    flash('Goodbye!', 'info')
    return redirect('/')



@app.route('/users/<username>/delete', methods=["GET", "POST"])
def delete_user(username):
    """Delete current user in session"""

    user = User.query.get_or_404(username)
        
    if username != session['username'] or "username" not in session:
        # flash('Sorry, you are not authorized to view that page')
        return redirect('/')
        
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

    flash("User Deleted!", "info")
    return redirect('/')




"""
Feedback routes
"""
@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """
    Shows add feedback form and handles form submission for current user
    """

    if username != session['username'] or "username" not in session:
        # flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    form = FeedbackForm()
    user = User.query.get(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=session["username"])

        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{session["username"]}')

    return render_template('feedback/add_feedback.html', user=user, form=form)



@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """
    Shows update feedback form and handles form submission for selected feedback
    """

    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)


    if feedback.username != session['username'] or "username" not in session:
        # flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f'/users/{session["username"]}')

    return render_template('feedback/update_feedback.html', form=form, feedback=feedback)




@app.route('/feedback/<int:feedback_id>/delete', methods=["GET", "POST"])
def delete_feedback(feedback_id):
    """Deletes selected feedback from current user in session"""

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
        
    if feedback.username != session['username'] or "username" not in session:
        # flash('Sorry, you are not authorized to view that page')
        return redirect('/')
        
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback Deleted!", "info")
    return redirect(f'/users/{session["username"]}')




