from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from books.models import Categori
from user.models import UserProfile,Address
from django.views import View
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
from django.conf import  settings
from django.contrib import messages
from methods.getCardCount import getItemsCount
from BaseView.BaseView import BaseViewClass


# Create your views here.

Allowed = ['ا','ب','پ','ت','ث','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش',
        'ص','ض','ط','ظ','ع','غ','ف','ق','ک','ل','م','ن','و','ه','ی','گ',' ']

notAllowed = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o'
        ,'p','q','r','s','t','u','v','w','x','y','z',',','<','.','>','/',
              '?',"'",'"',';',':','\\','|',']','}','{','[','=','+','-','_','!','@','#','$'
              ,'%','^','&','*','(',')']

def getUserMainInfo(request):
    context = {}
    if request.user.userprofile.name == 'NULL':
        name = 'بدون نام'
        lastName = ''
    else:
        name = request.user.userprofile.name
        lastName = request.user.userprofile.lastName

    ADDR = Address.objects.filter(userProfile__id=request.user.userprofile.id)
    if len(ADDR) != 0:
        tphone = ADDR[0].telephone
        addr = ADDR[0].address
        pcode = ADDR[0].postCode
        ci = ADDR[0].city
        co = ADDR[0].country
    else:
        tphone = 'خالی'
        addr = 'خالی'
        pcode = 'خالی'
        ci = 'خالی'
        co = 'خالی'
    context = {'name': name,
                    'lastName': lastName,
                    'bio': request.user.userprofile.bio,
                    'profileImgUrl': request.user.userprofile.profileImg,
                    'phoneNumber': request.user.userprofile.phoneNumber,
                    'credit': request.user.userprofile.credit,
                    'gender': request.user.userprofile.Gender,
                    'telephone': tphone,
                    'address': addr,
                    'postCode': pcode,
                    'city': ci,
                    'country': co,
                    'credit': request.user.userprofile.credit,
                    'invCode': 'http://127.0.0.1:8000/User/Register/?inviteCode=' + request.user.userprofile.invCode,
                    'count': getItemsCount(request)
                    }
    return context

def checkFullUser(user):
    p = UserProfile.objects.getUserByUsername(user.username)
    if p == None:
        return False
    return UserProfile.objects.getUserByUsername(user.username).isFullUser and user.is_authenticated

def checkAuthenticated(user):
    return user.is_authenticated

def checkLang(names):
    for name in names:
        for char in name:
            if char in notAllowed:
                return False
    return True

def checkNumbersValue(value,lentgh):
    if len(value) != lentgh:
        return False
    try:
        int(value)
    except:
        return False
    return True

#
@method_decorator(user_passes_test(checkAuthenticated,login_url='/User/Register/'),name='dispatch')
class info(BaseViewClass):
    templateName = 'userPanel/info.html'
    context = {}
    def dispatch(self, request, *args, **kwargs):
        self.context = getUserMainInfo(request)
        return super().dispatch(request,*args,**kwargs)

    def get(self,req):
        self.context['menu'] =  Categori.object.getAllCats()
        return render(req, 'userPanel/info.html', context=self.context)

    def post(self,req):
        err = False
        user = UserProfile.objects.getUserByUsername(req.user.username)
        try:
            username = req.POST.get('username')
            if username == None:
                username = ''
            city = req.POST['city']
            country = req.POST['country']
            name = req.POST['name']
            gender = int(req.POST['gender'])
            lastName = req.POST['lastName']
            number = req.POST['number']
            postCode = req.POST['postCode']
            address = req.POST['address']
            if checkLang([name,lastName,address]) == False:
                err = True
                self.context['messageType'] = 'alert-danger'
                messages.add_message(req, messages.ERROR, 'لضفا زبان فارسی وارد نمایید')
            if checkNumbersValue(postCode,10) == False:
                self.context['messageType'] = 'alert-danger'
                err = True
                messages.add_message(req, messages.ERROR, 'کد پستی اشتباه ')
            if checkNumbersValue(number, 11) == False:
                self.context['messageType'] = 'alert-danger'
                err = True
                messages.add_message(req, messages.ERROR, 'شماره اشتباه اشتباه ')

            if gender != 1 and gender != 0:
                self.context['messageType'] = 'alert-danger'
                err = True
                messages.add_message(req, messages.ERROR, 'جنسیت اشتباه ')
            print(err)
            if err == False:
                user.name = name
                user.lastName = lastName
                user.telephone = number
                user.postCode = postCode
                user.address = address
                user.Gender = gender
                user.city = city
                user.country = country
                ADDR = Address.objects.filter(userProfile__id = req.user.userprofile.id)
                print(len(ADDR))
                if len(ADDR) == 0:
                    ADDR = Address(userProfile=UserProfile.objects.getUserByUsername(req.user.username),telephone=number,postCode=postCode,address=address,city=city,country=country)
                    ADDR.save()
                else:
                    ADDR[0].telephone = number
                    ADDR[0].postCode = postCode
                    ADDR[0].address = address
                    ADDR[0].city = city
                    ADDR[0].country = country
                    ADDR[0].save()
                user.isFullUser = True
                user.save()
                self.context['name'] = name
                self.context['lastName'] = lastName
                self.context['telephone'] = number
                self.context['postCode'] = postCode
                self.context['address'] = address
                self.context['gender'] = gender
                self.context['city'] = city
                self.context['country'] = country
                self.context['messageType'] = 'alert-success'
                messages.add_message(req,messages.SUCCESS,'اضلاعات ثبت شد')
        except Exception as err:
            messages.add_message(req,messages.ERROR,err)
        return render(req, 'userPanel/info.html', context=self.context)


