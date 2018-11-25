from django.shortcuts import render,redirect
from zeep import Client
from django.http import HttpRequest,HttpResponse
from user.models import card
# Create your tests here.
api_key = '0d3a65e6-3b64-44d6-aa8a-86dccd2c7339'
client = Client('http://api.nextpay.org/gateway/token.wsdl')
client_check = Client('http://api.nextpay.org/gateway/verify.wsdl')
CallbackURL = 'http://127.0.0.1:8000/pay/Verify/'

def Buy(request):
    try:
        cardId = request.POST['cardId']
    except:
        return HttpResponse('error')
    try:
        userCard = card.objects.get(cardId=cardId)
        userCard.status = 2
        userCard.save()
    except:
        return HttpResponse('WRONG')
    if userCard.status == 2 or userCard.status == 4:
        result = client.service.TokenGenerator(api_key,cardId,userCard.getFinalPrice(), CallbackURL)
        userCard.TransId = result.trans_id
        userCard.save()
        if result.code == -1:
            return redirect('https://api.nextpay.org/gateway/payment/' + str(result.trans_id))
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    else:
        return HttpResponse('not on pay')

def Verify(request):
    if request.method == 'POST':
        trans_id = request.POST['trans_id']
        cardId = request.POST['order_id']
        userCard = card.objects.get(cardId=cardId)
        if userCard.TransId == trans_id:
            result = client_check.service.PaymentVerification(api_key,cardId,userCard.getFinalPrice(),trans_id)
            if result.code == 0:
                userCard.status = 4
                userCard.payedPrice = userCard.getFinalPrice()
                userCard.discountPrice = userCard.getCardDiscount()
                userCard.save()
                return HttpResponse('Done')
            else:
                userCard.status = 5
                userCard.save()
                return HttpResponse('Not done')
        else:
            return HttpResponse('Err')
    else:
        return HttpResponse('Not a post')
