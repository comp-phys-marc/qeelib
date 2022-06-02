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

## License

Copyright 2019 Marcus Edwards

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

```
http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.