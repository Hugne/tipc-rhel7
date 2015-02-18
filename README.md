# tipc-rhel7
TIPC kmod for RHEL7

Prebuilt binaries can be found here:
https://build.opensuse.org/package/binaries/home:hugne/tipc-rhel7?repository=RHEL_7

To build the SRPM/KMOD from sources, you'll need to install the following packages:
```
$ yum groupinstall "Development tools"
$ yum install kernel-devel kernel-abi-whitelists bzip2
```
After that, just do 'make' in the tipc-kmod directory. This will generate the srcrpm and build the TIPC kmod.
The output will be located in ~/rpmbuild/RPMS/x86_64/
```
$ rpm -ivh ~/rpmbuild/RPMS/x86_64/tipc-2.0-1.el7.x86_64.rpm ~/rpmbuild/RPMS/x86_64/kmod-tipc-2.0-1.el7.x86_64.rpm
Preparing...                          ################################# [100%]
Updating / installing...
   1:kmod-tipc-2.0-1.el7              ################################# [ 50%]
   2:tipc-2.0-1.el7                   ################################# [100%]
$ modprobe tipc
[ 1318.892857] tipc: Activated (version 2.0.0)
[ 1318.915972] NET: Registered protocol family 30
[ 1318.916146] tipc: Started in single node mode
```

RHEL does not package the tipcutils package, but you should be able to grab that from Fedora
http://rpm.pbone.net/index.php3/stat/4/idpl/27459724/dir/fedora_19/com/tipcutils-2.0.6-1.fc19.x86_64.rpm.html
