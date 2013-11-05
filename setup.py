# -*- coding: utf-8 -*-
from distutils.core import setup


setup(  name = "python-netinterfaces",
        version  = "0.1",
        author  = "Raul Rodrigo Segura",
        author_email = "raurodse@gmail.com",
        license="GPL", 
        py_modules = ['netinterfaces'],
        data_files = [('/usr/bin/',['enablenat'])]
     )