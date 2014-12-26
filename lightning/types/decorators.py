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
    argspec = inspect.getargspec(VizType.clean)
    formatted_args = inspect.formatargspec(*argspec)
    fndef = 'lambda self, %s: plotter(self,%s' % (formatted_args.lstrip('(').rstrip(')'), formatted_args[1:])
    fake_fn = eval(fndef, {'plotter': plotter})
    plotter = wraps(VizType.clean)(fake_fn)

    # manually assign a plot-specific name (instead of 'clean')
    plotter.__name__ = func

    # add plotter to class
    setattr(Lightning, func, plotter)

    return VizType
