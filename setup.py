from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [Extension("*", ["./*.pyx"])]

setup(
	packages=find_packages(),
	ext_modules=cythonize(extensions, compiler_directives={"cdivision": True})#['cpu6502.pyx', 'BusClass.pyx'])
)