from django.shortcuts import render,redirect
from . models import User,Product
from django.contrib.auth.hashers import make_password,check_password
import requests
import random

# Create your views here.
def index(request):
	return render(request,'index.html')

def product(request):
	return render(request,'product.html')

def about(request):
	return render(request,'about.html')

def blog(request):
	return render(request,'blog.html')

def contact(request):
	return render(request,'contact.html')

def shoping_cart(request):
	return render(request,'shoping-cart.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
			   User.objects.create(
			   			usertype=request.POST['usertype'],
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=make_password(request.POST['password']),
						profile_picture=request.FILES['profile_picture'],
						)
			   msg="User Sign Up Successfuly"
			   return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Dose Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			checkpassword=check_password(request.POST['password'],user.password)
			if checkpassword==True:
				if user.usertype=="buyer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_picture']=user.profile_picture.url
					return render(request,'index.html')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_picture']=user.profile_picture.url
					return render(request,'seller-index.html')
			else:
				msg="Password Is Incorrect"
				return render(request,'login.html',{'msg':msg})
		except:
			return render(request,'login.html',{'msg':'Email Is Incorrect'})

	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			otp=random.randint(1000,9999)
			user=User.objects.get(mobile=request.POST['mobile'])
			mobile=request.POST['mobile']
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"oL3B6xfN5SsXYePmZlMWczkCGVDR9hbIdy2irJ8qQF01avHtg4lLPywBFkI2gDqOove6SYzjm08CaV5d","variables_values":str(otp),"route":"otp","numbers":mobile}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			request.session['mobile']=mobile
			request.session['otp']=otp
			return render(request,'otp.html')
		except:
			msg="Mobile Number Dose Not Exists"
			return render(request,'forgot-password.html',{'msg':msg})

	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	otp=int(request.session['otp'])
	uotp=int(request.POST['uotp'])

	if otp==uotp:
		del request.session['otp']
		return render(request,'new-password.html')
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['newpassword']==request.POST['cnewpassword']:
		mobile=request.session['mobile']
		user=User.objects.get(mobile=mobile)
		user.password=request.POST['newpassword']
		user.save()
		return redirect('logout')

	else:
		msg="New Password & New Confirm Password Dose Not Matched"
		return render(request,'new-password.html',{'msg':msg})
 
def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		request.session['profile_picture']=user.profile_picture.url
		msg="Profile Updated Successfuly"
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})

def change_password(request):
	email=request.session['email']
	user=User.objects.get(email=email)
	if request.method=="POST":
		checkpassword=check_password(request.POST['oldpassword'],user.password)
		if checkpassword==True:
			if request.POST['newpassword']==request.POST['cnewpassword']:
				user.password=make_password(request.POST['newpassword'])
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confirm New Password Dose Not Matched"
				if user.usertype=="buyer":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})
		else:
			msg="Old Password Dose Not Matched"
			if user.usertype=="buyer":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'seller-change-password.html',{'msg':msg})			 
	else:
		if user.usertype=="buyer":
			return render(request,'change-password.html')
		else:
			return render(request,'seller-change-password.html')