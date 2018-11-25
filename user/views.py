from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import os
from django.views import View
from BaseView.BaseView import BaseViewClass
from django.conf import settings
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile
from userPanel.views import info
from django.contrib.auth.password_validation import validate_password
import random
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils.decorators import method_decorator
import requests,json,time
# Create your views here.

def checkPass(password):
    notAllowed = ['ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش',
               'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'ل', 'م', 'ن', 'و', 'ه', 'ی', 'گ', ' ']
    for char in password:
        if char in notAllowed:
            return False
    return True

def userCharCheck(username):
    allowed = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'
        ,'p','q','r','s','t','u','v','w','x','y','z','@','_','1','2','3','4','5','6','7','8','9','0']
    for char in username:
        if char not in allowed:
            return False
    return True

def nameAndLastnameCharCheck(name,lastname):
    Allowed = ['ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش',
               'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'ل', 'م', 'ن', 'و', 'ه', 'ی', 'گ',' ']
    for char in name:
        if char not in Allowed:
            return 'name',False
    for char in lastname:
        if char not in Allowed:
            return 'lastname',False
    return '',True


def checkNotLogin(user):
    return not user.is_authenticated

def sendSms(password,username,phone):
    data = {
        "ParameterArray": [
            {"Parameter": "username", "ParameterValue": username}, {'Parameter': 'password', 'ParameterValue': password}
        ],
        "Mobile": phone,
        "TemplateId": "4062"
    }
    req = requests.post('http://RestfulSms.com/api/Token',
                          data={'UserApiKey': 'd401b2a8cba80bb6c4edbf6b', 'SecretKey': '@H1ssen6221'})
    token = json.loads(req.content.decode('utf-8'))['TokenKey']
    header = {'x-sms-ir-secure-token':token,'Content-Type':'application/json'}
    sendSms = requests.post('http://RestfulSms.com/api/UltraFastSend',data=json.dumps(data),headers=header)
    # print(json.loads(sendSms.content.decode('utf-8')))
    return json.loads(sendSms.content.decode('utf-8'))['IsSuccessful']
    # return True


@method_decorator(decorator=user_passes_test(checkNotLogin,login_url='/UserPanel/Info'),name='dispatch')
class Login(BaseViewClass):
    context = {}
    returnNotFullUser = 'userPanel:info'
    returnFullUser = 'books:Home'
    templateName = 'user/login.html'
    def get(self,req):
        try:
            reg = req.session.pop('sucRegister')
        except:
            reg = False
        self.context['reg'] = reg
        return render(req, self.templateName, context=self.context)

    def post(self,req):
        err = False
        try:
            reg = req.session.pop('sucRegister')
        except:
            reg = False
        self.context['reg'] = reg
        try:
            username = req.POST['username']
            password = req.POST['pass']
            captcha = req.POST['captcha']
        except:
            messages.add_message(req,messages.ERROR,'ورودی اشتباه')
            err = True
        if captcha != req.session['captcha']:
            messages.add_message(req,messages.ERROR,'کد اشتباه')
            err = True
        if err == False:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                if user.userprofile.isFullUser:
                    return HttpResponseRedirect(reverse('books:Home'))
                else:
                    return HttpResponseRedirect(reverse('userPanel:info'))
            else:
                messages.add_message(req,messages.ERROR,'نام کاربری یا رمز عبور اشتباه است')
        return render(req, 'user/login.html', context=self.context)

#register with number
@method_decorator(decorator=user_passes_test(checkNotLogin,login_url='/UserPanel/Info'),name='dispatch')
class registerUser(BaseViewClass):
    context = {}
    templateName = 'user/register.html'
    def GeneratePass(self):
        str = '1234567890'
        hash = ''
        for i in range(1, 5):
            hash += str[random.randrange(0, len(str))]
        return hash
    def GenerateInvCode(self,id):
        strr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@'
        hash = ''
        for i in range(1, 20):
            hash += strr[random.randrange(0, len(strr))]
        return hash + str(id)
    def post(self,req):
        error = False
        credit = 0
        if req.session.get('inviteCode') != None:
            credit = 5000
            invCode = req.session.pop('inviteCode')
            userP = UserProfile.objects.getUserByInvCode(invCode)
            if userP != None:
                userP.credit += 10000
                userP.save()
        try:
            phone = req.POST['phoneNumber']
            captcha = req.POST['captcha']
            req.session['phoneNumber'] = phone
            # req.session['phoneNumber'] = phone
            if captcha.upper() != req.session['captcha']:
                error = True
                messages.add_message(req,messages.ERROR,'کد اشتباه است')
            req.session.pop('captcha')

            #check phone number (ajax ui)
            if phone[0:2] == '09' and len(phone) == 11:
                try:
                    UserProfile.objects.get(phoneNumber=phone)
                    self.context['error'] = 'phoneNumberExists'
                except:
                    pass
            else:
                self.context['error'] = 'phoneNumberNotValid'

            if error == False:
                password = self.GeneratePass()
                print('firstpass = ' + str(password))
                req.session['code'] = password
                username = phone
                if sendSms(password,username,phone) == True:
                    req.session['sucRegister'] = True
                    return JsonResponse({'sendSms':True})
                else:
                    req.session['sucRegister'] = False
            else:
                time.sleep(1)
                return JsonResponse({'redirect': '/User/Register'})
        except Exception as err:
            print(err)
            messages.add_message(req,messages.ERROR,'ورودی اشتباه')
            time.sleep(1)
            return JsonResponse({'redirect':'/User/Register'})

    def get(self,req):
        if req.session.get('phoneNumber') != None:
            self.context['phoneNumber'] = req.session['phoneNumber']
        if req.GET.get('inviteCode') != None:
            req.session['inviteCode'] = req.GET.get('inviteCode')
        return render(req, self.templateName, context=self.context)

@method_decorator(decorator=user_passes_test(checkNotLogin,login_url='/UserPanel/Info'),name='dispatch')
class ValidateCode(View):
    def post(self,req):
        try:
            time.sleep(1)
            code = req.session['code']
            userCode = req.POST['code']
            print(userCode)
            print(code)
            if code == userCode: #checkTime
                return JsonResponse({'stat':'trueCode'})
            else:
                return JsonResponse({'stat':'wrongCode'})
        except:
            return JsonResponse({'stat':'wrongDataCode'})

@user_passes_test(checkNotLogin,login_url='/UserPanel/Info')
def checkUsername(req):
    if req.method == 'POST':
        try:
            username = req.POST['username']
            if username == '':
                return JsonResponse({'stat': 'noValidate'})
            UserProfile.objects.get(username=username)
            return JsonResponse({'stat':'userTaken'})
        except:
            return JsonResponse({'stat':'success'})





@method_decorator(decorator=user_passes_test(checkNotLogin,login_url='/UserPanel/Info'),name='dispatch')
class FillInfo(View):
    def post(self,req):
        print(req.POST)
        try:
            username = req.POST['username']
            try:
                UserProfile.objects.get(username=username)
                return JsonResponse({'stat':'userExists'})
            except:
                pass
            if userCharCheck(username) == False:
                return JsonResponse({'stat':'invalidUserChar'})
            name = req.POST['name']
            lastname = req.POST['lastname']
            password = req.POST['pass']
            if checkPass(password) == False:
                return JsonResponse({'stat':'invalidPass'})
            phoneNumber = req.session['phoneNumber']
            if username == '' or name == '' or lastname == '' or password == '' or phoneNumber == '':
                return JsonResponse({'stat':'wrongData'})
            statName,stat = nameAndLastnameCharCheck(name,lastname)
            if stat == False:
                if statName == 'name':
                    return JsonResponse({'stat':'invalidName'})
                if statName == 'lastname':
                    return JsonResponse({'stat':'invalidLastname'})
            user = User.objects.create_user(username=phoneNumber,password=password)
            user.first_name=name
            user.last_name=lastname
            user.save()
            userprofile = UserProfile(user=user,name=name,lastName=lastname,username=username,phoneNumber=phoneNumber)
            userprofile.isFullUser = True
            userprofile.save()
            userLogedIn = authenticate(username=phoneNumber, password=password)
            login(req, userLogedIn)
            return JsonResponse({'stat':'suc','redirect':'/Home'})
        except:
            return JsonResponse({'stat':'wrongData'})


def generateCaptcha():
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 5):
        rand_str += str1[random.randrange(0, len(str1))]
    return rand_str

