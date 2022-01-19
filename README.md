[![plants](https://img.shields.io/badge/Plants-Healthy-green.svg)](https://shields.io/)
[![code](https://img.shields.io/badge/Code-Neat-blue.svg)](https://shields.io/)
[![docs](https://img.shields.io/badge/docs-soon-orange.svg)](https://shields.io/)

# Plant
Project for the monitoring and optimization of plant care.

### Installation

As this is a Python package, one can install it using the pip package manager. From
the github repository, follow the instructions below:

```bash
pip install -e .
```

The e-flag in this command allows you to make changes to the package without
reinstalling the package.
Note that the SMBus package appears to only work well on linux distros. We can move to
SMBus2 which runs on other systems but requires a small API change.

### Quick-start
At this point you can head to the examples directory and run them to see how it works.

### Documentation

You can build the documentation as follows:

```python
cd docs
make html
cd build/html
firefox index.html
```

