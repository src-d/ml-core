from importlib.machinery import SourceFileLoader
import io
import os.path

from setuptools import find_packages, setup

sourcedml = SourceFileLoader("sourced-ml-core", "./sourced/ml/core/__init__.py").load_module()

with io.open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

include_tests = os.getenv("ML_CORE_SETUP_INCLUDE_TESTS", False)
exclude_packages = (("sourced.ml.core.tests", "sourced.ml.core.tests.source")
                    if not include_tests else ())

tf_requires = ["tensorflow>=1.0,<1.14"]
tf_gpu_requires = ["tensorflow-gpu>=1.0,<1.14"]
package_data = {"": ["LICENSE.md", "README.md"]}
if include_tests:
    test_data_dirs = ["./asdf/*.asdf", "./swivel/*", "identifiers.csv.tar.gz"]
    package_data["sourced.ml.core.tests"] = test_data_dirs

setup(
    name="sourced-ml-core",
    description="Library containing the core algorithms for machine learning on source code. "
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
    packages=find_packages(exclude=exclude_packages),
    namespace_packages=["sourced", "sourced.ml"],
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
        "bblfsh>=3.1.0,<4.0",
        "modelforge>=0.14.1",
        "pygments>=2.2.0,<3.0",
        "keras>=2.0,<3.0",
        "scikit-learn>=0.21.1,<1.0",
        "tqdm>=4.20,<5.0",
    ],
    extras_require={"tf": tf_requires, "tf_gpu": tf_gpu_requires},
    tests_require=["docker>=3.6.0,<4.0"],
    package_data=package_data,
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
