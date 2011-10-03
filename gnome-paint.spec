%define Werror_cflags %nil

Name:           gnome-paint
Version:        0.4.0
Release:        %mkrel 1
Summary:        Easy to use paint program

Group:          Graphics
License:        GPLv3+
URL:            https://launchpad.net/gnome-paint
Source0:        http://launchpad.net/%{name}/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:		gnome-paint.packaging.patch
#debian patches
Patch1:		debian-612470-handle-urls.patch
Patch2:		lp-757607-crash-in-toolbar.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  intltool gtk2-devel desktop-file-utils
Requires:       hicolor-icon-theme

%description
gnome-paint is a simple, easy to use paint program.

%prep
%setup -q
%apply_patches
# remove icon extensions
sed -i 's|Icon=gp.png|Icon=gp|g' data/desktop/%{name}.desktop.in.in
sed -i 's|RasterGraphics;|2DGraphics;RasterGraphics;|g' data/desktop/%{name}.desktop.in.in

%build
autoreconf -fi
%configure
%make


%install 
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove docs, use rpmbuild instead
rm -rf $RPM_BUILD_ROOT/%{_prefix}/doc
# remove unnecessary includedir files
rm -rf $RPM_BUILD_ROOT/%{_includedir}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
%find_lang gnome_paint


%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%files -f gnome_paint.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_bindir}/gnome-paint
%{_datadir}/applications/gnome-paint.desktop
%{_datadir}/gnome-paint/
%{_datadir}/icons/hicolor/16x16/apps/gp.png
%{_localedir}