from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import user_passes_test
from user.models import UserProfile,card,cardItem
from books.models import Book
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from BaseView.BaseView import BaseViewClass
from django.utils import timezone
# Create your views here.

def checkFullUser(user):
    p = UserProfile.objects.getUserByUsername(user.username)
    if p == None:
        return False
    return UserProfile.objects.getUserByUsername(user.username).isFullUser and user.is_authenticated

def checkAuthenticated(user):
    return user.is_authenticated

class addItem(View):
    def post(self,req):
        try:
            reqUser = req.user
            if checkFullUser(reqUser) == False:
                messages.add_message(req,messages.ERROR,'برای خرید باید وارد حساب خود شوید یا ثبت نام کنید')
                return JsonResponse({'stat':'redirect','url':'/User/Register/'})
        except:
            return JsonResponse({'stat': 'redirect', 'url': '/User/Register/'})
        bookId = req.POST.get('bookId')
        quanity = req.POST.get('quanity')
        user = UserProfile.objects.getUserByUsername(req.user.username)
        if user == None or bookId == None:
            return JsonResponse({'stat':'err'})
        try:
            book = Book.objects.get(id=bookId)
        except:
            return JsonResponse({'stat':'bookNotFound'})
        try:
            quanity = int(quanity)
        except:
            quanity = 1
        try:
            userCard = user.card_set.get(status=0)
        except:
            userCard = card(status=0,user=user)
            userCard.save()
        try:
            item = userCard.carditem_set.get(book__id=bookId)
            item.quanity += quanity
            item.save()
        except:
            item = cardItem(quanity=1,book=book,itemCard=userCard)
            item.save()
        return JsonResponse({'stat':'done'})


@method_decorator(decorator=user_passes_test(checkFullUser,login_url='/UserPanel/Info'),name='dispatch')
class removeItem(View):
    def post(self,req):
        try:
            reqUser = req.user
            if checkFullUser(reqUser) == False:
                messages.add_message(req,messages.ERROR,'برای خرید باید وارد حساب خود شوید یا ثبت نام کنید')
                return JsonResponse({'stat':'redirect','url':'/User/Register/'})
        except:
            messages.add_message(req, messages.ERROR, 'برای خرید باید وارد حساب خود شوید یا ثبت نام کنید')
            return JsonResponse({'stat': 'redirect', 'url': '/User/Register/'})
        try:
            id = req.POST['id']
            user = UserProfile.objects.getUserByUsername(req.user.username)
            userCard = user.card_set.get(status=0)
            item = userCard.carditem_set.get(book_id=id)
            item.delete()
            return JsonResponse({'stat':'deleted'})
        except Exception as err:
            print(err)
            return JsonResponse({'stat':'error'})



@method_decorator(decorator=user_passes_test(checkFullUser,login_url='/UserPanel/Info'),name='dispatch')
class viewCard(BaseViewClass):
    context = {}
    def get(self,req):
        try:
            user = UserProfile.objects.getUserByUsername(req.user.username)
            addrs = user.address_set.all()
            if len(addrs) > 0:
                self.context['allAddress'] = addrs
            userCard = user.card_set.get(status=0)
            allPrice = userCard.getCardPriceWithDiscount()
            allDiscount = userCard.getCardDiscount()
            userCardItems = userCard.carditem_set.all()
            self.context['card'] = userCard
            self.context['userProfile'] = user
            self.context['purchaseList'] = userCardItems
            self.context['allPrice'] = allPrice
            self.context['allDiscount'] = allDiscount
        except Exception as err:

            self.context['purchaseList'] = 'empty'
        if self.context['purchaseList'] != 'empty' and len(self.context['purchaseList']) == 0:
            self.context['purchaseList'] = 'empty'

        return render(req,'order/viewOrderCard.html',self.context)

class changeQuantity(View):
    def post(self,req):
        try:
            itemId = req.POST['itemId']
            quantity = int(req.POST['quantity'])
            user = UserProfile.objects.getUserByUsername(req.user.username)
            userCard = user.card_set.get(status=0)
            userCardItem = userCard.carditem_set.get(id=itemId)
            userCardItem.quanity = quantity
            userCardItem.save()
            return JsonResponse({'stat':'done'})
        except Exception as err:
            return JsonResponse({'stat':'error'})



@user_passes_test(checkFullUser,login_url='/UserPanel/Info')
def getOrderInfo(req):
    return HttpResponse('orderinfo')

@method_decorator(decorator=user_passes_test(checkFullUser,login_url='/UserPanel/Info'),name='dispatch')
class orderConfirm(BaseViewClass):
    context = {}
    def checkTamin(self,allItems):
        for item in allItems:
            if item.book.inventory == False:
                print(item.book)
                return False
        return True

    def get(self,req,cardId):
        def calculatePostPrice(weight):
            return weight * 10
        try:
            usr = UserProfile.objects.getUserByUsername(username=req.user.username)
            card = usr.card_set.get(cardId = cardId)
            allCards = card.carditem_set.all()
            cardItemCount = card.carditem_set.count()
            allWeight = card.getCardWeight()
            # ;self.context['allWeight'] = allWeight
            postPrice = calculatePostPrice(allWeight)
        except:
            messages.add_message(req,messages.ERROR,'شماره سفارش اشتباه میشود')
            return redirect(reverse('shoppingCard:viewCard'))
        try:
            self.context['allCard'] = allCards
            self.context['card'] = card
            self.context['cardItemCount'] = cardItemCount
            self.context['postPrice']=postPrice
            addrs = usr.address_set.all()
            if len(addrs) > 0:
                self.context['allAddress'] = addrs
            return render(req,'order/orderConfirm.html',context=self.context)
        except:
            messages.add_message(req, messages.ERROR, 'خطای سیستم لطفا با پشتیبانی تماس بگیرید')
            return redirect(reverse('shoppingCard:viewCard'))
    def post(self,req):
        try:
            addrId = req.POST['addrId']
            postId = req.POST['postId']
            usr = UserProfile.objects.getUserByUsername(username=req.user.username)
            card = usr.card_set.get(status=0)
            card.userAddrId = int(addrId)
        except:
            messages.add_message(req, messages.ERROR, 'ادرس و نوع ارسال را انتخاب کنید')
            return redirect(reverse('shoppingCard:viewCard'))
        try:

            if postId == 'one':
                postId = 1
            elif postId == 'two':
                postId = 2
            elif postId == 'three':
                postId = 3
            card.postId = postId
            card.orderDate = timezone.now()
            if self.checkTamin(card.carditem_set.all()) == False:
                card.status = 1
                card.save()
                return HttpResponse('wait')
            return redirect(reverse('shoppingCard:orderConfirm',kwargs={'cardId':str(card.cardId)}))
        except:
            messages.add_message(req, messages.ERROR,'خطای سیستم لطفا با پشتیبانی تماس بگیرید')
            return redirect(reverse('shoppingCard:viewCard'))

@user_passes_test(checkFullUser,login_url='/UserPanel/Info')
def orderPay(req):
    return HttpResponse('pay')