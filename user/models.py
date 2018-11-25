from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from books.models import Book
import time,random
from  django.core.exceptions import ValidationError,FieldError
from django.utils import timezone

defaultUserImg= '/media/default.png'


stats = {0:'در سبد خرید' ,1:'در حال بررسی',2:'اماده پرداخت',3:'برداخت موفق',5:'عدم پرداخت',4:'برداخت ناموفق',6:'ارسال شده'}


fs = FileSystemStorage(location=os.path.join('Statics',settings.BASE_DIR))

class UserprofileManager(models.Manager):
    def getUserByUsername(self,username):
        try:
            return self.get(user__username=username)
        except:
            return None
    def getUserByInvCode(self,inv):
        try:
            return self.get(invCode=inv)
        except:
            return None

def getCardId():
    def generateCode():
        code = ''
        for p in range(1,5):
            code += str(random.randrange(1,10))
        return code
    lastId = card.objects.all().order_by('cardId').last()
    code = generateCode()
    if not lastId:
        newId = 'BR'+code+'0'
    else:
        lastId = str(int(lastId.cardId[5])+1)
        newId = 'BR'+code+lastId
    return newId

class card(models.Model):
    payedPrice = models.DecimalField(max_digits=6,decimal_places=0,default=0)
    discountPrice = models.DecimalField(max_digits=6,decimal_places=0,default=0)
    discountCodePrice = models.DecimalField(max_digits=6,decimal_places=0,default=0)
    TransId = models.CharField(null=True,max_length=100)
    orderDate = models.DateField(null=True)
    status = models.SmallIntegerField(choices=((a,b) for a,b in stats.items()),default=0)
    postCode = models.CharField(max_length=20,blank=True)
    userAddrId = models.SmallIntegerField(default=-1)
    postId = models.SmallIntegerField(default=0)
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    cardId = models.CharField(max_length=20,default=getCardId,editable=False,primary_key=True)
    def __str__(self):
        return self.cardId

    # def save(self, *args,**kwargs):
    #     try:
    #         card.objcets.get(status=0)
    #         return super(Book, self).save(*args, **kwargs)
    #     except:
    #         raise ValidationError('ridiii')

    def getFinalPrice(self):
        postPrice = self.calculatePostPrice()
        if self.postId == 1:
            postPrice = postPrice['one']
        elif self.postId == 2:
            postPrice = postPrice['two']
        else:
            postPrice = postPrice['three']

        return (postPrice + self.getCardPriceWithDiscount()) - int(self.discountCodePrice)

    def calculatePostPrice(self): #later
        return {'one':self.getCardWeight() * 2,'two':self.getCardWeight() * 3,'three':self.getCardWeight() * 4}

    def getCardRealPrice(self): # get price of all items without discount
        price = 0
        allItems = self.carditem_set.all()
        for item in allItems:
            price += item.getRealItemPrice()
        return price
    def getCardPriceWithDiscount(self): # get price of all items with discount
        price = 0
        allItems = self.carditem_set.all()
        for item in allItems:
            price += item.getItemPriceWithDiscount()
        return price
    def getCardDiscount(self): #get all card discount
        discount = 0
        allItems = self.carditem_set.all()
        for item in allItems:
            discount += item.getItemDiscount()
        return discount
    def getCardWeight(self):
        weight = 0
        allItems = self.carditem_set.all()
        for item in allItems:
            weight += int(item.getItemWeight())
        return weight


class cardItemManager(models.Manager):
    def getItemPrice(self):
        return self.quanity * self.book.price


class cardItem(models.Model):
    quanity = models.DecimalField(max_digits=3,decimal_places=0,default=1)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    itemCard = models.ForeignKey('card',on_delete=models.CASCADE)
    objects = cardItemManager()
    def __str__(self):
        return self.book.name

    def getRealItemPrice(self):
        return int(self.quanity) * self.book.getRealPrice()

    def getItemPriceWithDiscount(self): #get card item all price with discount
        return int(self.quanity) * self.book.calculatePriceWithDiscount()['price']

    def getItemDiscount(self):#get item discount with quanity
        return int(int(self.quanity)*self.book.getBookDiscount())

    def getItemWeight(self):
        try:
            return int(int(self.book.weight) * int(self.quanity))
        except Exception as err:
            return 0

class Address(models.Model):
    telephone = models.CharField(max_length=11,default='NULL')
    address = models.CharField(max_length=300,default='NULL')
    postCode = models.CharField(max_length=10,default='NULL')
    city = models.CharField(max_length=25,blank=True)
    country =models.CharField(max_length=25,blank=True)
    userProfile = models.ForeignKey('UserProfile',models.CASCADE)
    def __str__(self):
        return str(self.id)
    def returnFullAddress(self):
        def tokenizeAddress(addr):
            return addr.replace(' ',' , ')
        return 'استان ' + self.country + ' , ' + 'شهرستان '+ self.city + ' , ' +  'ادرس ' + tokenizeAddress(self.address)


class UserProfile(models.Model):
    invCode = models.CharField(max_length=20,default='NULL')
    name = models.CharField(max_length=20,blank=False,default='NULL')
    lastName = models.CharField(max_length=15,blank=False,default='NULL')
    bio = models.TextField(max_length=500,blank=True)
    profileImg = models.ImageField(storage=fs,upload_to=settings.MEDIA_DIR,default=defaultUserImg,blank=True)
    phoneNumber = models.CharField(max_length=11,null=False,blank=False)
    credit = models.DecimalField(max_digits=7,decimal_places=0,default=0)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    isFullUser = models.BooleanField(default=False)
    Gender = models.SmallIntegerField(default=0,choices=((0,'مرد'),(1,'زن')))
    birthDay = models.DecimalField(max_digits=2,blank=True,decimal_places=0,default=0)
    birthMonth = models.DecimalField(max_digits=2,blank=True,decimal_places=0,default=0)
    mirthYear = models.DecimalField(max_digits=4,blank=True,decimal_places=0,default=0)
    username = models.CharField(max_length=20,blank=False,null=False,unique=True)
    objects = UserprofileManager()
    def __str__(self):
        if self.name == 'NULL' and self.lastName == 'NULL':
            return str(self.user.username)
        else:
            return self.name + ' ' +self.lastName

