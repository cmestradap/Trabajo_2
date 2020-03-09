from distutils.core import setup
import py2exe 
import sys; sys.argv.append('py2exe')
   
py2exe_options = dict(
                       ascii=True,  # Exclude encodings
                       excludes=['_ssl',  # Exclude _ssl
                                'pyreadline', 'difflib', 'doctest', 'locale', 
                                 'optparse', 'pickle', 'calendar'],  # Exclude standard library
                       dll_excludes=['msvcr71.dll'],  # Exclude msvcr71
                       compressed=True,  # Compress library.zip
                       )
 
setup(name='<Registro>',
           version='1.0',
           description='<Control de usuarios>',
           author='Jose Alvarez', 
           windows = [
                {
                    "script": "registro.py",
                    "icon_resources": [(1, "unnamed.ico")]
                }
            ],
           options={'py2exe': py2exe_options},
)