#coding:utf-8
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def permission_check(perms, login_url=None):
    """ permisson check """
    def check_perms(user):
        if user.is_authenticated():
            roles = user.role_set.all()
            user_perms = []
            for role in roles:
                user_perms.extend([perm.code for perm in role.perms.all()])
            if set(perms).issubset(set(user_perms)):
                return True
            else:
                raise PermissionDenied
        else:
            return False
        return False
    return user_passes_test(check_perms, login_url=login_url)