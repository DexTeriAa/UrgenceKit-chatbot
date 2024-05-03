from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def home(request):
    return render(request, 'home.html', {})

genai.configure(api_key='AIzaSyDUMXJEFv0W5niUyaK8aV4AIgXwe73iqHo')
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


def main(request):
  template = loader.get_template('boxbot.html')
  return HttpResponse(template.render())



@csrf_exempt
# def generate_chat(request):
   

#     if request.method == 'POST':
#         msg = request.POST.get('msg', '') 
#         response = model.generate_content(msg)
#         template = loader.get_template('boxbot.html')
#         context = {
#         'response': response,
#         } 
#         return HttpResponse(template.render(context, request))
#     else:
#         return HttpResponse("Invalid request method")

def generate_chat(request):
   
   
    if request.method == 'POST':
       

        msg = request.POST.get('msg', '') 
        chat.send_message(msg)
        list_test = ['innondation','Hello', 'Salut' ,'tremblement', 'terre','vagues','tsunami','chaleur','incendie']
        if any(word in msg for word in list_test):
            


            template = loader.get_template('boxbot.html')
            context = {
             
            'response': chat.history,
            } 
            return HttpResponse(template.render(context, request))
        elif 'map' in msg:  # Si l'utilisateur demande la carte
            return map_view(request)
        else:
            template = loader.get_template('boxbot.html')

            chat.history[-1].parts[0].text="Désolé, je suis conçu pour discuter des préparatifs d'urgence et des fournitures nécessaires en cas de catastrophe"
            context = {
             
            'response': chat.history,
            } 
            return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponse("Invalid request method")



def map_view(request):
    template = loader.get_template('map.html')
    return HttpResponse(template.render())


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("There was an error login in , try again..."))
            return redirect('login')
    else:
        return render(request, 'login.html')
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You were Logged Out !"))
    return redirect('/')

   
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('main')  
        
        else:
            
            return render(request, 'register_user.html', {'form': form})
    else:
        form = RegisterUserForm()
    return render(request, 'register_user.html', {'form': form})




    
  