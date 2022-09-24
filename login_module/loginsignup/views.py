import email
from email import message
from django.shortcuts import render
from django.http import JsonResponse,request,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password, make_password
from loginsignup.models import (users,session)
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
            
            return HttpResponse(message ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            message = [
                
                {
                    "success" : "False",
                    "message" : "Email already exist. Please use another email" 
                }
            ]
            
            return HttpResponse(message ,status=409,content_type="application/json")
        
        
        emptyVar, duplicateVar = (checkDuplicateMobile(request,mobile))
        
        
        if(emptyVar == 101):
            message = [
                {
                    "success": "False",
                    "message" : "mobile is required"
                }
            ]
            
            return HttpResponse(message ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            message = [
                
                {
                    "success" : "False",
                    "message" : "mobile already exist. Please use another mobile" 
                }
            ]
            
            return HttpResponse(message ,status=409,content_type="application/json")
        
        
        emptyVar, duplicateVar = (checkDuplicateUserid(request,userid))
        
            
        if(emptyVar == 101):
            message = [
                
                {
                    "success": "False",
                    "message" : "userid is required"
                }
            ]
            
            return HttpResponse(message ,status=302,content_type="application/json")
        
        elif(duplicateVar == 101):
            
            message = [
                
                {
                    "success" : "False",
                    "message" : "userid already exist. Please use another userid" 
                }
            ]
            
            return HttpResponse(message ,status=409,content_type="application/json")
        
        
        generatedPassword = ''
        
        if(password)== '':
            generatedPassword = password_generate
            password  = make_password(generatedPassword)
        else:
            password = make_password(password)
            
        
        
        uName = body['name']
        uMobile = body['mobile']
        uEmail = body['email']
        uUserTypeid= body['user_type_id']
        uUserid = body['userid']
        uPassword = body['password']
        uCreatedAt = body['created_at']
        uupdatedAt = body['updated_at']
        uIsDeleted = body['is_deleted']
        
        
        addNewuser = users(name = uName, mobile = uMobile, email = uEmail, user_type_id =uUserTypeid, userid = uUserid, password = uPassword, 
                           created_at=uCreatedAt,updated_at = uupdatedAt, is_deleted = uIsDeleted)
        
        
        try:
            addNewuser.save()
            
            message = [
                {
                "success": "True",
                "message" : "User created successfully"
                }
            ]
            
            stCode= 201
            
            
        except:
            message = [
                 {
                "success": "False",
                "message" : "User creation failed"
                  }
            ]

            stCode= 400
        
            

    return HttpResponse(message ,status=stCode,content_type="application/json")



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
            
            
            
        
            


    
    
    