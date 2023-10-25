import os.path

from FoodyAuth import auth
from FoodyAuth.form import LoginForm
from FoodyConfig.config import Auth_Static, ADMIN_LOGIN_TOKEN
from FoodyCore.extension import ServerCaptchaV2, db, ServerRedis
from FoodyAuth.AccessControl.decorators import change_password_only

import FoodyAuth.utils as AuthUtils
import FoodyAuth.model as AuthModel
import FoodyAuth.form as AuthForm
import FoodyAdmin.model as AdminModel

from flask import render_template, send_from_directory,\
    redirect, flash, request, get_flashed_messages, session,\
    url_for, jsonify, abort


@auth.get("/get/notifications/")
def get_notification():
    """This view return user all flash messages in a json"""
    flashes = []
    messages = get_flashed_messages(with_categories=True)

    for category, message in messages:
        temp = {"message": message}
        flashes.append(temp)
    return jsonify(flashes)


@auth.get("/logout/")
def logout():
    """Logout User"""
    session.clear()
    return redirect(url_for('web.index_view'))


@auth.route("/static_auth/<path:filename>")
def AuthStatic(path):
    """
        Serve Auth Static File
    """
    if os.path.exists(Auth_Static / path):
        return send_from_directory(Auth_Static, path)
    else:
        return "File Not Found!", 404


@auth.get("/login/")
def login():
    """Show Login Form for users"""
    form = LoginForm()
    return render_template("auth/login.html", form=form)


@auth.post("/login/")
def login_post():
    """
        this view take a post request : for users to log in to their accounts
    """
    form = LoginForm()
    captcha = ServerCaptchaV2.is_verify()

    if form.validate() and captcha:
        username = form.username.data
        password = form.password.data
        if not(user_db := AuthModel.User.query.filter(AuthModel.User.Username == username).first()):
            flash("کاربری با اطلاعات وارد شده یافت نشد" ,"danger")
            return redirect(request.referrer)

        if not user_db.CheckPassword(password):
            flash("اعتبار سنجی حساب نادرست است", "danger")
            return redirect(request.referrer)

        if user_db.Is_Active():
            AuthUtils.login(user_session=session, user_db=user_db)
            flash(f"کارمند گرامی{user_db.Username} خوش آمدیدی ")
            return redirect(url_for("user.index_view"))
        else:
            # if user have a token and it has a valid time
            if (old_token := ServerRedis.get(name=user_db.PublicKey)):
                old_token = str(old_token.decode('utf-8'))
                session['reset-token'] = old_token
                return redirect(url_for('auth.setNewPassword'))

            if not (token := AuthUtils.generate_change_password_token(user_db.PublicKey)):
                flash("خطایی در تولید کد برای تغییر گذرواژه رخ داد", "danger")
                return redirect(request.referrer)

            if not ServerRedis.set(name=token, value=user_db.PublicKey):
                flash("خطایی رخ داد بعدا امتحان کنید \nError Code : 91", "danger")
                return redirect(request.referrer)

            if not ServerRedis.set(name=user_db.PublicKey, value=token):
                flash("خطایی رخ داد بعدا امتحان کنید \nError Code : 95", "danger")
                return redirect(request.referrer)


            session['reset-token'] = token
            return redirect(url_for('auth.setNewPassword'))


    else:
        if not captcha:
            flash("ارزیابی کپچا نادرست بود،  لطفا دوباره امتحان کنید", "danger")
            return render_template("auth/login.html", form=form)

        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return render_template("auth/login.html", form=form)


@auth.get("/setPassword/")
@change_password_only
def setNewPassword():
    """ SetNew password for users"""
    flash("برای اطمینان از امینت حسابتان لطفا گذرواژه خود را تغییر دهید")
    form = AuthForm.ChangePasswordForm()
    return render_template('auth/changepassword.html', form=form)


