from datetime import datetime

#Find self duplicates in dictionary
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


#Utility functions
def sort_by_month(data):
    months = list(dict.keys(data))
    months.sort(key=lambda date: datetime.strptime(date,'%B'))
    return months


#must call get_purchase_list first to remove duplicates
def merge_dict(dict1,dict2):
    final_dict = {}
    #Get all keys from two dictionary
    for x in {**dict1,**dict2}:
        final_dict[x] = 0
    #find all same key then add first dict
    for x in dict1:
        if x in final_dict:
            final_dict[x] += dict1[x]
    #find all same key then add second dict
    for x in dict2:
        if x in final_dict:
            final_dict[x] += dict2[x]

    sorted_key = sort_by_month(final_dict)
    tmp_dict = {}
    
    for x in sorted_key:
        tmp_dict[x] = ''

    for x in tmp_dict:
        if x in final_dict:
            tmp_dict[x] = final_dict[x]
    
    final_dict = tmp_dict

    return final_dict



