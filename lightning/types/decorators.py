from lightning import Lightning


def viztype(VizType):

    def plotter(self, *args, **kwargs):
        viz = VizType.baseplot(self.session, VizType._name, *args, **kwargs)
        self.session.visualizations.append(viz)
        return viz

    if not hasattr(VizType,'_func'):
        func = VizType._name
    else:
        func = VizType._func

    setattr(Lightning, func, plotter)
    return VizType


def imgtype(ImgType):

    def plotter(self, *args, **kwargs):
        img = ImgType.baseimage(self.session, ImgType._name, *args, **kwargs)
        self.session.visualizations.append(img)
        return img

    if not hasattr(ImgType, '_func'):
        func = ImgType._name
    else:
        func = ImgType._func

    setattr(Lightning, func, plotter)
    return ImgType