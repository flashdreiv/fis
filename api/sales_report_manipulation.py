from datetime import datetime

def get_purchase_list(purchases):
    data = {}
    for purchase in purchases:
        key = str(purchase.purchase_date.strftime('%B')) 
        if key in data:
            data[key] += purchase.item.price
        else:
            data[key] = purchase.item.price
    return data     