#captcha
def getCaptcha(req):
    print('a')
    from PIL import Image, ImageDraw, ImageFont
    import random
    # print(rand_str)
    rand_str = generateCaptcha()
    req.session['captcha'] = rand_str
    print('done')
    bgcolor = (248, 249, 250)
    width = 500
    height = 100
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join(settings.STATIC_DIR, 'Yekan-full.ttf'), 80)
    for i in range(0,5):
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((i*100, 0), rand_str[i], font=font, fill=fontcolor)
    for i in range(0, 20):
        a = random.randrange(0,width)+i*3
        b = random.randrange(20,height-50)
        xy = [(a,b),(a+50,b+50)]
        fill = (random.randrange(0, 255), random.randrange(0,255), random.randrange(0, 255))
        draw.rectangle(xy,outline=fill)
    del draw
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')

#fill info

# def validateForm():


@login_required(login_url='/User/Login/')
def Logout(req):
    helpStat = req.session.get('help')
    logout(req)
    req.session['help'] = helpStat
    return HttpResponseRedirect(reverse_lazy('books:Home'))

def checkData(req):
    if len(req.POST) == 1:
        arg = list(req.POST.keys())[0]
        dt = req.POST[arg]
        if arg == 'username':
            try:
                User.objects.get(username=dt)
                return JsonResponse({'stat':'userIdExistError'})
            except Exception as e:
                return JsonResponse({'stat':'noError'})
        elif arg == 'phoneNumber':
            if dt[0:2] == '09' and len(dt) == 11:
                try:
                    UserProfile.objects.get(phoneNumber=dt)
                    return JsonResponse({'stat':'phoneExistError'})
                except:
                    pass
            else:
                return JsonResponse({'stat': 'phoneError'})
            return JsonResponse({'stat': 'noError'})
        elif arg == 'pass':
            try:
                validate_password(dt)
                return JsonResponse({'stat': 'noError'})
            except:
                return JsonResponse({'stat': 'passError'})
        else:
            return JsonResponse({'stat': 'argError'})
    else:
        return JsonResponse({'stat': 'argError'})


@login_required(login_url='/User/Login/')
def setProfilePic(req):
    if req.method == 'POST':
        userprofile = UserProfile.objects.getUserByUsername(req.user.username)
        # try:
        file = req.FILES['profilePic']
        if file.name.endswith('.jpg') or file.name.endswith('.png'):
            pPicurl = userprofile.profileImg.url.split(sep='/')
            pPicname = pPicurl[len(pPicurl)-1]
            fs = FileSystemStorage(location=settings.MEDIA_DIR)
            if pPicname != 'default.png':
                fs.delete(pPicname)
            filename = fs.save(file.name, file)
            path = os.path.join(settings.MEDIA_DIR,filename)
            userprofile.profileImg = path
            userprofile.save()
        else:
            messages.add_message(req, messages.ERROR, 'عکس با فرمت jpg یا png باشد')
        # except:
        messages.add_message(req,messages.ERROR,'ورودی اشتباه')
        return HttpResponseRedirect(reverse('userPanel:info'))










