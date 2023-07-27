from django.shortcuts import render,redirect
from .models import Contact,User
# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        msg="Contact Saved Successfully"
        return render(request,'contact.html',{'msg':msg})
    else:
        return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:

                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    usertype=request.POST['usertype']
                )
                msg="User Signup Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password and Confirm Password does not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:

            user=User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']
            )
            print("-------------->role",user.usertype)
            if user.usertype=="user":
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'index.html')
            elif user.usertype=="seller":
                 request.session['email']=user.email
                 request.session['fname']=user.fname
                 return render(request,'seller_index.html')
        except:
            msg="Email or Password is Incorrect"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        msg="User Logout Successfully"
        return render(request,'login.html',{'msg':msg})
    except:
        return render(request,'login.html')
    
def change_password(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg="New password and Confirm new password does not matched!"
                return render(request,'change_password.html',{'msg':msg})
            
        else:
            msg="Old Password does not matched!"
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')
    
def seller_index(request):
    return render(request,'seller_index.html')

def seller_change_password(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
               msg="New password and Confirm new password does not matched!"
               return render(request,'seller_change_password.html',{'msg':msg})
        else:
            msg="Old Password does not matched!"
            return render(request,'seller_change_password.html',{'msg':msg})
    else:
        return render(request,'seller_change_password.html')