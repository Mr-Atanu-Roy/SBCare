import random
import string

from accounts.models import UserToken


#func to generate random string of length=len
def generate_random_string(len):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(len))
    
    return random_string


def get_token_source(token):
    source = {
        'app-use':'sbcare-product', 
        'api-use':'api-service' 
    }
    token_role = 'api-use'
    
    token = token.replace('Token ', '')
    token_obj = UserToken.objects.filter(token=token).first()
    
    if token_obj:
        token_role = token_obj.role.lower()
    
    return source[token_role]

