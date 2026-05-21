outdir ?= $(CURDIR)
     srpm:
     	dnf -y install rpm-build spectool
     	spectool -g -S -C $(outdir) powercap.spec
     	rpmbuild -bs \
     	  --define "_sourcedir $(outdir)" \
     	  --define "_specdir   $(CURDIR)" \
     	  --define "_srcrpmdir $(outdir)" \
     	  --define "dist %{nil}" powercap.spec
