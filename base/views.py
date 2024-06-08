from django.shortcuts import render
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from base.funcutlils import calculate_key_dates_slu, calculate_key_dates_uppsala
from django.contrib.auth import logout, authenticate
from base.forms import LoginForm, SignupForm
from django.contrib.auth import login as dj_login
from django.shortcuts import render, redirect
from django.conf import settings



def login_view(request):
    if request.user.is_authenticated:
        return redirect("index_view")
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)

            if user is not None:
                dj_login(request, user)

                redirect_url = request.POST.get('redirect_url') if request.POST.get('redirect_url') else settings.LOGOUT_REDIRECT_URL

                return redirect(redirect_url)
            else:
                form.add_error('password', "No! Account Found. Please enter a correct email and password. Note that both fields may be case-sensitive")
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def signup_view(request):
    if request.user.is_authenticated:
        return redirect("index_view")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index_view')
        
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('index_view')


def index(request):
    current_date = date.today()
    selected_university = None  # Initialize the selected_university variable
    warning = None
    context = {}
    if request.method == 'POST':
        defence_date_str = request.POST.get('defence_date')  # Using get is safer as it won't raise a KeyError
        selected_university = request.POST.get('university', '')

        if not defence_date_str:
            context = {
                "error":"Defence date cannot be empty.",
                "current_date":current_date, 
                "university":selected_university
            }

        
        # Check if no university is selected
        if selected_university == '':
            context = {
                "error":"No university selected.",
                "current_date":current_date, 
                "university":selected_university
            }
            return render(request, 'index.html', context)
    
        # Convert the defence_date_str to a date object
        defence_date = datetime.strptime(defence_date_str, '%Y-%m-%d').date()

        
        
        # Calculate the key dates based on the selected university
        if selected_university == 'SLU':
            # Check for the minimum defence date (at least 5 months in the future)
            minimum_defence_date = date.today() + relativedelta(months=+5)
            
            if defence_date < minimum_defence_date:
                warning = 'Limited time for preparation, please consider a date at least 5 months in advance.'

            
            key_dates = calculate_key_dates_slu(defence_date_str)
        elif selected_university == 'Uppsala university':
            # Check for the minimum defence date (at least 7 months in the future)
            minimum_defence_date = date.today() + relativedelta(months=+5)
            
            if defence_date < minimum_defence_date:
                warning = 'Limited time for preparation, please consider a date at least 5 months in advance.'

            key_dates = calculate_key_dates_uppsala(defence_date_str)

        if "error" in key_dates:
            context = {
                "error":key_dates["error"],
                "current_date":current_date, 
                "university":selected_university
            }
            return render(request, 'index.html', context)

        context = {
            "key_dates":key_dates,
            "current_date":current_date, 
            "university":selected_university
        }

        return render(request, 'index.html', context)
    
    context = {
        "current_date":current_date,
        "university":selected_university,
        "warning":warning
    }

    return render(request, 'index.html', context)