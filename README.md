python-lightning
================

Python client for the [lightning](https://github.com/mathisonian/lightning) API

## Installation

```
pip install lightning-python
```

## Usage

### Creating a new session

```python
from lightning import Lightning

lightning = Lightning(host="http://my-lightning-instance.herokuapp.com")
lightning.create_session("provide an optional session name")

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

### Using an existing session


```python
from lightning import Lightning

lightning = Lightning(host="http://my-lightning-instance.herokuapp.com")

session_id = 14
lightning.use_session(session_id)

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

### Using with iPython

```python
from lightning import Lightning

lightning = Lightning(host="http://my-lightning-instance.herokuapp.com", ipython=True)

session_id = 14
lightning.use_session(session_id)

lightning.plot(data=[1,2,3,4,5,6,7,8,0,-2,2], type='line')

```

![ipython-example](http://i.gif.fm/6ZTdQ.png)




## Examples

### ROI

Creates a new visualization with scatter plot and then appends time series data for each scatter point

```python

from lightning import Lightning

lgn = Lightning(host="http://my-lightning-instance.herokuapp.com")

lgn.create_session()

data = {
    points: # point data,
    timeseries: # timeseries data
}

lgn.plot(data=data, type='roi')

```

### Image

Generate a few random images and show as a gallery

```python

from lightning import Lightning
from numpy import random

lgn = Lightning(host="http://my-lightning-instance.herokuapp.com")

lgn.create_session()

img1 = random.rand(256,256)
img2 = random.rand(256,256,3)

lgn.image([img1,img2], type='gallery')

```

## running tests


(you will need to have [pytest](http://pytest.org/latest/) installed)


Clone this repo and install the library locally:

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



