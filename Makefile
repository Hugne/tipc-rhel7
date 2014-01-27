CONFIGDIR=./mock/
SPECFILE=./src/tipc-kmod.spec
SOURCES=./src/
OUTDIR=./out
SRPM=./out/tipc*.el6.src.rpm

all: srpm kmod

srpm:
	tar -cjf src/tipc.tar.bz2 -C src tipc
	mock --configdir=$(CONFIGDIR) --spec=$(SPECFILE) --sources=$(SOURCES) --resultdir=$(OUTDIR) --buildsrpm

kmod:
	mock --configdir=$(CONFIGDIR) --init
	mock --configdir=$(CONFIGDIR) --chroot "ln -s /lib/modules/kabi-current/ /lib/modules/kabi"
	mock --no-clean --configdir=$(CONFIGDIR)  --resultdir=$(OUTDIR) --rebuild $(SRPM)
	#This is just a workaround for the kabi symlink bug:
	#https://bugzilla.redhat.com/show_bug.cgi?id=842038
	#Once that bug is resolved, they should be replaced with:
	#mock --configdir=$(CONFIGDIR)  --resultdir=$(OUTDIR) --rebuild $(SRPM)

clean:
	rm -rf out/*
