from session import Session
from visualization import Visualization


class Lightning(object):

    def __init__(self, host="http://localhost:3000", ipython=False, auth=None):
        self.host = host
        self.auth = auth

        if auth is not None:
            if isinstance(auth, tuple):
                self.set_basic_auth(auth[0], auth[1])

        if ipython:
            self.enable_ipython()

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
        formatter.for_type(Visualization,
                           lambda viz, kwds=kwargs: viz.get_html())

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
        self.host = host
        return self

    def plot(self, type=None, **kwargs):
        """
        Generic plotting function.

        Provide an arbtirary data object as a dictionary,
        and a plot type as a string. Can be used to provide data to custom
        plot types, as opposed to the included plot types
        (e.g. lightning.scatter, lightning.line, etc.)
        """

        from types.plots import Generic
        
        viz = Generic.baseplot(self.session, type=type, **kwargs)
        self.session.visualizations.append(viz)
        return viz





        

