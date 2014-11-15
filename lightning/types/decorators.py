from lightning import Lightning


def viztype(VizType):

    def plotter(self, *args, **kwargs):
        if not hasattr(self, 'session'):
            self.create_session()
        viz = VizType.baseplot(self.session, VizType._name, *args, **kwargs)
        self.session.visualizations.append(viz)
        return viz

    if not hasattr(VizType,'_func'):
        func = VizType._name
    else:
        func = VizType._func

    setattr(Lightning, func, plotter)
    return VizType
