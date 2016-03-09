# 
# This is an example of a local settings file.
# 
# Copy it to "local_settings.py" and modify it to suit your needs.
# 
# It is ignored by git, so you don't have to worry about accidentally checking
# in any secrets.
# 



# Uncomment and change these before running in production!
# Seriously, do NOT run a live site with DEBUG or the default SECRET_KEY

#DEBUG=False
#SECRET_KEY='a long random string here'
#ALLOWED_HOSTS=['example.com']



# Database configuration
# Note: Databases other than PostgreSQL are NOT supported!

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'korform',
#         'USER': 'korform',
#         'PASSWORD': 'korform',
#         'HOST': '127.0.0.1',
#     }
# }


# Email credentials
# By default, it will connect to localhost:25 with no auth

DEFAULT_FROM_EMAIL = "noreply@example.com"
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 465
#EMAIL_USE_SSL = True
#EMAIL_USE_TLS = False
#EMAIL_HOST_USER = 'myusername'
#EMAIL_HOST_PASSWORD = 'mypassword'
#EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'



# Common security features
# You may or may not want to tweak these, but they're good production defaults

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# If the application is only accessible via https, these make it more secure
# Note that it will also break logins on non-https connections

#SESSION_COOKIE_SECURE=True
#CSRF_COOKIE_SECURE=True
