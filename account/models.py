from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.models import _user_get_permissions, _user_has_perm, _user_has_module_perms


class User(AbstractBaseUser, PermissionsMixin):

    # fields
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False, unique=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='Phone number')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    image = models.ImageField(verbose_name='Profile Picture', null=True, blank=True, upload_to='files/images/users')

    # permissions
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # settings
    USERNAME_FIELD = ['email']
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']
    objects = UserManager

    # methods
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email