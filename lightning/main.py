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

    def enable_ipython(self, **kwargs):
        """
        ipython code inspired by code powering similar functionality in mpld3:
        https://github.com/jakevdp/mpld3/blob/master/mpld3/_display.py#L357
        """

        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.for_type(Visualization,
                           lambda viz, kwds=kwargs: viz.get_html())

    def disable_ipython(self):
        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.type_printers.pop(Visualization, None)

    def create_session(self, name=None):
        self.session = Session.create(self.host, name=name, auth=self.auth)
        return self.session

    def use_session(self, session_id):
        self.session = Session(host=self.host, id=session_id, auth=self.auth)
        return self.session

    def set_basic_auth(self, username, password):
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(username, password)


    def plot(self, type=None, **kwargs):

        from types.plots import Generic
        
        viz = Generic.baseplot(self.session, type=type, **kwargs)
        self.session.visualizations.append(viz)
        return viz




        

