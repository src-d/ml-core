# MLonCode research playground [![PyPI](https://img.shields.io/pypi/v/sourced-ml.svg)](https://pypi.python.org/pypi/sourced-ml) [![Build Status](https://travis-ci.org/src-d/ml.svg)](https://travis-ci.org/src-d/ml) [![Docker Build Status](https://img.shields.io/docker/build/srcd/ml.svg)](https://hub.docker.com/r/srcd/ml) [![codecov](https://codecov.io/github/src-d/ml/coverage.svg)](https://codecov.io/gh/src-d/ml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This project is the foundation for [MLonCode](https://github.com/src-d/awesome-machine-learning-on-source-code) research and development. It abstracts feature extraction and training models, thus allowing to focus on the higher level tasks.

Currently, the following models are implemented:

* BOW - weighted bag of x, where x is many different extracted feature types.
* id2vec, source code identifier embeddings.
* docfreq, feature document frequencies \(part of TF-IDF\).
* topic modeling over source code identifiers.

It is written in Python3 and has been tested on Linux and macOS. source{d} core-ml is tightly 
coupled with [source{d} engine](https://engine.sourced.tech) and delegates all the feature extraction parallelization to it.

Here is the list of proof-of-concept projects which are built using ml-core:

* [vecino](https://github.com/src-d/vecino) - finding similar repositories.
* [tmsc](https://github.com/src-d/tmsc) - listing topics of a repository.
* [snippet-ranger](https://github.com/src-d/snippet-ranger) - topic modeling of source code snippets.
* [apollo](https://github.com/src-d/apollo) - source code deduplication at scale.

## Installation

Whether you wish to include Spark in your installation or would rather use an existing
installation, to use `sourced-ml` you will need to have some native libraries installed,
e.g. on Ubuntu you must first run: `apt install libxml2-dev libsnappy-dev`. [Tensorflow](https://tensorflow.org)
is also a requirement - we support both the CPU and GPU  version. 
In order to select which version you want, modify the package name in the next section
to either `sourced-ml[tf]` or `sourced-ml[tf-gpu]` depending on your choice.
**If you don't, neither version will be installed.**

## Docker image

```text
docker run -it --rm srcd/ml --help
```

If this first command fails with

```text
Cannot connect to the Docker daemon. Is the docker daemon running on this host?
```

And you are sure that the daemon is running, then you need to add your user to `docker` group: refer to the [documentation](https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user).

## Contributions

...are welcome! See [CONTRIBUTING](contributing.md) and [CODE\_OF\_CONDUCT.md](code_of_conduct.md).

## License

[Apache 2.0](license.md)

## Algorithms

#### Identifier embeddings

We build the source code identifier co-occurrence matrix for every repository.

1. Read Git repositories.
2. Classify files using [enry](https://github.com/src-d/enry).
3. Extract [UAST](https://doc.bblf.sh/uast/specification.html) from each supported file.
4. [Split and stem](https://github.com/src-d/ml/tree/d1f13d079f57caa6338bb7eb8acb9062e011eda9/sourced/ml/algorithms/token_parser.py) all the identifiers in each tree.
5. [Traverse UAST](https://github.com/src-d/ml/tree/d1f13d079f57caa6338bb7eb8acb9062e011eda9/sourced/ml/transformers/coocc.py), collapse all non-identifier paths and record all
   identifiers on the same level as co-occurring. Besides, connect them with their immediate parents.

6. Write the global co-occurrence matrix.
7. Train the embeddings using [Swivel](https://github.com/src-d/ml/tree/d1f13d079f57caa6338bb7eb8acb9062e011eda9/sourced/ml/algorithms/swivel.py) \(requires Tensorflow\). Interactively view
   the intermediate results in Tensorboard using `--logs`.

8. Write the identifier embeddings model.

1-5 is performed with `repos2coocc` command, 6 with `id2vec_preproc`, 7 with `id2vec_train`, 8 with `id2vec_postproc`.

#### Weighted Bag of X

We represent every repository as a weighted bag-of-vectors, provided by we've got document frequencies \("docfreq"\) and identifier embeddings \("id2vec"\).

1. Clone or read the repository from disk.
2. Classify files using [enry](https://github.com/src-d/enry).
3. Extract [UAST](https://doc.bblf.sh/uast/specification.html) from each supported file.
4. Extract various features from each tree, e.g. identifiers, literals or node2vec-like structural fingerprints.
5. Group by repository, file or function.
6. Set the weight of each such feature according to TF-IDF.
7. Write the BOW model.

1-7 are performed with `repos2bow` command.

#### Topic modeling

See [here](doc/topic_modeling.md).

## Glossary

See [here](GLOSSARY.md).
