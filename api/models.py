from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.core import validators
from django.utils.translation import ugettext_lazy as _


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('Tələb olunur. 100 simvol və ya az. Hərflər, Rəqəmlər və '
                                            '@/./+/-/_ simvollar.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Düzgün istifadəçi adı daxil edin.'),
                                                              'yanlışdır')
                                ])
    full_name = models.CharField(_('Full name'), max_length=255, blank=True)
    # last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)
    # profile_picture = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    # gender = models.IntegerField(choices=GENDER, verbose_name="cinsi", null=True, blank=True)
    # place = models.IntegerField(default=0)
    # is_play = models.BooleanField(default=False)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)#



    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


    def friends(self):
        return [
            obj.from_user for obj in
            self.my_friends.all()
        ]

    def my_wishes(self):
        return self.author_of_wish.all()

    def incoming_wishes(self):
        return self.wish_target.all()



class Friends(models.Model):
    from_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='other_friends')
    to_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_friends')


class Wishes(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='author_of_wish')
    content = models.CharField(max_length=1000, null=False)
    url_image = models.URLField(null=True)
    url_video = models.URLField(null=True)


    def targets(self):
        return self.wishtarget_set.all()


class WishTarget(models.Model):
    target = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="wish_target")
    wish = models.ForeignKey(Wishes, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    next = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="next_target")

