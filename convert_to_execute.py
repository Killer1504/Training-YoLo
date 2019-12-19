import PyInstaller.__main__
import os
PyInstaller.__main__.run([
    '--name=%s' % "ObjectDetection",
    '--onefile',
    '--windowed',
    os.path.join('helloVietNam.py'),
])