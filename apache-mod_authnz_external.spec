#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_authnz_external
%define load_order 150

Summary:	An apache authentication DSO using external programs
Name:		apache-%{mod_name}
Version:	3.3.1
Release:	1
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/mod-auth-external/
Source0:	http://mod-auth-external.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Requires:	pwauth
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}

%description
An apache external authentication module - uses PAM.

%prep

%setup -q -n %{mod_name}-%{version}

chmod 644 AUTHENTICATORS CHANGES INSTALL* README TODO UPGRADE

%build

apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache/

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule authnz_external_module %{_libdir}/%{mod_name}.so

AddExternalAuth pwauth %{_bindir}/pwauth
SetExternalAuthMethod pwauth pipe
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc AUTHENTICATORS CHANGES INSTALL* README TODO UPGRADE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
