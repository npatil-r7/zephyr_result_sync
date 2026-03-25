from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zephyr-robotframework-listener",
    version="1.0.0",
    author="Nileshkumar Patil",
    author_email="npatil@rapid7.com",
    description="Robot Framework listener for Zephyr Scale Cloud integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/npatil-r7/zephyr_result_sync",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "robotframework>=6.0",
        "requests>=2.28.0",
        "pytz>=2023.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework",
    ],
)