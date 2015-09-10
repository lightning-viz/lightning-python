import requests
from .session import Session
from .visualization import Visualization, VisualizationLocal


class Lightning(object):

    def __init__(self, host="http://localhost:3000", local=False, ipython=False, auth=None, size='medium'):

        if ipython:
            self.startup_message_ipython()
        else:
            self.startup_message()

        if local:
            self.enable_local()
        else:
            self.local_enabled = False
            self.set_host(host)
            self.auth = auth

            if auth is not None:
                if isinstance(auth, tuple):
                    self.set_basic_auth(auth[0], auth[1])

            status = self.check_status()
            if not status:
                raise ValueError("Could not access server")

        if ipython:
            self.enable_ipython()
            self.set_size(size)
        else:
            self.ipython_enabled = False
            self.set_size('full')

    def __repr__(self):
        s = 'Lightning\n'
        if hasattr(self, 'host') and self.host is not None and not self.local_enabled:
            s += 'host: %s\n' % self.host
        if self.local_enabled:
            s += 'host: local\n'
        if hasattr(self, 'session') and self.session is not None:
            s += 'session: %s\n' % self.session.id
        return s

    def get_ipython_markup_link(self):
        return '%s/js/ipython-comm.js' % self.host

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
        from IPython.display import display, Javascript, HTML

        self.ipython_enabled = True
        self.set_size('medium')

        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']

        if self.local_enabled:
            from lightning.visualization import VisualizationLocal
            js = VisualizationLocal.load_embed()
            display(HTML("<script>" + js + "</script>"))
            print('Running local mode, some functionality limited.\n')
            formatter.for_type(VisualizationLocal, lambda viz, kwds=kwargs: viz.get_html())
        else:
            formatter.for_type(Visualization, lambda viz, kwds=kwargs: viz.get_html())
            r = requests.get(self.get_ipython_markup_link(), auth=self.auth)
            display(Javascript(r.text))

    def disable_ipython(self):
        """
        Disable plotting in the iPython notebook.

        After disabling, lightning plots will be produced in your lightning server,
        but will not appear in the notebook.
        """
        from IPython.core.getipython import get_ipython

        self.ipython_enabled = False
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.type_printers.pop(Visualization, None)
        formatter.type_printers.pop(VisualizationLocal, None)

    def create_session(self, name=None):
        """
        Create a lightning session.

        Can create a session with the provided name, otherwise session name
        will be "Session No." with the number automatically generated.
        """
        self.session = Session.create(self, name=name)
        return self.session

    def use_session(self, session_id):
        """
        Use the specified lightning session.

        Specify a lightning session by id number. Check the number of an existing
        session in the attribute lightning.session.id.
        """
        self.session = Session(lgn=self, id=session_id)
        return self.session

    def enable_local(self):
        """
        Enable a local mode.

        Data is handled locally and embedded via templates.
        Does not require a running Lightning server.
        Useful for notebooks, and can be used offline.
        """
        self.local_enabled = True

    def disable_local(self):
        """
        Disable local mode.
        """
        self.local_enabled = False

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

    def set_size(self, size='medium'):
        """
        Set a figure size using one of four options.

        Convention is 'small': 400px, 'medium': 600px, 'large': 800px,
        and 'full' will use the entire width
        """
        if size not in ['small', 'medium', 'large', 'full']:
            raise ValueError("Size must be one of 'small', 'medium', 'large', 'full'")
        self.size = size

    def check_status(self):
        """
        Check the server for status
        """
        try:
            r = requests.get(self.host + '/status', auth=self.auth,
                             timeout=(10.0, 10.0))
            if not r.status_code == requests.codes.ok:
                print("Problem connecting to server at %s" % self.host)
                print("status code: %s" % r.status_code)
                return False
            else:
                print("Connected to server at %s" % self.host)
                return True
        except (requests.exceptions.ConnectionError,
                requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema) as e:
            print("Problem connecting to server at %s" % self.host)
            print("error: %s" % e)
            return False

    def startup_message_ipython(self):
        import os
        import base64
        try:
            from IPython.display import display, HTML
            icon = os.path.join(os.path.dirname(__file__), 'lib/icon.png')
            with open(icon, "rb") as imfile:
                im = b"".join([b'data:image/png;base64,', base64.b64encode(imfile.read())]).decode("utf-8")
            t = "<div style='margin-top:8px'><img src='%s' width='30px' height='35px' " \
                "style='display: inline-block; padding-right: 10px'>" \
                "</img><span>Lightning initialized</span></div>" % im
            display(HTML(t))
        except:
            print("Lightning initialized")

    def startup_message(self):
        print("Lightning initialized")