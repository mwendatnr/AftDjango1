import json

import requests
from django.http import HttpResponse
from django.shortcuts import render,redirect
from requests.auth import HTTPBasicAuth

from hospitalapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from hospitalapp.models import Appointment,Patient,Member
from hospitalapp.forms import AppointmentForm

# Create your views here.
def index(request):
    if request.method=='POST':
        if Member.objects.filter(username = request.POST['username'], password = request.POST['password']).exists():
            return render(request,'index.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')


def inner(request):
    return render(request,'inner-page.html')

def about(request):
    return render(request,'about.html')

def doctor(request):
    return render(request,'doctors.html')

def appointment(request):
    if request.method == 'POST':
        appointments= Appointment(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            department=request.POST['department'],
            doctor=request.POST['doctor'],
            message=request.POST['message']
        )
        appointments.save()
        return redirect("/show")
    else:
        return render(request,'appointment.html')

def show(request):
    myappointments = Appointment.objects.all()
    return render(request,'show.html',{'appointments':myappointments})

def delete(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect("/show")

def patients(request):
    allpatients= Patient.objects.all()
    return render(request,'patient.html',{'patients':allpatients})

def edit(request,id):
    editappointment= Appointment.objects.get(id=id)
    return render(request,'edit.html',{'appointment':editappointment})

def update(request,id):
    updateinfo= Appointment.objects.get(id=id)
    form = AppointmentForm(request.POST,instance=updateinfo)
    if form.is_valid():
        form.save()
        return redirect('/show')
    else:
        return render(request,'edit.html')


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')

def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Apen Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Payment made successfully")


def register(request):
    if request.method == "POST":
        member=Member(
            fullname=request.POST['fullname'],
            username=request.POST['username'],
            password=request.POST['password']
               )
        member.save()
        return redirect('/login')
    else:
        return render(request,'register.html')


def login(request):
    return render(request,'login.html')