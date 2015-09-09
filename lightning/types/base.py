from lightning import Visualization, VisualizationLocal
import requests
import six


class Base(Visualization, VisualizationLocal):

    _name = 'base'

    _options = {
        'width': {'default': None},
        'height': {'default': None},
        'description': {'default': None}
    }

    _doc = """
        width : int, optional, default=None
            Width of visualization in pixels.

        height : int, optional, default=None
            Height of visualization in pixels.

        description : str, optional, default=None
            Markdown formatted text to show with visualization
            when displayed in a Lightning server.
    """

    _data_dict_inputs = {}

    @classmethod
    def _check_unkeyed_arrays(cls, key, val):

        if key not in cls._data_dict_inputs:
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
            mapping = cls._data_dict_inputs[key]
            for l in val:
                out.append(dict(zip(mapping, l)))

            return out

    @staticmethod
    def _ensure_dict_or_list(x):

        if isinstance(x, dict):
            return x

        if isinstance(x, list):
            return x

        if isinstance(x, str):
            return x

        if isinstance(x, (int, float, complex)):
            return x

        try:
            # convert numpy arrays to lists
            return x.tolist()

        except Exception:
            pass

        # add other data type conversions here
        raise Exception("Could not convert to correct data type")

    @classmethod
    def _clean_data(cls, *args, **kwargs):
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

        if 'data' in datadict:
            data = datadict['data']
            data = cls._ensure_dict_or_list(data)
        else:
            data = {}
            for key in datadict:
                if key == 'images':
                    data[key] = datadict[key]
                else:
                    d = cls._ensure_dict_or_list(datadict[key])
                    data[key] = cls._check_unkeyed_arrays(key, d)

        return data

    @classmethod
    def _clean_options(cls, **kwargs):

        options = {}
        description = None
        if hasattr(cls, '_options'):
            for key, value in six.iteritems(kwargs):
                if key in cls._options:
                    lgn_option = cls._options[key].get('name', key)
                    options[lgn_option] = value
                if key == 'description':
                    description = value

        return options, description

    @classmethod
    def _baseplot_local(cls, type, *args, **kwargs):

        data = cls._clean_data(*args)
        options, description = cls._clean_options(**kwargs)

        payload = {'type': type, 'options': options}

        if 'images' in data:
            payload['images'] = data['images']
        else:
            payload['data'] = data

        viz = VisualizationLocal._create(**payload)

        return viz

    @classmethod
    def _baseplot(cls, session, type, *args, **kwargs):
        """
        Base method for plotting data and images.

        Applies a plot-type specific cleaning operation to generate
        a dictionary with the data, then creates a visualization with the data. 
        Expects a session and a type, followed by all plot-type specific
        positional and keyword arguments, which will be handled by the clean
        method of the given plot type.

        If the dictionary contains only images, or only non-image data, 
        they will be passed on their own. If the dictionary contains
        both images and non-image data, the images will be appended
        to the visualization.
        """

        if not type:
            raise Exception("Must provide a plot type")

        options, description = cls._clean_options(**kwargs)
        data = cls._clean_data(*args)

        if 'images' in data and len(data) > 1:
            images = data['images']
            del data['images']
            viz = cls._create(session, data=data, type=type, options=options, description=description)
            first_image, remaining_images = images[0], images[1:]
            viz._append_image(first_image)
            for image in remaining_images:
                viz._append_image(image)

        elif 'images' in data:
            images = data['images']
            viz = cls._create(session, images=images, type=type, options=options, description=description)

        else:
            viz = cls._create(session, data=data, type=type, options=options, description=description)

        return viz

    def update(self, *args, **kwargs):
        """
        Base method for updating data.

        Applies a plot-type specific cleaning operation, then
        updates the data in the visualization.
        """

        data = self._clean_data(*args, **kwargs)
        if 'images' in data:
            images = data['images']
            for img in images:
                self._update_image(img)
        else:
            self._update_data(data=data)

    def append(self, *args, **kwargs):
        """
        Base method for appending data.

        Applies a plot-type specific cleaning operation, then
        appends data to the visualization.
        """

        data = self._clean_data(*args, **kwargs)
        if 'images' in data:
            images = data['images']
            for img in images:
                self._append_image(img)
        else:
            self._append_data(data=data)

    def _get_user_data(self):
        """
        Base method for retrieving user data from a viz.
        """

        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/settings/'
        r = requests.get(url)
        if r.status_code == 200:
            content = r.json()
        else:
            raise Exception('Error retrieving user data from server')

        return content



