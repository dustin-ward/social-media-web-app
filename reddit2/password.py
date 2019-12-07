def salt_password(password):
    i = 0
    pass_arr = []
    for char in password:
        i += 1
        pass_arr.append(char)
        if i % 2 == 0:
            pass_arr.append('$$%$')
    return ''.join(pass_arr)
