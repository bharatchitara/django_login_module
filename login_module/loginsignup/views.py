import email
import datetime
from datetime import date
from genericpath import exists
from getpass import getuser
import re
from shutil import ExecError
from textwrap import indent
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
import secrets
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
import string
from django.core.mail import EmailMessage
from email import message
from django.shortcuts import render
from django.http import JsonResponse,request,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from .models import (users,session)
import django_restframework
import json

# Create your views here.


@csrf_exempt
def createUser(request):
    
    if request.method == 'POST':
        
        json_data = request.body.decode('utf-8')
        body = json.loads(json_data)
        
        email = body['email']
        mobile = body['mobile']
        userid = body['userid']
        password = body['password']
        
        
        emptyVar, duplicateVar = (checkDuplicateEmail(request,email))
        
            
        if(emptyVar == 101):
            message = [
                
                {
                    "success": "False",
                    "message" : "email is required"
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            message = [
                
                {
                    "success" : "False",
                    "message" : "Email already exist. Please use another email" 
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=409,content_type="application/json")
        
        flagValidEmail = 0
    
        try:
            validate_email(email) 
            flag_valid_email = 1
        
        except:
            message = [
                
                {
                    "success" : "False",
                    "message" : "Invalid Email used. correct email Format: johndow@example.com" 
                }
            ]
            return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        
        emptyVar, duplicateVar = (checkDuplicateMobile(request,mobile))
        
        
        if(emptyVar == 101):
            message = [
                {
                    "success": "False",
                    "message" : "mobile is required"
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            message = [
                
                {
                    "success" : "False",
                    "message" : "mobile already exist. Please use another mobile" 
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=409,content_type="application/json")
        
        
        emptyVar, duplicateVar = (checkDuplicateUserid(request,userid))
        
            
        if(emptyVar == 101):
            message = [
                
                {
                    "success": "False",
                    "message" : "userid is required"
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            message = [
                
                {
                    "success" : "False",
                    "message" : "userid already taken. Please use another userid" 
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=409,content_type="application/json")
        
        
        generatedPassword = ''
        
        copyGeneratedPassword = ''
        
        copyPassword = password
        
        flagForEmptyPass = 0
        
        if(password)== '':
            flagForEmptyPass = 1 
            generatedPassword = password_generate()
            copyGeneratedPassword = generatedPassword
            
            password = make_password(generatedPassword)
            
            
        else:
            password = make_password(password)
            
        if(flagForEmptyPass != 1):
        
            if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{8,}$",copyPassword):
                print(password)
            else:
                message = [
                    
                    {
                        "success" : "False", 
                        "message" : 'Incorrect Password used. The password should contains Min 8 characters including atleast 1 uppercase,atleast 1 lowercase, atleast 1 number(0-9), atleast 1 special character ( !, @, #, $, %, *)'
                    }
                ]
                
                
                return HttpResponse(json.dumps(message, indent=4) ,status=409,content_type="application/json")
            
        
        uName = body['name']
        uMobile = body['mobile']
        uEmail = body['email']
        uUserTypeid= body['user_type_id']
        uUserid = body['userid']
        uPassword = password
        uCreatedAt = datetime.datetime.now()
        uupdatedAt = datetime.datetime.now()
        uIsDeleted = 1
        
        
        addNewuser = users(name = uName, mobile = uMobile, email = uEmail, user_type_id =uUserTypeid, userid = uUserid, password = uPassword, 
                           created_at=uCreatedAt,updated_at = uupdatedAt, is_deleted = uIsDeleted)
        
        
        try:
            addNewuser.save()
            
            stCode= 201
           
        except:
            message = [
                 {
                "success": "False",
                "message" : "User creation failed"
                  }
            ]

            stCode= 400
            
        getUID = ''
        
        checkFlagForSendMail = 0
        
        if(stCode == 201):
            getUID = users.objects.get(email = uEmail)
            
            print(getUID.id)
            checkFlagForSendMail = sendVerifyMail(request, getUID.id, uEmail, uName)
            
            if(flagForEmptyPass == 1):
                sendGeneratedPassMail(request,copyGeneratedPassword,uEmail) 
                
            
        
        if(checkFlagForSendMail == 1 ):
            message = [
                {
                "success": "True",
                "message" : "User created successfully. Please verify the email to activate your account."
                }
            ]
            
            stCode= 201   
            
    return HttpResponse(json.dumps(message, indent=4) ,status=stCode,content_type="application/json")



def checkDuplicateEmail(request, inpEmail):
    
    emptyFlag= 0
    duplicateFlag = 0 
    
    if(inpEmail == ''):
        emptyFlag = 101
    
    else:
        checkEmail = ''
        
        try:
            checkEmail = users.objects.get(email = inpEmail)
            
        except:
            pass
        
        if (checkEmail):
            duplicateFlag = 101
    
    return emptyFlag,duplicateFlag


def checkDuplicateUserid(request,inpUserId):
    
    emptyFlag= 0
    duplicateFlag = 0 
    
    if(inpUserId == ''):
        emptyFlag = 101
    
    else:
        checkEmail = ''
        
        try:
            checkEmail = users.objects.get(userid = inpUserId)
            
        except:
            pass
        
        if (checkEmail):
            duplicateFlag = 101
    
    return emptyFlag,duplicateFlag
    
        

def checkDuplicateMobile(request, inpMobile):
    
    emptyFlag= 0
    duplicateFlag = 0 
    
    if(inpMobile == ''):
        emptyFlag = 101
    
    else:
        checkMobile = ''
        
        try:
            checkMobile = users.objects.get(mobile = inpMobile)
            
        except:
            pass
        
        if (checkMobile):
            duplicateFlag = 101
    
    return emptyFlag,duplicateFlag
        

def password_generate():
    

    symbols = ['!','@','#','$','%','*'] # Can add more
    
    password = ""
    
    for i in range(8):
        password += secrets.choice(string.ascii_lowercase)
    password += secrets.choice(string.ascii_uppercase)
    password += secrets.choice(string.digits)
    password += secrets.choice(symbols)
    return password        
            
            
            
        
def sendVerifyMail(request,userUid, userEmail, userName):
    
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('acc_active_email.html', {
                                        'user': userName,
                                        'domain': current_site.domain,
                                        'uid':urlsafe_base64_encode(force_bytes(userUid)),
                                        'token':account_activation_token.make_token(userEmail),
    })
    
    
    to_email = userEmail
    
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )

    passFlagForSendMail = 0
    
    try:
        email.send()
        passFlagForSendMail =  1 
    
    except:
        passFlagForSendMail = 0
    
    return passFlagForSendMail


    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = users.objects.get(id=uid)
       
      
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        
        user = None
        
    if user is not None and account_activation_token.check_token(user.email, token):
    
        user.is_deleted=0    #making the user active
        user.save()
        
        
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
    
def sendGeneratedPassMail(request, generatedPassword, userEmail):
    mail_subject = 'Activate your account.'
    message = 'Your Auto Generated Password is:'+generatedPassword
    
    print(message)
    
    to_email = userEmail
    
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )

    try:
        email.send()
    
    except:
        pass



@csrf_exempt
def updateUser(request):
    
    if request.method == 'POST':
        
        json_data = request.body.decode('utf-8')
        body = json.loads(json_data)
        
        requiredFields = ['email','mobile','userid']
         
        for i in requiredFields: 
            if i not in body.keys():
                message = [
                
                {
                    "success": "False",
                    "message" : "email, mobile and userid are Required Fields. Please add these fields in Json Body."
                }
            ]
            
                return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        
                
        
        uEmail = body['email']
        uMobile = body['mobile']
        uUserId = body['userid']
        
        emptyVar, duplicateVar = (checkDuplicateEmail(request,uEmail))
          
        if(emptyVar == 101):
            message = [
                
                {
                    "success": "False",
                    "message" : "email is required"
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            emptyVar, duplicateVar = (checkDuplicateMobile(request,uMobile))
        
        
            if(duplicateVar == 101):
                
                message = [
                    
                    {
                        "success" : "False",
                        "message" : "mobile already exist. Please use another mobile" 
                    }
                ]
                
                return HttpResponse(json.dumps(message, indent=4) ,status=409,content_type="application/json")
            
            
            emptyVar, duplicateVar = (checkDuplicateUserid(request,uUserId))
            
                
            if(duplicateVar == 101):
                
                message = [
                    
                    {
                        "success" : "False",
                        "message" : "userid already Exist. Please use another userid" 
                    }
                ]
                
                return HttpResponse(json.dumps(message, indent=4) ,status=409,content_type="application/json")
        
        
        getUser = ''
        
        try:
            getUser = users.objects.get(email = uEmail)
            
        
        except: 
            message = [
                    {
                        "success" : "False",
                        "message" : "User/Email not exist" 
                    }
                ]
            st_code = 400
            return HttpResponse(json.dumps(message, indent=4) ,status=st_code,content_type="application/json")
         
       
        updateUser = getUser
        copyUpdateUser = updateUser
        
        print(updateUser.name,updateUser.created_at,updateUser.updated_at, updateUser.is_deleted,updateUser.user_type_id )
        
        for key in body.keys():
            if(key == 'name'):
                updateUser.name = body['name']
            elif(key  == 'mobile'):
                updateUser.mobile = body['mobile']  
            elif(key == 'userid'):
                updateUser.userid = body['userid']
            elif(key == 'password'):
                updateUser.password = body['password']
            elif(key == 'user_type_id'):
                
                if(body['user_type_id'] == ""):
                    pass
                else:
                    updateUser.user_type_id = body['user_type_id']
                    
            elif(key == 'is_deleted'):
                if(body['is_deleted'] == ""):
                    pass
                else:
                    updateUser.is_deleted = body['is_deleted']
                
                
        updateUser.updated_at = datetime.datetime.now()
        
        print(updateUser.name,updateUser.created_at,updateUser.updated_at, updateUser.is_deleted,updateUser.user_type_id )
        
        
        updateSuccess = 0
        st_code = 0
        
        try:
            updateUser.save()
            updateSuccess = 1
            
        except:
            print('error')
        
        
        if(updateSuccess == 1 ):
            
            message = [
                    
                    {
                        "success" : "True",
                        "message" : "User updated successfully" 
                    }
                ]
                
            st_code = 201
        
        else:
            message = [
                    
                    {
                        "success" : "False",
                        "message" : "User updation failed" 
                    }
                ]
                
            st_code = 400
            
        return HttpResponse(json.dumps(message, indent=4) ,status=st_code,content_type="application/json")
         
         
@csrf_exempt
def deleteUser(request):
    
    if request.method == 'POST':
        
        json_data = request.body.decode('utf-8')
        body = json.loads(json_data)
        
        requiredFields = ['email']
        
        for i in requiredFields: 
            if i not in body.keys():
                message = [
                
                {
                    "success": "False",
                    "message" : "email is Required Fields. Please add that field in Json Body."
                }
            ]
            
                return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        
        uEmail = body['email']
        getUser = ''
        
        emptyVar, duplicateVar = (checkDuplicateEmail(request,uEmail))
          
        if(emptyVar == 101):
            message = [
                
                {
                    "success": "False",
                    "message" : "email is required"
                }
            ]
            
            return HttpResponse(json.dumps(message, indent=4) ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
        
            try:
                getUser = users.objects.filter(email = uEmail).delete()
                
                st_code = 201
                
                message = [
                        {
                            "success" : "True",
                            "message" : "User Deleted Successfully." 
                        }
                    ]

            
            except: 
                message = [
                        {
                            "success" : "False",
                            "message" : "User/ Email not exist" 
                        }
                    ]
                st_code = 400
            
        else:
            message = [
                        {
                            "success" : "False",
                            "message" : "User/ Email not exist" 
                        }
                    ]
            st_code = 400
            
                
        return HttpResponse(json.dumps(message, indent=4) ,status=st_code,content_type="application/json")
            
    else:
        message = [
                        {
                            "success" : "False",
                            "message" : "Plase use the Post method" 
                        }
                    ]
        st_code = 400
        return HttpResponse(json.dumps(message, indent=4) ,status=st_code,content_type="application/json")
         
