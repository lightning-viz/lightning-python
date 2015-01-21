Lightning python client
================

Python client for the [lightning](https://github.com/mathisonian/lightning) API

## installation

```
pip install lightning-python
```

## usage

### creating a new session

```python
from lightning import Lightning

lightning = Lightning(host="http://my-lightning-instance.herokuapp.com")
lightning.create_session("provide an optional session name")

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

### using an existing session


```python
from lightning import Lightning

lightning = Lightning(host="http://my-lightning-instance.herokuapp.com")

session_id = 14
lightning.use_session(session_id)

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

### using with iPython

```python
from lightning import Lightning

lightning = Lightning(host="http://my-lightning-instance.herokuapp.com", ipython=True)

session_id = 14
lightning.use_session(session_id)

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

![ipython-example](http://i.gif.fm/6ZTdQ.png)

## running tests

Requires [pytest](http://pytest.org/latest/)

Clone the repo and install the library locally:

```sh
$ pip install -e .
``` 

The tests need to be run against a lightning server. By default they expect
this to be found at `http://localhost:3000`.

To run the tests:

```
$ py.test
```

or with against a custom host url


```
$ py.test --host=http://mylightninghost.herokuapp.com
```
## examples

http://nbviewer.ipython.org/github/lightning-viz/lightning-example-notebooks/tree/master/

## complete documentation

http://lightning-viz.github.io/lightning-python/

## help

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/lightning-viz/lightning?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

We maintain a chatroom on gitter. If there's no response there: file an issue or reach out on twitter (@mathisonian, @thefreemanlab)

