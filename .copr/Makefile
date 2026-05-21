outdir ?= $(CURDIR)
spec   ?= $(CURDIR)/powercap.spec

srpm:
	dnf -y install rpm-build spectool git-core
	set -e ; \
	sha=$$(git ls-remote https://github.com/powercap/powercap.git master | awk '{print $$1}') ; \
	cdate=$$(date -u +%Y%m%d) ; \
	sed -i "s/^%global commit .*/%global commit $$sha/" $(spec) ; \
	sed -i "s/^%global cdate  .*/%global cdate  $$cdate/" $(spec) ; \
	spectool -g -S -C $(outdir) $(spec) ; \
	rpmbuild -bs \
	  --define "_sourcedir $(outdir)" \
	  --define "_specdir   $(CURDIR)" \
	  --define "_srcrpmdir $(outdir)" \
	  --define "dist %{nil}" \
	  $(spec)
