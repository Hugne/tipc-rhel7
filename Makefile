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
	mock --configdir=$(CONFIGDIR)  --resultdir=$(OUTDIR) --rebuild $(SRPM)

