from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="VPA",
    version="0.0.1",
    author="Prakash Tiwari",
    author_email="22f1000252@ds.study.iitm.ac.in",
    description="Vehicle Parking App V2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nyalazone/dce-platform",  # Example URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Users",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.10",
    install_requires=[
        "flask",
        "celery",
        "redis",
        # Add other dependencies here
    ],
    license="MIT"
)
