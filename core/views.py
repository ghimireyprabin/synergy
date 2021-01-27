from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Directory,  Document


user_admin_required = user_passes_test(lambda user: user.is_superuser, login_url='accounts\login')

def admin_user_required(view_func):
    decorated_view_func = login_required(user_admin_required(view_func))
    return decorated_view_func

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr = request.user
        if usr.is_authenticated and usr.is_superuser:
            pass
        else:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def index(request):
    is_admin = True if request.user.is_superuser else False
    print(is_admin)
    context = {
        'is_admin' : is_admin
    }
    return render(request, 'core\index.html', context)

@admin_user_required
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'core\signup.html', {'form': form})


class DirectoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Directory
    fields = ['name']
    template_name = 'core/create_directory.html'
    success_url ='/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(DirectoryCreateView, self).form_valid(form)

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['file']
    template_name = 'core\create_document.html'
    success_url ='/'

    def form_valid(self, form):
        directory = Directory.objects.get(pk=self.kwargs['pk'])
        form.instance.uploaded_by = self.request.user
        form.instance.uploaded_to = directory
        return super(DocumentCreateView, self).form_valid(form)

class DirectoriesListView(LoginRequiredMixin, ListView):
    model = Directory
    template_name = 'core\dirs.html'
    context_object_name= 'dirs'

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'core\document_list.html'
    context_object_name= 'docs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        directory = Directory.objects.get(pk=self.kwargs['pk'])
        documents = Document.objects.filter(uploaded_to = directory)

        context['directory'] = directory
        context['documents'] = documents
            
        return context