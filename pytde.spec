%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 4

%define tde_pkg pytde
%define tde_prefix /opt/trinity

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.16.3
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Trinity bindings for Python
Group:		Development/Libraries/Python
URL:		http://www.trinitydesktop.org/
#URL:		http://www.simonzone.com/software/pykdeextensions

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	autoconf automake libtool m4
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:  make

# PYTHON support
%if "%{?python}" == "%{nil}"
%global python python3
%global __python %__python3
%global python_sitearch %{python3_sitearch}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
BuildRequires:	%{python}
BuildRequires:	%{python}-devel
%endif

BuildRequires:	pytqt-devel
Requires:		pytqt

# SIP
BuildRequires:	sip4-tqt-devel >= 4.10.5
Requires:		sip4-tqt >= 4.10.5

Obsoletes:	python-trinity < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python-trinity = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	trinity-python-trinity < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-python-trinity = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Python binding module that provides wide access to the Trinity API,
also known as PyTDE. Using this, you'll get (for example) classes
from tdeio, tdejs, tdehtml and tdeprint.

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{python_sitearch}/*.so
%{python_sitearch}/dcopexport.py*
%{python_sitearch}/dcopext.py*
%{python_sitearch}/pytdeconfig.py*

##########

%package devel
Summary:	Trinity bindings for Python - Development files and scripts
Group:		Development/Libraries/Python
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	python-trinity-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python-trinity-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	trinity-python-trinity-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-python-trinity-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Development .sip files with definitions of PyTDE classes. They
are needed to build PyTDE, but also as building blocks of other
packages based on them. 
The package also contains kdepyuic, a wrapper script around PyQt's 
user interface compiler.

%files devel
%defattr(-,root,root,-)
%{tde_prefix}/bin/tdepyuic
# The SIP files are outside TDE's prefix
%{_datadir}/sip/trinity/

##########

%package doc
Summary:	Documentation and examples for PyTDE
Group:		Development/Libraries/Python

Obsoletes:	python-trinity-doc < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python-trinity-doc = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	trinity-python-trinity-doc < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-python-trinity-doc = %{?epoch:%{epoch}:}%{version}-%{release}

%description doc
General documentation and examples for PyTDE providing programming
tips and working code you can use to learn from.

%files doc
%defattr(-,root,root,-)
%{tde_prefix}/share/doc/tde/HTML/en/pytde/

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%__sed -i "contrib/tdepyuic" -e "s|/usr/bin/env python|/usr/bin/env python3|"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export LD_RUN_PATH="%{tde_prefix}/%{_lib}"

export DH_OPTIONS

%__python configure.py \
	-k %{tde_prefix} \
	-L %{_lib} \
	-v %{_datadir}/sip/trinity

%__make %{_smp_mflags} || %__make


%install
export PATH="%{tde_prefix}/bin:${PATH}"
%__make install DESTDIR=%{buildroot}

# Install documentation
%__mkdir_p %{buildroot}%{tde_prefix}/share/doc/tde/HTML/en/
%__cp -rf doc %{buildroot}%{tde_prefix}/share/doc/tde/HTML/en/pytde/

