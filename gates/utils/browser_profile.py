
import random
import string
import tempfile

def generate_profile():
    rand_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    user_data_dir = tempfile.TemporaryDirectory(prefix=rand_name)
    return user_data_dir.name

