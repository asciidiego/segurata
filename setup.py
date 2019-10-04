import setuptools

from segurata import name as PKG_NAME

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=PKG_NAME,
    version="0.0.1",
    author="Diego Rodriguez, Sergio Pastor, Sara Fernandez",
    author_email="diego.vincent.rodriguez@gmail.com",
    description="Tool to extract data from login-based websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegovincent/segurata",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7',
)


"""Based on the following setup.py from the Python Software Foundation:
https://github.com/pypa/sampleproject/blob/388156a01d3ca549b25fdfbf6108072790d30b0a/setup.py
"""
