# ds Stoa

![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11-blue)
[![PyPI version](https://badge.fury.io/py/ds-stoa.svg?kill_cache=1)](https://badge.fury.io/py/ds-stoa)
[![Build Status](https://github.com/grasp-labs/ds-stoa/actions/workflows/deploy.yml/badge.svg)](https://github.com/grasp-labs/ds-stoa/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/grasp-labs/ds-stoa/graph/badge.svg?token=EO3YCNCZFS)](https://codecov.io/gh/grasp-labs/ds-stoa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Development

### Build package

You can build the package files in a Docker container by executing the ``build.sh`` script. If you prefer to build locally run the command

```shell
pipenv run python -m build
```

**Note that this requires that you install the build package locally (by running ``pipenv install build``).**

### Deploy package to TestPyPI

If you want to see what your final package is going to look like you can deploy it to TestPyPI. This requires an account and an api token. Once you have both you can run the command

```shell
# Make sure there are no changes to commit to git then
git tag <insert version> # for simple testing use something like 0.0.1

# Now build the package
./build.sh

# Finally you can deploy to TestPyPI
pipenv run python -m twine upload --repository testpypi dist/*
```

**Some things to consider**
- This requires twine ``pipenv install twine``
- PyPI will reject development builds, after a successfull build the ``dist`` directory should contain something like ``<package-name>-<0.0.1>-py3-none-any.whl`` and ``<package-name>-<0.0.1>.tag.gz``. If you get commit refs in your version chances are you have some unstaged changes or did not tag the latest commit with a version.
- Use this deployment for testing only, the GitHub Action Workflow will take care of deploying the package to regular PyPI when you merge to main.

### Building the documentation
This template features automated documentation. To build the documentation run
```shell
cd docs
pipenv run make html
```
Once this is done simply open the ``docs/build/html/index.html`` file in a browser to view the docs.

Enhance your docs by adding to the ``docs/source/index.rst`` file.
