from numpy import asarray, vstack, newaxis, zeros, nonzero, concatenate, transpose, atleast_2d, size


def add_property(d, prop, name):

    if prop is not None:
        p = check_property(prop, name)
        d[name] = p

    return d


def check_property(prop, name):
    """
    Check and parse a property with either a specific checking function
    or a generic parser
    """

    checkers = {
        'color': check_color,
        'alpha': check_alpha
    }

    if name in checkers:
        return checkers[name](prop)
    else:
        return check_1d(prop, name)


def check_color(c):
    """
    Check and parse color specs as either a single [r,g,b] or a list of
    [[r,g,b],[r,g,b]...]
    """

    c = asarray(c)
    if c.ndim == 1:
        c = c.flatten()
        c = c[newaxis, :]
        if c.shape[1] != 3:
            raise Exception("Color must have three values per point")
    elif c.ndim == 2:
        if c.shape[1] != 3:
            raise Exception("Color array must have three values per point")
    return c


def check_alpha(a):
    """
    Check and parse alpha specs as either a single [x] or a list of [x,x,x...]
    """

    a = check_1d(a, "alpha")
    if any(map(lambda d: d <= 0, a)):
        raise Exception('Alpha cannot be 0 or negative')

    return a


def check_1d(x, name):
    """
    Check and parse a one-dimensional spec as either a single [x] or a list of [x,x,x...]
    """

    x = asarray(x)
    if size(x) == 1:
        x = asarray([x])
    if x.ndim == 2:
        raise Exception("Property: %s must be one-dimensional" % name)
    x = x.flatten()

    return x


def array_to_lines(data):

    data = asarray(data)

    return data


def vecs_to_points(x, y):
        
    x = asarray(x)
    y = asarray(y)

    if x.ndim > 1 or y.ndim > 1:
        raise Exception('x and y vectors must be one-dimensional')

    if size(x) != size(y):
        raise Exception('x and y vectors must be the same length')

    points = vstack([x, y]).T

    return points


def mat_to_links(mat):

    # get nonzero entries as list with the source, target, and value as columns
    
    mat = asarray(mat)
    if mat.ndim < 2:
            raise Exception('Matrix input must be two-dimensional')

    inds = nonzero(mat)
    links = concatenate((transpose(nonzero(mat)), atleast_2d(mat[inds]).T), axis=1)

    return links


def array_to_im(im):

    from matplotlib.pyplot import imsave
    from matplotlib.pyplot import cm
    import io

    im = asarray(im)
    imfile = io.BytesIO()
    if im.ndim == 3:
        # if 3D, show as RGB
        imsave(imfile, im, format="png")
    else:
        # if 2D, show as grayscale
        imsave(imfile, im, format="png", cmap=cm.gray)

    if im.ndim > 3:
        raise Exception("Images must be 2 or 3 dimensions")

    return imfile.getvalue()