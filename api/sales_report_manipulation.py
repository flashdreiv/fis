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

def get_purchase_list_item(purchases):
    data = {}
    for purchase in purchases:
        key = purchase.item.item_name
        if key in data:
            data[key] += purchase.item.price
        else:
            data[key] = purchase.item.price 
    return data   