import requests
import os
from .session import Session
from .visualization import Visualization


class Lightning(object):

    def __init__(self, host="http://localhost:3000", ipython=False, dbcloud=False, auth=None):
        self.set_host(host)
        self.auth = auth

        if auth is not None:
            if isinstance(auth, tuple):
                self.set_basic_auth(auth[0], auth[1])

        if ipython:
            self.enable_ipython()

        if dbcloud:
            self.enable_dbcloud()

    def __repr__(self):
        if hasattr(self, 'session') and self.session is not None:
            return 'Lightning server at host: %s' % self.host + '\n' + self.session.__repr__()
        else:
            return 'Lightning server at host: %s' % self.host

    def enable_ipython(self, **kwargs):
        """
        Enable plotting in the iPython notebook.

        Once enabled, all lightning plots will be automatically produced
        within the iPython notebook. They will also be available on
        your lightning server within the current session.
        """

        # inspired by code powering similar functionality in mpld3
        # https://github.com/jakevdp/mpld3/blob/master/mpld3/_display.py#L357

        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.for_type(Visualization, lambda viz, kwds=kwargs: viz.get_html())

    def disable_ipython(self):
        """
        Disable plotting in the iPython notebook.

        After disabling, lightning plots will be produced in your lightning server,
        but will not appear in the notebook.
        """
        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.type_printers.pop(Visualization, None)

    def enable_dbcloud(self):
        """
        Enable lightning in the Databricks cloud notebook.

        This will automatically start a lightning server if
        it is not already running, using the host and install
        location expected on a Databricks cloud notebook.
        """
        self.host = "http://localhost:3000"
        url = self.host + "/status/"
        installation = '/root/lightning/'
        try:
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception("Server is running but not returning 200 status")
        except requests.ConnectionError:
            s = os.system('node ' + installation + '/server.js &> /dev/null > /dev/null &')
            if s != 0:
                raise Exception("Failed to start lightning server, check path %s", installation)

    def create_session(self, name=None):
        """
        Create a lightning session.

        Can create a session with the provided name, otherwise session name
        will be "Session No." with the number automatically generated.
        """
        self.session = Session.create(self.host, name=name, auth=self.auth)
        return self.session

    def use_session(self, session_id):
        """
        Use the specified lightning session.

        Specify a lightning session by id number. Check the number of an existing
        session in the attribute lightning.session.id.
        """
        self.session = Session(host=self.host, id=session_id, auth=self.auth)
        return self.session

    def set_basic_auth(self, username, password):
        """
        Set authenatication.
        """
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(username, password)
        return self

    def set_host(self, host):
        """
        Set the host for a lightning server.

        Host can be local (e.g. http://localhost:3000), a heroku
        instance (e.g. http://lightning-test.herokuapp.com), or
        a independently hosted lightning server.
        """
        if host[-1] == '/':
            host = host[:-1]

        self.host = host
        return self

    def plot(self, data=None, type=None):
        """
        Generic plotting function.

        Provide an arbtirary data object as a dictionary, and a plot type as a string.
        The data dictionary will be passed directly to the plot, without any parsing or formatting,
        so make sure it is of the appropriate for your visualization
        (e.g. {"series": [1,2,3]} for a "line" visualization).

        Most useful when providing data to custom visualizations, as opposed to the included plot types
        (e.g. lightning.scatter, lightning.line, etc.) which do automatic parsing and formatting.

        Parameters
        ----------
        data : dict
            Dictionary with data to plot

        type : str
            Name of plot (e.g. 'line' or 'scatter')
        """

        from .types.plots import Generic

        if not hasattr(self, 'session'):
            self.create_session()
        
        viz = Generic.baseplot(self.session, type, data)
        self.session.visualizations.append(viz)
        return viz





        

