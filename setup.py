from importlib.machinery import SourceFileLoader
import io
import os.path

from setuptools import find_packages, setup

sourcedml = SourceFileLoader("ml_core", "./ml_core/__init__.py").load_module()

with io.open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ml-core",
    description="Framework for machine learning on source code. "
    "Provides API and tools to train and use models based "
    "on source code features extracted from Babelfish's UASTs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=sourcedml.__version__,
    license="Apache 2.0",
    author="source{d}",
    author_email="machine-learning@sourced.tech",
    url="https://github.com/src-d/ml-core",
    download_url="https://github.com/src-d/ml-core",
    packages=find_packages(exclude=("ml_core.tests",)),
    namespace_packages=["ml_core"],
    keywords=[
        "machine learning on source code",
        "word2vec",
        "id2vec",
        "github",
        "swivel",
        "bow",
        "bblfsh",
        "babelfish",
    ],
    install_requires=[
        "PyStemmer>=1.3,<2.0",
        "bblfsh>=2.2.1,<3.0",
        "modelforge>=0.11.1,<0.13",
        "humanize>=0.5.0,<0.6",
        "pygments>=2.2.0,<3.0",
        "keras>=2.0,<3.0",
        "scikit-learn>=0.19,<1.0",
        "tqdm>=4.20,<5.0",
        "typing;python_version<'3.5'",
    ],
    extras_require={"tf": ["tensorflow>=1.0,<2.0"], "tf_gpu": ["tensorflow-gpu>=1.0,<2.0"]},
    tests_require=["docker>=3.6.0,<4.0"],
    package_data={"": ["LICENSE.md", "README.md"]},
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
)
