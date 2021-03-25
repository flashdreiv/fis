import uuid 
def generate_coupon_code(strPrefix):
    code = strPrefix+uuid.uuid4().hex[:9]
    return code
