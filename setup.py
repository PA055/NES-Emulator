from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = Extension("cycore.*", ['NES/cycore/*.pyx']),
extensions = cythonize(extensions, compiler_directives={"language_level": 3, "profile": False, "boundscheck": False, "nonecheck": False, "cdivision": True}, annotate=True)

setup(
	ext_modules=extensions
)