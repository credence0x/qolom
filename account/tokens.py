from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

class SecondTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)+ six.text_type(
                user.businessProfile.pk)
        )
class ThirdTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(
                '863276bi&5%%qg#2@!$%^@^7duqq')+ six.text_type(timestamp) +
            six.text_type(user.is_active)
            )
account_activation_token = TokenGenerator()
account_activation_token_two = SecondTokenGenerator()
account_activation_token_three = ThirdTokenGenerator()
