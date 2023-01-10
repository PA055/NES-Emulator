from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [Extension("*", ["./*.pyx"])]

setup(
	packages=find_packages(),
	ext_modules=cythonize(extensions, compiler_directives={"language_level": 3, "profile": False, "boundscheck": False, "nonecheck": False, "cdivision": True})#['cpu6502.pyx', 'BusClass.pyx'])
)