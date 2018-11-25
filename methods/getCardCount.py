from user.models import UserProfile,card,cardItem

def getItemsCount(req):
    count = 0
    try:
        user = UserProfile.objects.getUserByUsername(req.user.username)
    except:
        return count
    if user == None:
        return count
    try:
        userCard = user.card_set.get(status=0)
        allItems = userCard.carditem_set.all()
        for item in allItems:
            count += item.quanity
        return count
    except:
        return count