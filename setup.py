from setuptools import setup, Extension
from Cython.Build import cythonize

# extensions = Extension('*', ['./*.pyx'])
extensions = cythonize(['bus.pyx', 'cpu.pyx'], language_level=3)

setup(
    python_requires='>=3.6',
    ext_modules = extensions,
)