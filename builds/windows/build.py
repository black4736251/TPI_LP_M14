import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=Loja_de_Carrinhos',
    '--noconfirm',
    '--clean',
    '--onefile',
    '--windowed',
    '--distpath=dist',
    '--workpath=build',
    '--add-data=../../app/resources/images;app/resources/images',
    '--add-data=../../app/resources/sounds;app/resources/sounds',
    '--add-data=../../app/views;app/views',
    '--add-data=../../app/controllers;app/controllers',
    '--add-data=../../app/services;app/services',
    '--add-data=../../app/models;app/models',
    '--add-data=../../app/core;app/core',
    '../../main.py'
])
