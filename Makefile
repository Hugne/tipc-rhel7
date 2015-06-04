RPMBUILD=~/rpmbuild/

all: srpm kmod

srpm:
	mkdir -p $(RPMBUILD)/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	tar -cjf $(RPMBUILD)/SOURCES/tipc.tar.bz2 -C src tipc
	tar -cjf $(RPMBUILD)/SOURCES/patches.v3.14.tar.bz2 -C src patches.v3.14
	cp src/*.patch src/tipc-kmodtool.sh $(RPMBUILD)/SOURCES
	cp src/tipc-kmod.spec $(RPMBUILD)/SPECS
	rpmbuild -bs $(RPMBUILD)/SPECS/tipc-kmod.spec

kmod:
	rpmbuild --rebuild $(RPMBUILD)/SRPMS/tipc*.rpm

clean:
	rm -rf out/*
