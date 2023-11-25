import os
from util.exception import NotAdminException


class Authentication():
    def check_admin_access(token):
        if token == os.getenv("ADMIN_KEY"):
            return True
        else:
            raise NotAdminException("User is not an admin")
        
