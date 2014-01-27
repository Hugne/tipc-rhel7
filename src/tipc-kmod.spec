%define kmod_name		tipc

#%{!?dist: %define dist .el6}
#%{!?kernel_version: %global kernel_version %(uname -r)}

Source0:	tipc.tar.bz2
Source1:	tipc.conf
Name:           %{kmod_name}
Version:        2.0
Release:        1.0%{?dist}
Group:          System Environment/Kernel
License:        Dual BSD/GPL
Summary:        TIPC: Transparent Inter Process Communication
URL:            http://tipc.sourceforge.net
BuildRequires:  %kernel_module_package_buildreqs kabi-whitelists
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch:  i686 x86_64

%files
%defattr(-,root,root,-)
/etc/depmod.d/tipc.conf

%kernel_module_package

#redhat-rpm-config bug: find-requires.ksyms searches for whitelist
#in the wrong path, workaround:
# sudo ln -s /lib/modules/kabi-current/ /lib/modules/kabi

%define debug_package %{nil}

%description
This package provides a TIPC stack with additional upstream patches.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -n %{kmod_name}
set -- *
mkdir source
mv "$@" source/
mkdir obj

%{echo:prep stage 2}
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > %{kmod_name}.conf

%build
for flavor in %flavors_to_build ; do
    rm -rf obj/{$flavor}
    cp -r source obj/${flavor}
    make %{?_smp_mflags} -C %{kernel_source $flavor} M=$PWD/obj/$flavor \
            CONFIG_TIPC=m TIPC_PORTS=131072
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
for flavor in %flavors_to_build ; do
    make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor
done
install -m 644 -D %{SOURCE1} $RPM_BUILD_ROOT/etc/depmod.d/%{kmod_name}.conf

%clean

%{__rm} -rf $RPM_BUILD_ROOT

%changelog
* Fri Nov 22 2013 Erik Hugne <erik.hugne@ericsson.com>
- Initial version


