from datetime import datetime

def get_month_list(purchases):
    months = []
    for purchase in purchases:
        months.append(str(purchase.purchase_date.strftime('%B')))
    months = list(dict.fromkeys(months))
    return months