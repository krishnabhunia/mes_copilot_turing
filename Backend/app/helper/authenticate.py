

def authenticate_user(username='', password='', sessionToken='') -> bool:
    if username and password:
        if username == 'admin' and password == 'admin':
            return True
        else:
            us, pwd = get_username_password()
            if username == us and password == pwd:
                return True
            else:
                return False

    if sessionToken:
        if sessionToken == 'sessionToken':
            return True
        else:
            return False

    return False


def get_username_password():
    return 'krishna', 'bhunia'
