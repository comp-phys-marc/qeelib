# QEElib module (Python)

A quantum computing simulation abstraction library written in Python.

# Setup

### Install Git:

```
apt-get install git
```

## Repository

### Cloning:

```
git clone https://gitlab.com/QuantumEmulator/qeelib.git
```

# Documentation

## Generating documentation

```
rm docs/*
python3 -m pydoc -w ./*.py
mv ./*.html docs
```

# Tests

## Running tests

```
python3 ./tests/qasm_tests.py
```