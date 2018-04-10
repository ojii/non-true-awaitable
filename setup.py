from setuptools import setup, find_packages


setup(
    version="18.4",
    name="non-true-awaitable",
    package_dir={"": "src"},
    py_modules=["nta"],
    license="APLv2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
