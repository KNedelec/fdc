
def get_ok_code():
    ''' return the base ok code as a tuple '''
    return 0, "ok"

def get_baseerror_code(err_type, args):
    ''' return the base error code as a tuple '''
    return 1, err_type, args