# @user_passes_test(checkAuthenticated,login_url='/User/Login/')
# def info(req):
#
#     return render(req,'userPanel/info.html',context={'menu':Categori.object.getAllCats()})

def checkNumber(number):
    for char in number:
        if char not in [0,1,2,3,4,5,6,7,8,9,'0','1','2','3','4','5','6','7','8','9']:
            return False
    return True

@method_decorator(user_passes_test(checkAuthenticated,login_url='/User/Register/'),name='dispatch')
class address(BaseViewClass):
    context = {}
    def dispatch(self, request, *args, **kwargs):
        self.context = getUserMainInfo(request)
        return super().dispatch(request,*args,**kwargs)
    def get(self,req):
        usr = UserProfile.objects.getUserByUsername(req.user.username)
        addresses = usr.address_set.all()
        self.context['allAddress'] = addresses
        return render(req,'userPanel/address.html',context=self.context)
    def post(self,req):
        try:
            id = int(req.POST['id'])
            phone = req.POST['number']
            city = req.POST['city']
            country = req.POST['country']
            code = req.POST['postCode']
            address = req.POST['address']
            if phone == ''  or city  == '' or  country  == '' or code  == '' or address == '':
                messages.add_message(req, messages.WARNING, 'ورودی اشتباه')
                return JsonResponse({'redirect': '/UserPanel/Address/'})
            if checkLang([city,country,address]) == False:
                messages.add_message(req,messages.WARNING,'ادرس و شهر و استان را فارسی وارد کنید')
                return JsonResponse({'redirect':'/UserPanel/Address/'})
            if checkNumbersValue(phone,11)==False or checkNumber(phone) == False:
                messages.add_message(req, messages.WARNING, 'شماره تلفن فقط اعداد و 11 رقم باشد')
                return JsonResponse({'redirect': '/UserPanel/Address/'})
            if checkNumbersValue(code,10)==False or checkNumber(code) == False:
                messages.add_message(req, messages.WARNING, 'کد پستی فقط اعداد و 11 رقم باشد')
                return JsonResponse({'redirect': '/UserPanel/Address/'})
            if id == -1:
                ADDR = Address(telephone=phone,city=city,country=country,postCode=code,address=address,
                           userProfile=UserProfile.objects.getUserByUsername(req.user.username))
                ADDR.save()
                return JsonResponse({'stat':'success'})
            else:
                ADDR = Address.objects.get(id=id)
                ADDR.telephone = phone;ADDR.city=city;ADDR.country=country;ADDR.postCode=code;ADDR.address=address
                ADDR.save()
                return JsonResponse({'stat': 'success'})
        except Exception as Err:
            print(Err)
            messages.add_message(req,messages.WARNING,'ورودی اشتباه')
            return JsonResponse({'redirect': '/UserPanel/Address/'})

@user_passes_test(checkAuthenticated,login_url='/User/Register/')
def deleteAddr(req):
    if req.method == 'GET':
        try:
            id = int(req.GET['id'])
            try:
                addr = Address.objects.get(id=id)
                addr.delete()
                return JsonResponse({'stat':'success'})
            except Exception as er:
                messages.add_message(req,messages.ERROR,'خطا')
                return JsonResponse({'stat': 'err'})
        except Exception as err:
            messages.add_message(req, messages.ERROR, 'خطا')
            return JsonResponse({'stat': 'err'})


@user_passes_test(checkAuthenticated,login_url='/User/Register/')
def getAddr(req):
    if req.method == 'GET':
        try:
            id = int(req.GET['id'])
            try:
                addr = Address.objects.get(id=id)
            except:
                return JsonResponse({'addr':'err'})
            return JsonResponse({'addr':addr.address,'phone':addr.telephone,'postcode':addr.postCode,
                                 'country':addr.country,'city':addr.city})
        except Exception as err:
            return JsonResponse({'addr':'err'})