@auth.post("/setPassword/")
@change_password_only
def setNewPassword_POST():
    """ SetNew password for users : POST Requests """
    form = AuthForm.ChangePasswordForm()
    captcha = ServerCaptchaV2.is_verify()

    if form.validate() and captcha:

        if not (user_key := ServerRedis.get(session.get('reset-token', None))):
            session.clear()
            abort(401)

        user_key = str(user_key.decode('utf-8'))
        if not (user_db := AuthUtils.LoadUserObjectPublickKey(public_key=user_key)):
            session.clear()
            abort(401)

        password = form.password.data
        user_db.SetPassword(password)
        user_db.SetActive()
        try:
            db.session.add(user_db)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            session.clear()
            flash("خطایی رخ داد / بعدا امتحان کنید", "danger")
            return redirect(url_for('auth.login'))
        else:
            session.clear()
            AuthUtils.login(user_session=session, user_db=user_db)
            flash("حساب کاربری با موفقیت فعال گردید", "success")
            return redirect(url_for('auth.login'))

    else:
        if not captcha:
            flash("ارزیابی برای کپچا اشتباه است. دوباره سعی کنید")
            return redirect(request.referrer)

        flash("برخی موارد مقدار دهی نشده اند")
        return redirect(request.referrer)



@auth.route(f"/admin/login/<string:token>/", methods=["GET"])
def admin_login_get(token):
    """Admin Login Route"""

    if not token or token != ADMIN_LOGIN_TOKEN:
        abort(404)

    form = AuthForm.LoginForm()
    form.login_path = url_for('auth.admin_login_post', token=ADMIN_LOGIN_TOKEN)
    return render_template('auth/admin-login.html', form=form)


@auth.route("/admin/login/<string:token>/", methods=["POST"])
def admin_login_post(token):
    if not token or token != ADMIN_LOGIN_TOKEN:
        abort(404)

    form = AuthForm.LoginForm()
    captcha = ServerCaptchaV2.is_verify()

    if not captcha:
        flash("ارزیابی کپچا ناموفق بود، دوباره سعی کنید", "danger")
        return redirect(request.referrer)

    if not form.validate():
        flash("برخی مقادیر مقدار دهی نشده اند", "danger")
        return render_template('auth/admin-login.html', form=form)

    username = form.username.data
    password = form.password.data
    admin_db = AdminModel.Admin.query.filter_by(Username=username).first()

    if not admin_db:
        flash("اعتبار سنجی نادرست است", "danger")
        return render_template('auth/admin-login.html', form=form)

    if not admin_db.Is_Active():
        flash("حساب کاربری مورد نظر غیرفعال می باشد", "danger")
        return redirect(request.referrer)

    if admin_db.Is_TryNumber_Check():
        flash("تلاش بیش از اندازه حساب کاربری مورد نظر قفل گردید\nبرای بازگشایی قفل به پشتیبانی مراجعه کنید", "danger")
        return redirect(request.referrer)

    #  Ar-Real-Ip  =: Arvan Cloud Put Users Real Ip in this header in request := Ar-Real-Ip
    #  Ar-Real-Country  =: Arvan Cloud Put Users Country Ip in this header in request := Ar-Real-Country
                # if this web app is hosting and getting services from other cdn providers make sure you change Ar-Real-Ip
    userIP = (request.headers.get("Ar-Real-Ip", request.remote_addr) or "0.0.0.0")
    if not admin_db.CheckPassword(password):
        admin_db.TryNumber += 1
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

        admin_db.SetAdminLogin("Login - failed - invalid password", ip=userIP)
        flash("اعتبار سنجی نادرست است", "danger")
        return render_template('auth/admin-login.html', form=form)



    # log admin in db and set last login time
    admin_db.SetAdminLogin(message="Login - Successful", ip=userIP)
    admin_db.SetLastLogin()
    admin_db.ResetTryNUmber() # if login is successfully rest try numbers

    try:
        db.session.add(admin_db)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


    session['login'] = True
    session['account-id'] = admin_db.id
    session['password'] = admin_db.Password # hash password
    session['admin'] = True


    flash(f"ادمین گرامی {admin_db.Username} خوش آمدید", "success")
    return redirect(url_for('admin.index'))
