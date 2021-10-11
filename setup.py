import setuptools

long_description = """
A collection of modern flat themes inspired by Bootstrap. There are more than a dozen built-in themes, and you also have 
the ability to easily create your own.

## Links
- **Documentation:** https://ttkbootstrap.readthedocs.io/en/latest/  
- **GitHub:** https://github.com/israel-dryer/ttkbootstrap
"""

setuptools.setup(
    name="ttkbootstrap",
    version="1.0.0",
    author="Israel Dryer",
    author_email="israel.dryer@gmail.com",
    description="Provides expanded theme support to tkinter using bootstrap style keywords.",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/israel-dryer/ttk_framework",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["pillow>=8.2.0"],
    python_requires=">=3.7",
)
