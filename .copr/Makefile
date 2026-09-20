outdir ?= $(CURDIR)
spec   ?= $(CURDIR)/powercap.spec

.PHONY: srpm
srpm:
	dnf -y install rpm-build git-core python3
	python3 .copr/prepare.py --outdir "$(outdir)" --spec "$(spec)"
