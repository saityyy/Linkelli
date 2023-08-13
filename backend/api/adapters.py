from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class UserAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        user = super(
            UserAccountAdapter,
            self).save_user(
            request,
            user,
            form,
            commit=False)
        user.age = "22"
        user.save()
