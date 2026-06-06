import os
import ssl

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend


class FixedSMTPEmailBackend(EmailBackend):
    """SMTP backend with SSL context suited for local Windows/dev environments."""

    @property
    def ssl_context(self):
        if settings.DEBUG or os.getenv('EMAIL_SSL_INSECURE') == 'true':
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            return context
        return super().ssl_context
