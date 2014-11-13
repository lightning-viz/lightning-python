from lightning import Visualization

class Base(Visualization):

    _name = 'base'

    data_dict_inputs = {
        'points': ['x', 'y', 'i'],
        'colors': ['r', 'g', 'b'],
        'labels': ['k'],
        'links': ['source', 'target', 'value'],
        'nodes': ['group']
    }

    @classmethod
    def clean(cls, data):
        return {'data': data}

    @classmethod
    def check_unkeyed_arrays(cls, key, val):

        if not key in cls.data_dict_inputs:
            return val

        if not isinstance(val, list):
            raise Exception("Must provide a list")

        if len(val) == 0:
            return val

        if isinstance(val[0], dict) and isinstance(val[-1], dict):
            return val

        if isinstance(val[0], list) and isinstance(val[-1], list):
            # if both the first and last elements are lists
            out = []
            mapping = cls.data_dict_inputs[key]
            for l in val:
                out.append(dict(zip(mapping, l)))

            return out

    @staticmethod
    def ensure_dict_or_list(x):

        if isinstance(x, dict):
            return x

        if isinstance(x, list):
            return x

        try:
            # Convert Numpy arrays to lists
            return x.tolist()

        except Exception:
            pass

        # add other data type conversions here
        raise Exception("Could not convert to correct data type")

    @classmethod
    def clean_data(cls, *args, **kwargs):
        """
        Convert raw data into a dictionary with plot-type specific methods.

        The result of the cleaning operation should be a dictionary.
        If the dictionary contains a 'data' field it will be passed directly
        (ensuring appropriate formatting). Otherwise, it should be a
        dictionary of data-type specific array data (e.g. 'points', 
        'timeseries'), which will be labeled appropriately
        (see _check_unkeyed_arrays).
        """

        datadict = cls.clean(*args, **kwargs)
        print(datadict)
        if 'data' in datadict:
            data = datadict['data']
            data = cls.ensure_dict_or_list(data)
        else:
            data = {}
            for key in datadict:
                if key == 'images':
                    data[key] = datadict[key]
                else:
                    d = cls.ensure_dict_or_list(datadict[key])
                    data[key] = cls.check_unkeyed_arrays(key, d)

        return data

    @classmethod
    def baseplot(cls, session, type, *args, **kwargs):
        """
        Base method for plotting data.

        Applies a plot-type specific cleaning operation to generate
        a dictionary with the data, then creates a visualization with the data. 
        Expects a session and a type, followed by all plot-type specific
        positional and keyword arguments, which will be handled by the clean
        method of the given plot type.

        If the dictionary contains images, they will be extracted
        and appended separately from the rest of the data.
        """

        if not type:
            raise Exception("Must provide a plot type")

        data = cls.clean_data(*args, **kwargs)
        
        if 'images' in data:
            images = data['images']
            del data['images']
            viz = cls.create(session, data=data, type=type)
            viz.append_image(images)
        else:
            viz = cls.create(session, data=data, type=type)

        return viz

    @classmethod
    def baseimage(cls, session, type, *args, **kwargs):
        """
        Base method for showing images.

        Applies an image-type specific cleaning operation, then creates
        a visualization with the images. Expects a session and a type,
        followed by all image-type specific positional and keyword arguments.
        """

        images = cls.clean_data(*args, **kwargs)['images']
        return cls.create(session, images=images, type=type)

    def update(self, *args, **kwargs):
        """
        Base method for updating data.

        Applies a plot-type specific cleaning operation, then
        updates the data in the visualization.
        """

        data = self.clean_data(*args, **kwargs)
        self.update_data(data=data)


