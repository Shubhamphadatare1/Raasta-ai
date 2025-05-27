from dashboard import login, helmet

if not login.check_login():
    login.login()
else:
    helmet.run_module()