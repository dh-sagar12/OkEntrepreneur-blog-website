from django.db.models import query
from blog.models import Post
from home.models import Contact
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime 
# Create your views here.

def home(request):
    weekTime = datetime.date.today() - datetime.timedelta(days= 7)
    trends = Post.objects.filter(upload_date__gte= weekTime).order_by('-viewsCount')
    print(trends)
    popularPosts = Post.objects.filter(is_published=True).order_by('-viewsCount')
    params = {'popularPosts':popularPosts, 'trends': trends}
    return render(request, 'home/home.html', params)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(name, email, phone, message)
        if len(name)<3 or len(email)<5 or len(phone)<10 or len(message)<3:
            messages.error(request, 'Form Submission Error! Please Enter Correct Values Accordingly')
        else:
            contact = Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, 'Your Form Has Been Submitted Successfully')
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')










def userHandling(request):
    if request.method == 'POST':

        allUsers = User.objects.all()
         # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        # validate the users here 
        if len(username) > 15 or len(username)<3:
            messages.error(request, 'Username must not be greater than 10 characters and less than 3. Please sign up again. ')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        
        if pass1 != pass2:
            messages.error(request, 'Password do not matched. Please sign in again.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and number. Please signup again.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        
        for item in allUsers:
            if username == item.username:
                messages.error(request, 'User already exits with this user name. Please enter another user name')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


        
        
        # Creating the users
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        login(request, myuser)
        messages.success(request, " Your Account Has Been Created Successfully")
        # return redirect('home')
        # redirect to the same page where user is in 
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponse('404-Error occurs')


def loginHandeling(request):
    if request.method== 'POST':
        userNameLogin = request.POST['userNameLogin']
        passLogin = request.POST['passLogin']
        #authenticate the request with database
        user = authenticate(username= userNameLogin, password = passLogin)

        if user is not None:
            login(request, user)
            messages.success(request, " Your are Logged In Successfully")
            # return redirect('home')
            #This code will redirect to the same page from where user has logged in 
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            # return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, " Invalid Credentials. Please Log In Again Using Correct Credentials")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponse('404 not found')






def logoutHandeling(request):
    logout(request)
    messages.success(request, " Your are Logged Out Successfully")
    return redirect('home')

    
