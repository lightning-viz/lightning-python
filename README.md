python-lightning
================

Python client for the lightning API



## Usage

### Example 1 - Creating a new session

```python
from lightning import Lightning

lng = Lightning()
lng.create_session()

lng.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

### Example 2 - Using an existing session


```python
from lightning import Lightning

lng = Lightning()

session_id = 14
lng.create_session(session_id)

lng.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```
