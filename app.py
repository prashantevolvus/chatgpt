from flask import Flask, render_template, redirect, url_for, session, current_app
from flask_oauthlib.client import OAuth
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.secret_key = "your-secret-key"

oauth = OAuth(app)

# Initialize Bootstrap
bootstrap = Bootstrap5(app)

microsoft = oauth.remote_app(
    "microsoft",
    consumer_key="b0c07c90-9ee5-4380-a653-0ead0ca1c5ea",
    consumer_secret="PLW8Q~5VvwGczqmSP0OGysqsNwrFjw.RBgsu6cnn",
    request_token_params={"scope": "User.Read"},
    base_url="https://graph.microsoft.com/v1.0/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
)

# Mock data for menu options
menu_options = [
    {"name": "Define Test", "url": "/define-test"},
    {"name": "Assign Test", "url": "#"},
    {"name": "Add User", "url": "#"},
    {"name": "Add Role", "url": "#"},
    {"name": "Test Reports", "url": "#"},
    {"name": "Audit Trail", "url": "#"}
]


@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("index.html", menu_options=menu_options)


@app.route("/login")
def login():
    if session.get("user"):
        return redirect(url_for("index"))
    return microsoft.authorize(callback=url_for("authorized", _external=True))

@app.route("/define-test")
def define_test():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("define_test.html", menu_options=menu_options)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/authorized")
def authorized():
    response = microsoft.authorized_response()
    if response is None or "access_token" not in response:
        return "Access denied: Reason={}&Error={}".format(
            response.get("error"), response.get("error_description")
        )
    session["user"] = response["access_token"]
    return redirect(url_for("index"))


@microsoft.tokengetter
def get_microsoft_token():
    with current_app.app_context():
        return session.get("user")


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")



if __name__ == "__main__":
    app.run(ssl_context=("cert.pem", "key.pem"))
