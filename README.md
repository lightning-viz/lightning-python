python-lightning
================

Python client for the lightning API

## Installation

```
pip install lightning-python
```

## Usage

### Example 1 - Creating a new session

```python
from lightning import Lightning

lightning = Lightning()
lightning.create_session("provide an optional session name")

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

### Example 2 - Using an existing session


```python
from lightning import Lightning

lightning = Lightning()

session_id = 14
lightning.use_session(session_id)

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```
