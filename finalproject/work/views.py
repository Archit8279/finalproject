from django.shortcuts import render,redirect
from .models import users  
from datetime import date
from dateutil import parser
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.db import IntegrityError
import random
import socket

# Create your views here.
def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'login.html')


def home(request):
    return render(request,'home.html') 

def product(request):
    return render(request,'product.html') 

def fgtpwdgo(request):
    return render(request,'fgtpwd.html') 


def add(request):
    uname = request.POST['uname']
    pwd = request.POST['pwd']
    fname = request.POST['fname']
    lname = request.POST['lname']
    mob = request.POST['mob']
    email = request.POST['email']
    dob = parser.parse(request.POST['dob']).date()
    if 'romantic' in request.POST:
        romantic = request.POST['romantic']
    else:
        romantic = False
    if 'act' in request.POST:
        act = request.POST['act']
    else:
        act = False
    if 'comedy' in request.POST:
        comedy = request.POST['comedy']
    else:
        comedy = False
    if 'animation' in request.POST:
        animation = request.POST['animation']
    else:
        animation = False
    if 'horror' in request.POST:
        horror = request.POST['horror']
    else:
        horror = False

    days_in_year = 365.2425    
    age = int((date.today() - dob).days / days_in_year)
    otp = random.randint(100000,999999)

    u = users(uname = uname,pwd=pwd,fname=fname,lname=lname,mob=mob,email=email,
    dob=dob,age=age,otp=otp,romantic=romantic,action=act,comedy=comedy,animation=animation,
    horror=horror)
    try:
        u.save()
    except IntegrityError:
        messages.error(request,"This e-mail is already registered, try another email to Signup")
        return redirect('signup')

    try:
        send_mail('Email verification', 'your email verification OTP is '+ str(otp), 'hypemoveis2020@gmail.com', [email])
    except socket.gaierror:
        print('email not sent')

    record = users.objects.filter(uname = uname,pwd=pwd,otp=otp)
    for r in record:
        request.session['id'] = r.uid
    return render(request,'verification.html')

def check(request):
    uname = request.POST['uname']
    pwd = request.POST['pwd']
    recs = users.objects.filter(uname = uname,pwd = pwd)
    if recs: 
        for a in recs:
            request.session['uname']=uname
            request.session['uid'] = a.uid
        return render(request,'home.html')
    else:
        rec = users.objects.filter(email = uname,pwd = pwd)
        if rec:
            for b in rec:
                request.session['uname']=b.uname
                request.session['uid'] = b.uid
            return render(request,'home.html')
        else:
            messages.error(request,'login failed, wrong credentials!')
            return redirect('signin')
        
def verify(request):
    otp = int(request.POST['otp'])
    if request.session.has_key('id'):
        uid = request.session.get('id')
        rec = users.objects.filter(uid = uid)
    elif request.session.has_key('mail'):
        email = request.session.get('mail')
        rec = users.objects.filter(email = email)
    if rec:
        for a in rec:
            if a.otp == otp:
                if request.session.has_key('id'):
                    del request.session['id']
                    return render(request,'login.html')
                elif request.session.has_key('mail'):
                    return render(request,'changepwd.html')

            else:
                if request.session.has_key('id'):
                    del request.session['id']
                    rec.delete()
                    return render(request,'signup.html')
                elif request.session.has_key('mail'):
                    del request.session['mail']
                    messages.error(request,'wrong OTP')
                    return redirect('verify')
        
def profile(request):
    if request.session.has_key('uid'):
        uid = request.session.get('uid')
        rec = users.objects.get(uid = uid)
        return render(request,'profile.html',{'data':rec})
    else:
        return HttpResponse('invalid')

def logout(request):
    if request.session.has_key('uid'):
        del request.session['uid']
    if request.session.has_key('uname'):
        del request.session['uname']
    return render(request,'login.html')

def editprofile(request):
    if request.session.has_key('uid'):
        uid = request.session.get('uid')
        rec = users.objects.get(uid = uid)
        return render(request,'editprofile.html',{'data':rec})
    else:
        messages.error(request,'invalid')
        return redirect('profile')

def saveprofile(request):
    if request.session.has_key('uid'):
        uid = request.session.get('uid')
        rec = users.objects.get(uid = uid)
        umail = rec.email
        rec.pwd = request.POST['pwd']
        rec.fname = request.POST['fname']
        rec.lname = request.POST['lname']
        rec.mob = request.POST['mob']
        rec.email = request.POST['email']
        rec.dob = parser.parse(request.POST['dob']).date()
        if 'romantic' in request.POST:
            rec.romantic = request.POST['romantic']
        else:
            rec.romantic = False
        if 'act' in request.POST:
            rec.act = request.POST['act']
        else:
            rec.act = False
        if 'comedy' in request.POST:
            rec.comedy = request.POST['comedy']
        else:
            rec.comedy = False
        if 'animation' in request.POST:
            rec.animation = request.POST['animation']
        else:
            rec.animation = False
        if 'horror' in request.POST:
            rec.horror = request.POST['horror']
        else:
            rec.horror = False

        days_in_year = 365.2425    
        rec.age = int((date.today() - rec.dob).days / days_in_year)
        if request.POST['email'] != umail:
            rec.otp = random.randint(100000,999999)
            rec.save()
            try:
                send_mail('Email verification', 'your email verification OTP is '+ str(rec.otp), 'hypemoveis2020@gmail.com', [email])
            except socket.gaierror:
                print('email not sent')
            record = users.objects.get(uid = uid)
            for r in record:
                request.session['id'] = r.uid
            return render(request,'verification.html')
        else:
            rec.save()
            record = users.objects.get(uid = uid)
            return render(request,'profile.html',{'data':record})

def resend(request):
    if request.session.has_key('id'):
        rec = users.objects.get(uid = id)
        email = rec.email
        rec.otp = random.randint(100000,999999)
        rec.save()
        try:
            send_mail('Email verification', 'your email verification OTP is '+ str(rec.otp), 'hypemoveis2020@gmail.com', [email])
        except socket.gaierror:
            print('email not sent')
        return render(request,'verification.html')
    else:
        messages.error(request,'OTP already sent')
        return redirect('verify')

def fgtpwd(request):
    email = request.POST['email']
    fname = request.POST['fname']
    lname = request.POST['lname']
    request.session['mail'] = email
    rec = users.objects.get(email = email, fname=fname,lname=lname)
    if rec:
        rec.otp = random.randint(100000,999999)
        rec.save()
        try:
            send_mail('Email verification', 'your email verification OTP is '+ str(rec.otp), 'hypemoveis2020@gmail.com', [email])
        except socket.gaierror:
            print('email not sent')
        return render(request,'verification.html')
    else:
        messages.error(request,'invalid')
        return redirect('signin')

def changepwd(request):
    if request.session.has_key('mail'):
        email = request.session['mail']
        pwd = request.POST['pwd']
        rec = users.objects.get(email = email)
        rec.pwd = pwd
        rec.save()
        del request.session['mail']
        return render(request,'login.html')
    else:
        messages.error(request,'invalid')
        return redirect('changepwd')