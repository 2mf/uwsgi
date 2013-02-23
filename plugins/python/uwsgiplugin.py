import os,sys

from distutils import sysconfig

def get_python_version():
    version = sysconfig.get_config_var('VERSION')
    try:
        version = version + sys.abiflags
    except:
        pass
    return version

NAME='python'
GCC_LIST = ['python_plugin', 'pyutils', 'pyloader', 'wsgi_handlers', 'wsgi_headers', 'wsgi_subhandler', 'web3_subhandler', 'pump_subhandler', 'gil', 'uwsgi_pymodule', 'profiler', 'symimporter', 'tracebacker']

CFLAGS = ['-I' + sysconfig.get_python_inc(), '-I' + sysconfig.get_python_inc(plat_specific=True) ] 

if 'pypy_version_info' in sys.__dict__:
    CFLAGS.append('-DUWSGI_PYPY')

LDFLAGS = []

if not 'UWSGI_PYTHON_NOLIB' in os.environ:
    LIBS = sysconfig.get_config_var('LIBS').split() + sysconfig.get_config_var('SYSLIBS').split()
    # check if it is a non-shared build (but please, add --enable-shared to your python's ./configure script)
    if not sysconfig.get_config_var('Py_ENABLE_SHARED'):
        libdir = sysconfig.get_config_var('LIBPL')
        # libdir does not exists, try to get it from the venv
        if not os.path.exists(libdir):
            libdir = '%s/lib/python%s/config' % (sys.prefix, get_python_version())
        libpath = '%s/%s' % (libdir, sysconfig.get_config_var('LDLIBRARY'))
        if not os.path.exists(libpath): 
            libpath = '%s/%s' % (libdir, sysconfig.get_config_var('LIBRARY'))
        if not os.path.exists(libpath): 
            libpath = '%s/libpython%s.a' % (libdir, get_python_version())
        LIBS.append(libpath)
    else:
        try:
            LDFLAGS.append("-L%s" % sysconfig.get_config_var('LIBDIR'))
            os.environ['LD_RUN_PATH'] = "%s" % (sysconfig.get_config_var('LIBDIR'))
        except:
            LDFLAGS.append("-L%s/lib" % sysconfig.PREFIX)
            os.environ['LD_RUN_PATH'] = "%s/lib" % sysconfig.PREFIX

        LIBS.append('-lpython%s' % get_python_version())
else:
    LIBS = []
