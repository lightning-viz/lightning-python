[![Build Status](https://travis-ci.org/lightning-viz/lightning-python.svg?branch=master)](https://travis-ci.org/lightning-viz/lightning-python)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/lightning-viz/lightning?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Lightning python client
================

Python client for the [lightning](https://github.com/mathisonian/lightning) API

## installation
Install using:

```
pip install lightning-python
```
Compatible with Python 2.7 and 3.4. 

## usage

### creating a session

```python
from lightning import Lightning

lgn = Lightning(host="http://my-lightning-instance.herokuapp.com")

lgn.create_session()
lgn.create_session("provide an optional session name")
```

### creating a visualization
Methods are available for the default visualization types included with Lightning
```python
lgn.line([1,2,3,4,5,6,7,8,0,-2,2])
lgn.scatter([1,2,3],[2,9,4])
```

### setting options
Visualizations can be customized through optional parameters
```python
lgn.scatter([1,2,3],[2,9,4], label=[1,2,3], size=[5,10,20])
```
### using custom plots
For custom plots not included with the default set, specify by name and provide data as a dictionary
```python
lgn.plot(data={"series": [1,2,3]}, type='line')
```

## examples

See a collection of [IPython notebooks](http://nbviewer.ipython.org/github/lightning-viz/lightning-example-notebooks/tree/master/).

## complete documentation

Available [here](http://lightning-viz.github.io/lightning-python/).

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

## help

We maintain a [chatroom](https://gitter.im/lightning-viz/lightning) on gitter. If there's no response there: file an issue or reach out on twitter ([@mathisonian](http://twitter.com/matisonian), [@thefreemanlab](http://twitter.com/thefreemanlab))

