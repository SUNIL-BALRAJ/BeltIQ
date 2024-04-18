from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import time
from django.contrib.auth.decorators import login_required
import joblib

def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, "pages/index.html", context)


# Authentication
class UserRegistrationView(CreateView):
  template_name = 'accounts/auth-signup.html'
  form_class = RegistrationForm
  success_url = '/accounts/login/'

class UserLoginView(LoginView):
  template_name = 'accounts/auth-signin.html'
  form_class = LoginForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/auth-reset-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/auth-password-reset-confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/auth-change-password.html'
  form_class = UserPasswordChangeForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def profile(request):
  context = {
    'segment': 'profile',
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def sample_page(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/sample-page.html', context)


@login_required(login_url='/accounts/login/')
def live_data(request):
  context = {
    'segment': 'live_data',
  }
  return render(request, 'pages/live_data.html', context)



@login_required(login_url='/accounts/login/')
def failure(request):
  context = {
    'segment': 'failure',
  }
  return render(request, 'pages/failure.html', context)

@login_required(login_url='/accounts/login/')
def profile(request):
    misleading_results = AnalysisResult.objects.filter(conclusion='misleading')
    return render(request, 'pages/profile.html', {'misleading_results': misleading_results})

@login_required(login_url='/accounts/login/')
def misleading_telegram(request):
    misleading_results = TelegramAnalysis.objects.filter(conclusion='Potentially Misleading')
    return render(request, 'pages/misleading_telegram.html', {'misleading_results': misleading_results})

@login_required(login_url='/accounts/login/')
def prediction(request):
    import math
    last_uploaded_text = None
    if request.method == 'POST':
      
      while True:
        print("running")
        base_url = 'https://api.thingspeak.com/channels/2375718/feeds.json?api_key=ATHYX1B78TCPT7W6&results=2'
        params = {'results': 1}
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json() 

        # Extract the 'feeds' values
        input = data.get('feeds', [])

        # Extract the desired values into a list
        if input:
            feed_values = [
                input[0]['entry_id'],
                float(input[0]['field1'].strip()) if input[0]['field1'].strip() != 'NaN' else 0.0,
                float(input[0]['field2']) if input[0]['field2'].strip() != 'NaN' else 0.0,
                int(input[0]['field3']) if input[0]['field3'].strip() != 'NaN' else 0,
                int(input[0]['field4']) if input[0]['field4'].strip() != 'NaN' else 0,
                int(input[0]['field5']) if input[0]['field5'].strip() != 'NaN' else 0,
                int(input[0]['field6']) if input[0]['field6'].strip() != 'NaN' else 0
                
            ]

            print(feed_values)
        
        else:
            print("No 'feeds' data found.")
        inp=feed_values[0:3]
        inputrf=[]
        inputrf.append(inp)
        model = joblib.load(r'home\my_random_forest.joblib')
        a = model.predict(inputrf)
        print(f'Prediction is {a}')

        import pickle
        if feed_values[3]>10:
          alert="Alert"
          reason="High Vibrations"
        elif feed_values[2]>30:
          alert="Alert"
          reason="High Temperature"
        elif feed_values[2]<10:
          alert="Alert"
          reason="Low Temperature" 
        if feed_values[3]>10 or feed_values[2]>30 or feed_values[2]<10: 
          break
        time.sleep(5)
      

      analysis_result = TelegramAnalysis(
            alert_status=alert,
            location="Segment1",
            reason=reason,
            measure="parameter abnormal :"+reason + "/n" + "The main motive is to predict dislodgement of cable belt conveyer by sensing and analysing parameters like temperature, vibration, moisture, accelerometer and give some suggestions or preventive, corrective measures. I have given the parameter which is abnormal based on our sensor data. please give me suggestion or preventive corrective measure for futher steps. for eg if we sense that the vibration is very high the reason would maybe because of high load at that point, decrease in tension, dislocation of pulleys etc. so you can suggest corrective measures."

        )
      analysis_result.save()   
      last_uploaded_text= TelegramAnalysis.objects.latest('uploaded_at')

    return render(request, 'pages/prediction.html',  {'latest_analysis_result': last_uploaded_text})
   




