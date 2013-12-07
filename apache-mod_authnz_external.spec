#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_authnz_external
%define mod_conf 10_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An apache authentication DSO using external programs
Name:		apache-%{mod_name}
Version:	3.3.0
Release:	4
Group:		System/Servers
License:	Apache License
URL:		http://www.unixpapa.com/mod_auth_external.html
Source0:	http://mod-auth-external.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_authnz_external-3.2.5.patch
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An apache external authentication module - uses PAM.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}
chmod 644 AUTHENTICATORS CHANGES INSTALL* README TODO
%patch0 -p0

%build

%{_bindir}/apxs -c %{mod_name}.c

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


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-5mdv2011.0
+ Revision: 674426
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-4
+ Revision: 662774
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-3mdv2011.0
+ Revision: 588280
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-2mdv2010.1
+ Revision: 515835
- rebuilt for apache-2.2.15

* Sun Dec 27 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-1mdv2010.1
+ Revision: 482825
- 3.2.5

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-3mdv2010.0
+ Revision: 451698
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-2mdv2010.0
+ Revision: 405136
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-1mdv2010.0
+ Revision: 387622
- 3.2.4
- new url

* Wed Mar 11 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.3-1mdv2009.1
+ Revision: 353767
- 3.2.3

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.1-2mdv2009.1
+ Revision: 326484
- rebuild

* Sun Aug 03 2008 Olivier Thauvin <nanardon@mandriva.org> 3.2.1-1mdv2009.0
+ Revision: 261753
- 3.2.1

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-11mdv2009.0
+ Revision: 235639
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-10mdv2009.0
+ Revision: 215289
- rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-9mdv2008.1
+ Revision: 181433
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 3.1.0-8mdv2008.1
+ Revision: 148459
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-7mdv2008.0
+ Revision: 82359
- rebuild

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-6mdv2008.0
+ Revision: 64319
- use the new %%serverbuild macro

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-5mdv2008.0
+ Revision: 38411
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-4mdv2007.1
+ Revision: 140581
- rebuild

* Tue Feb 27 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-3mdv2007.1
+ Revision: 126610
- general cleanups

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-2mdv2007.1
+ Revision: 79248
- Import apache-mod_authnz_external

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-2mdv2007.0
- rebuild

* Sun Mar 19 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-1mdk
- 3.1.0
- mod_authnz_external is the new name for apache-2.1.x
- drop the register patch

* Mon Dec 12 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-4mdk
- rebuilt against apache-2.2.0

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-3mdk
- rebuilt to provide a -debug package too

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2.10-1mdk
- 2.2.10

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.2.9-3mdk
- added another work around for a rpm bug

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.2.9-2mdk
- added a work around for a rpm bug, "Requires(foo,bar)" don't work

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.2.9-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Thu Mar 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.2.9-6mdk
- use the %%mkrel macro

* Sun Feb 27 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.2.9-5mdk
- fix %%post and %%postun to prevent double restarts

* Wed Feb 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_2.2.9-4mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.2.9-3mdk
- fix deps

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.2.9-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Mon Feb 14 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.2.9-1mdk
- 2.2.9
- drop redundant patches, renumber and rediff patches
- pwauth is in an external package, patches moved there.
- reflect pwauth changes in S1

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.2.7-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.2.7-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.2.7-1mdk
- built for apache 2.0.51

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.2.7-2mdk
- rebuilt
- remove redundant provides

* Mon Aug 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.2.7-1mdk
- built for apache 2.0.50

* Sat Jun 12 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.2.7-1mdk
- built for apache 2.0.49

