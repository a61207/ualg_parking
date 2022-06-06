from django.views.generic import TemplateView, CreateView, DetailView
from main.forms import UserForm
from main.models import User


# Create your views here.
class Index(TemplateView):
    template_name = 'index.html'


class SignIn(CreateView):
    model = User
    form_class = UserForm
