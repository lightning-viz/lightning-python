from lightning import Lightning
from functools import wraps
import inspect


def viztype(VizType):

    # wrapper that passes inputs to cleaning function and creates viz
    @wraps(VizType.clean)
    def plotter(self, *args, **kwargs):
        if not hasattr(self, 'session'):
            self.create_session()
        viz = VizType.baseplot(self.session, VizType._name, *args, **kwargs)
        self.session.visualizations.append(viz)
        return viz

    # get desired function name if different than plot type
    if hasattr(VizType, '_func'):
        func = VizType._func
    else:
        func = VizType._name

    # crazy hack to give the dynamically generated function the correct signature
    # based on: http://emptysqua.re/blog/copying-a-python-functions-signature/
    # NOTE currently only handles functions with keyword arguments with defaults of None

    valid_opts = {}
    if hasattr(VizType, '_validOptions'):
        valid_opts = VizType._validOptions

    formatted_opts = ', '.join(['%s=%s' % (key, value.get('default_value')) for (key, value) in valid_opts.items()])
    argspec = inspect.getargspec(VizType.clean)
    formatted_args = inspect.formatargspec(*argspec)
    fndef = 'lambda self, %s, %s: plotter(self,%s, %s)' % (formatted_args.lstrip('(').rstrip(')'), formatted_opts, formatted_args[1:].replace('=None', '').rstrip(')'), ', '.join('%s=%s' % (key, key) for key in valid_opts.keys()))

    fake_fn = eval(fndef, {'plotter': plotter})
    plotter = wraps(VizType.clean)(fake_fn)

    # manually assign a plot-specific name (instead of 'clean')
    plotter.__name__ = func

    # add plotter to class
    setattr(Lightning, func, plotter)

    return VizType
