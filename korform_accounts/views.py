from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from .forms import RegistrationForm

class RegistrationView(DefaultRegistrationView):
    form_class = RegistrationForm
