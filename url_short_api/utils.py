import random
import string


#func to generate random string of length=len
def generate_random_string(len):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(len))
    
    return random_string
