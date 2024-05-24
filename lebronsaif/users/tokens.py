from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type 
class ActivateEmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self,user, timestamp ):
        return(text_type(user)+text_type(timestamp)+text_type(user.is_verified))

account_activation_token = ActivateEmailToken()
