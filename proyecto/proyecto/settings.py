from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v*8b00oiqh3014l#knir-lmnjig5diyc_^pizufayeqs+f-kdn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        
    'ckeditor',
        
    'django.contrib.sites',  # Necesario para allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # Necesario si quieres habilitar autenticación social
    # 'allauth.socialaccount.providers.google',  # Ejemplo para habilitar Google como proveedor social
    
    'users', # Agregamos el app "users"
    'contenido', # Agregamos el app "contenido"
    'categorias', # Agregamos el app "categorias"

    
]

CKEDITOR_UPLOAD_PATH = "uploads/"

# Especifica el ID del sitio, necesario para django-allauth
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
    
]

ROOT_URLCONF = 'proyecto.urls'

# Configuración de la ruta de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Directorio donde están tus plantillas personalizadas
        'APP_DIRS': True,  # Permite que Django busque plantillas en las carpetas templates de las apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Opcional: configuración para archivos cargados por los usuarios (media)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'proyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'leticia',
        'USER': 'postgres',
        'PASSWORD': '13100864',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Para allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend predeterminado de Django
    'allauth.account.auth_backends.AuthenticationBackend',  # Backend de allauth
]
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Permite iniciar sesión con nombre de usuario o email
ACCOUNT_EMAIL_REQUIRED = True  # El correo electrónico es obligatorio
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Verificación de email obligatoria
ACCOUNT_USERNAME_REQUIRED = True  # El nombre de usuario también es obligatorio
# Redirige después del login según el rol del usuario
LOGIN_REDIRECT_URL = '/dashboard/'
  # Redirige a la página principal después de iniciar sesión
LOGOUT_REDIRECT_URL = '/'  # Redirige a la página principal después de cerrar sesión
ACCOUNT_SIGNUP_FORM_CLASS = None  # Si deseas utilizar un formulario de registro personalizado
ACCOUNT_FORMS = {'signup': 'users.forms.CustomSignupForm'}
# Configuración del modelo de usuario personalizado
AUTH_USER_MODEL = 'users.CustomUser'

# Configuración del backend de correo para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Configuración de correo para envío de campos en contacto
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '2024g5is2@gmail.com'
EMAIL_HOST_PASSWORD = 'leti1168'
# Configuración de correo para envío de campos en contacto
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '2024g5is2@gmail.com'
EMAIL_HOST_PASSWORD = 'leti1168'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Asuncion'  # Ajusta según tu zona horaria

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Ruta para los archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#CONFIGURACION DEL CRON(Automatizacion de Publicaciones)

CRON_CLASSES = [
    "contenido.cron.AutopublicarContenido",
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django_cron': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

#pasarela de pago stripe

#keys de la cuenta
STRIPE_TEST_PUBLIC_KEY = 'pk_test_51Q2vVqHgGd0NSdDUyHvjPNnMVJMnU0aJr99r1H9ieaSQVJ8v2Hy4YE1SuGVXLBvmYuhtsr9AuOxVzL14GamULDV800cA7xb7tF'
STRIPE_TEST_SECRET_KEY = 'sk_test_51Q2vVqHgGd0NSdDU0Z6C88f88yR9lcB4h5tWPlYmdvf8hidhkuMNwQ989Vo8HlQo16NtpVeq9J5UgGVUJQFXZz4A007crMVl5X'



SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_AGE = 1209600  # 2 semanas, en segundos para que no se desloguee el usuario al pasar a stripe
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # No expira cuando se cierra el navegador



#pasarela de pago stripe

#keys de la cuenta
STRIPE_TEST_PUBLIC_KEY = 'pk_test_51Q2vVqHgGd0NSdDUyHvjPNnMVJMnU0aJr99r1H9ieaSQVJ8v2Hy4YE1SuGVXLBvmYuhtsr9AuOxVzL14GamULDV800cA7xb7tF'
STRIPE_TEST_SECRET_KEY = 'sk_test_51Q2vVqHgGd0NSdDU0Z6C88f88yR9lcB4h5tWPlYmdvf8hidhkuMNwQ989Vo8HlQo16NtpVeq9J5UgGVUJQFXZz4A007crMVl5X'



SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_AGE = 1209600  # 2 semanas, en segundos para que no se desloguee el usuario al pasar a stripe
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # No expira cuando se cierra el navegador

