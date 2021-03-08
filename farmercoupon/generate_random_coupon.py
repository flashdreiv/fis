import uuid 
def generate_coupon_code():
    code = 'ALJAY-'+uuid.uuid4().hex[:10]
    return code
