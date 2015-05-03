from lightning import Visualization
import requests
import six


class Base(Visualization):

    _name = 'base'

    data_dict_inputs = {}

    @classmethod
    def check_unkeyed_arrays(cls, key, val):

        if key not in cls.data_dict_inputs:
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

        if isinstance(x, str):
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

        options = {}
        if hasattr(cls, '_validOptions'):
            for key, value in six.iteritems(kwargs):
                if key in cls._validOptions:
                    lgn_option = cls._validOptions[key].get('lightning_name')
                    options[lgn_option] = value

        data = cls.clean_data(*args)

        if 'images' in data and len(data) > 1:
            images = data['images']
            del data['images']
            viz = cls.create(session, data=data, type=type)
            first_image, remaining_images = images[0], images[1:]
            viz._append_image(first_image)
            for image in remaining_images:
                viz._append_image(image)

        elif 'images' in data:
            images = data['images']
            viz = cls.create(session, images=images, type=type, options=options)

        else:
            viz = cls.create(session, data=data, type=type, options=options)

        return viz

    def update(self, *args, **kwargs):
        """
        Base method for updating data.

        Applies a plot-type specific cleaning operation, then
        updates the data in the visualization.
        """

        data = self.clean_data(*args, **kwargs)
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

        data = self.clean_data(*args, **kwargs)
        if 'images' in data:
            images = data['images']
            for img in images:
                self._append_image(img)
        else:
            self._append_data(data=data)

    def get_user_data(self):
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



