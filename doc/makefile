BUILDDIR      = build

html:
	rm -rf $(BUILDDIR)
	rm -rf source/generated
	sphinx-build -a source $(BUILDDIR)/html
	cp -R source/_static/images/ $(BUILDDIR)/html/generated/generated/

include sphinx_deployment.mk
