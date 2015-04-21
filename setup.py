from setuptools import setup, find_packages

setup(
    name='tunobase',
    version='1.1.24',
    description='Unomena Base Django Application',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read(),
    author='Unomena',
    author_email='dev@unomena.com',
    license='BSD',
    url='http://git.unomena.net/unomena/tunobase',
    packages = find_packages(),
    dependency_links = [
        'http://github.com/unomena/django-photologue/tarball/2.8.praekelt#egg=django-photologue-2.8.praekelt',
        'http://github.com/unomena/django-ckeditor-new/tarball/3.6.2.2#egg=django-ckeditor-3.6.2.2'
    ],
    install_requires = [
        'South',
        'django-polymorphic',
        'django-ckeditor==3.6.2.2',
        'django-photologue==2.8.praekelt',
        'django-preferences',
        'python-memcached',
        'celery==3.0.23',
        'django-celery==3.0.23',
        'django-honeypot',
        'Pillow',
        'facebook-sdk==0.4.0',
        'twython==3.1.0',
        'google-api-python-client==1.2',
        'flufl.password==1.2.1',
        'requests==2.0.0',
        'unidecode',
    ],
    tests_require=[
        'django-setuptest>=0.1.2',
        'pysqlite>=2.5',
	    'pycurl'
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
