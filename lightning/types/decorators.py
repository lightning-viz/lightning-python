from lightning import Lightning
from lightning.types.base import Base
from functools import wraps
import inspect


def viztype(VizType):

    # wrapper that passes inputs to cleaning function and creates viz
    @wraps(VizType.clean)
    def plotter(self, *args, **kwargs):

        if kwargs['height'] is None and kwargs['width'] is None:
            if self.size != 'full':
                kwargs['width'] = SIZES[self.size]

        if self.local_enabled:
            if hasattr(VizType, '_local') and VizType._local == False:
                name = VizType._func if hasattr(VizType, 'func') else VizType._name
                print("Plots of type '%s' not yet supported in local mode" % name)
            else:
                viz = VizType._baseplot_local(VizType._name, *args, **kwargs)
                return viz

        else:
            if not hasattr(self, 'session'):
                self.create_session()
            if VizType._name == 'plot':
                if 'type' not in kwargs:
                    raise ValueError("Must specify a type for custom plots")
                else:
                    type = kwargs['type']
                    del kwargs['type']
                viz = VizType._baseplot(self.session, type, *args, **kwargs)
            else:
                viz = VizType._baseplot(self.session, VizType._name, *args, **kwargs)
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

    options = {}
    if hasattr(VizType, '_options'):
        options = VizType._options

    def parse(val):
        if isinstance(val, str):
            return "'" + val + "'"
        else:
            return val

    formatted_options = ', '.join(['%s=%s' % (key, parse(value.get('default'))) for (key, value) in options.items()])
    argspec = inspect.getargspec(VizType.clean)
    formatted_args = inspect.formatargspec(*argspec)
    fndef = 'lambda self, %s, %s: plotter(self,%s, %s)' \
            % (formatted_args.lstrip('(').rstrip(')'),
               formatted_options, formatted_args[1:].replace('=None', '').rstrip(')'),
               ', '.join('%s=%s' % (key, key) for key in options.keys()))

    fake_fn = eval(fndef, {'plotter': plotter})
    plotter = wraps(VizType.clean)(fake_fn)

    # manually assign a plot-specific name (instead of 'clean')
    plotter.__name__ = func

    if plotter.__doc__:
        plotter.__doc__ += Base._doc

    # add plotter to class
    setattr(Lightning, func, plotter)

    return VizType

SIZES = {
    'small': 400,
    'medium': 600,
    'large': 800,
}
