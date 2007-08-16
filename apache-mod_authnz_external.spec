#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_authnz_external
%define mod_conf 10_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An apache authentication DSO using external programs
Name:		apache-%{mod_name}
Version:	3.1.0
Release:	%mkrel 6
Group:		System/Servers
License:	Apache License
URL:		http://www.unixpapa.com/mod_auth_external.html
Source0:	http://www.unixpapa.com/software/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires:	pwauth
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Provides:	apache-mod_auth_external
Obsoletes:	apache-mod_auth_external
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
An apache external authentication module - uses PAM.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}
chmod 644 AUTHENTICATORS CHANGES INSTALL* README TODO

%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHENTICATORS CHANGES INSTALL* README TODO UPGRADE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
