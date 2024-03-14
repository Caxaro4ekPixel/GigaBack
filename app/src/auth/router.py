from app.src.auth import auth
from app.src.auth.views import LoginView, RegisterView


auth.add_url_rule('/login', view_func=LoginView.as_view('login'), methods=['POST'])
auth.add_url_rule('/register', view_func=RegisterView.as_view('register'), methods=['POST'])
