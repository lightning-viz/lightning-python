from numpy import asarray, vstack, newaxis, zeros, nonzero, concatenate, transpose, atleast_2d

def check_colors(clrs):
    
    clrs = asarray(clrs)
    if clrs.ndim == 2 and clrs.shape[1] == 1:
        clrs = clrs.flatten()
    if clrs.ndim == 2 and clrs.shape[0] == 1:
        clrs = clrs.flatten()
    if clrs.ndim == 1:
        clrs = clrs[:,newaxis]
    elif clrs.shape[1] != 3:
        raise Exception("Color array must have three values per point")

    return clrs


def array_to_lines(data):

    data = asarray(data)

    return data


def vecs_to_points(x, y):
        
    x = asarray(x)
    y = asarray(y)
    points = vstack([x, y, range(0,len(x))]).T

    return points


def mat_to_links(mat, labels=None):

    # get nonzero entries as list with the source, target, and value as columns
    
    mat = asarray(mat)
    if mat.ndim < 2:
            raise Exception('Matrix input must be two-dimensional')

    inds = nonzero(mat)
    links = concatenate((transpose(nonzero(mat)), atleast_2d(mat[inds]).T), axis=1)

    # pick group assignments (default is all 1s)
    n = mat.shape[0]
    if labels is None:
        nodes = zeros((1, n)).T
    else:
        if labels.size != n:
            raise Exception("Must provide label for each row")
        nodes = labels.astype(int).reshape(labels.size, 1)

    return links, nodes


def array_to_im(im):

    from matplotlib.pyplot import imsave
    from matplotlib.pyplot import cm
    import io

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