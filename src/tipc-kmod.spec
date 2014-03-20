%define kmod_name		tipc
%define kmod_version		2.0
%define kmod_release		1%{?dist}

Source0:	tipc.tar.bz2
Source10:	tipc-kmodtool.sh
Source100:	patches.v3.14.tar.bz2
Name:           %{kmod_name}
Version:        %{kmod_version}
Release:        %{kmod_release}
Group:          System Environment/Kernel
License:        Dual BSD/GPL
Summary:        TIPC: Transparent Inter Process Communication
URL:            http://tipc.sourceforge.net
BuildRequires:  %kernel_module_package_buildreqs kernel-abi-whitelists
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch:  i686 x86_64

%files
%defattr(-,root,root,-)

#Because redhat-rpm-config is hopelessly broken in chroot environments
%define kversion %{expand:%(sh %{SOURCE10} verrel)}
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

%define debug_package %{nil}

%description
This package provides a TIPC stack with additional upstream patches.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -n %{kmod_name} -a 100
for patch in patches.v3.14/*.patch; do
	echo applying $patch...
	patch -p3 < $patch
done

set -- *
mkdir tipc
mv "$@" tipc/

%build
ksrc="%{_usrsrc}/kernels/%{kversion}"
KCPPFLAGS="-DCONFIG_TIPC_PORTS=262144" %{__make} -C "$ksrc" %{?_smp_mflags} CONFIG_TIPC=m M=$PWD/tipc

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} $PWD/tipc/*.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*

%clean
%{__rm} -rf %{buildroot}

%changelog
* Thu Feb 06 2014 Erik Hugne <erik.hugne@ericsson.com>
- Initial version for RHEL7, based on 3.10 and uplifted to 3.14
  * tipc: eliminate redundant lookups in registry
  * tipc: align usage of variable names and macros in socket
  * tipc: eliminate redundant locking
  * tipc: eliminate upcall function pointers between port and socket
  * tipc: aggregate port structure into socket structure
  * tipc: remove redundant 'peer_name' field in struct tipc_sock
  * tipc: replace reference table rwlock with spinlock
  * tipc: don't log disabled tasklet handler errors
  * tipc: fix memory leak during module removal
  * tipc: drop subscriber connection id invalidation
  * tipc: fix connection refcount leak
  * tipc: allow connection shutdown callback to be invoked in advance
  * tipc: remove all enabled flags from all tipc components
  * tipc: failed transmissions should return error
  * tipc: align tipc function names with common naming practice in the network
  * tipc: correct usage of spin_lock() vs spin_lock_bh()
  * tipc: fix a loop style problem
  * tipc: add node_lock protection to link lookup function
  * tipc: remove bearer_lock from tipc_bearer struct
  * tipc: delay delete of link when failover is needed
  * tipc: changes to general packet reception algorithm
  * tipc: rename stack variables in function tipc_link_tunnel_rcv
  * tipc: more cleanup of tunnelling reception function
  * tipc: change signature of tunnelling reception function
  * tipc: change reception of tunnelled failover packets
  * tipc: change reception of tunnelled duplicate packets
  * tipc: remove 'links' list from tipc_bearer struct
  * tipc: redefine 'started' flag in struct link to bitmap
  * tipc: move code for deleting links from bearer.c to link.c
  * tipc: move code for resetting links from bearer.c to link.c
  * tipc: stricter behavior of message reassembly function
  * tipc: explicitly include core.h in addr.h
  * tipc: fix message corruption bug for deferred packets
  * net: add build-time checks for msg->msg_name size
  * tipc: standardize recvmsg routine
  * tipc: standardize sendmsg routine of connected socket
  * tipc: standardize sendmsg routine of connectionless socket
  * tipc: standardize accept routine
  * tipc: standardize connect routine
  * tipc: spelling fixes
  * tipc: make link start event synchronous
  * tipc: introduce new spinlock to protect struct link_req
  * tipc: remove 'has_redundant_link' flag from STATE link protocol messages
  * tipc: rename functions related to link failover and improve comments
  * tipc: correctly unlink packets from deferred packet queue
  * tipc: remove unused code
  * tipc: make local function static
  * tipc: make the code look more readable
  * tipc: fix deadlock during socket release
  * tipc: change lock_sock order in connect()
  * tipc: Use <linux/uaccess.h> instead of <asm/uaccess.h>
  * tipc: kill unnecessary goto's
  * tipc: remove unnecessary variables and conditions
  * tipc: remove unused 'blocked' flag from tipc_link struct
  * tipc: improve naming and comment consistency in media layer
  * tipc: initiate media type array at compile time
  * tipc: eliminate redundant code with kfree_skb_list routine
  * tipc: protect handler_enabled variable with qitem_lock spin lock
  * tipc: correct the order of stopping services at rmmod
  * tipc: remove interface state mirroring in bearer
  * net: rework recvmsg handler msg_name and msg_namelen logic
  * tipc: fix dereference before check warning
  * tipc: reassembly failures should cause link reset
  * tipc: message reassembly using fragment chain
  * tipc: don't reroute message fragments
  * tipc: remove two indentation levels in tipc_recv_msg routine
  * net: misc: Remove extern from function prototypes
  * tipc: simplify the link lookup routine
  * tipc: correct return value of link_cmd_set_value routine
  * tipc: correct return value of recv_msg routine
  * tipc: avoid unnecessary lookup for tipc bearer instance
  * tipc: make bearer and media naming consistent
  * tipc: silence sparse warnings
  * tipc: remove iovec length parameter from all sending functions
  * tipc: don't use memcpy to copy from user space
  * tipc: set sk_err correctly when connection fails
  * tipc: avoid possible deadlock while enable and disable bearer
  * tipc: fix oops when creating server socket fails
  * net/tipc: use %*phC to dump small buffers in hex form
  * tipc: remove dev_base_lock use from enable_bearer
  * tipc: fix wrong return value for link_send_sections_long routine
  * tipc: make tipc_link_send_sections_fast exit earlier
  * tipc: enhance priority of link protocol packet
  * tipc: cosmetic realignment of function arguments
  * tipc: save sock structure pointer instead of void pointer to tipc_port
  * tipc: convert config_lock from spinlock to mutex
  * tipc: rename tipc_createport_raw to tipc_createport
  * tipc: remove user_port instance from tipc_port structure
  * tipc: delete code orphaned by new server infrastructure
  * tipc: convert configuration server to use new server facility
  * tipc: convert topology server to use new server facility
  * tipc: introduce new TIPC server infrastructure
  * tipc: allow implicit connect for stream sockets
  * tipc: change socket buffer overflow control to respect sk_rcvbuf



