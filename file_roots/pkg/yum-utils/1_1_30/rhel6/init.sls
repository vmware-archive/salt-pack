{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "yum-utils" %}

{% set pkg_info = pkg_data.get(sls_name, {}) %}
{% if "version" in pkg_info %}
  {% set pkg_name = pkg_info.get("name", sls_name) %}
  {% set version, release = pkg_info["version"].split("-", 1) %}
  {% if pkg_info.get("noarch", False) %}
    {% set arch = "noarch" %}
  {% else %}
    {% set arch = buildcfg.build_arch %}
  {% endif %}

{{ macros.includes(sls_name, pkg_data) }}

{{sls_name}}-{{version}}:
  pkgbuild.built:
    - runas: {{buildcfg.build_runas}}
    - force: {{force}}

{{ macros.results(sls_name, pkg_data) }}

    - dest_dir: {{buildcfg.build_dest_dir}}
    - spec: salt://{{slspath}}/spec/{{pkg_name}}.spec
    - template: jinja
    - tgt: {{buildcfg.build_tgt}}

{{ macros.build_deps(sls_name, pkg_data) }}
{{ macros.requires(sls_name, pkg_data) }}

    - sources:
      # Can't use the Google Code link because the URL causes Salt to cache the
      # file with a non-matching filename. TODO: Fix this.
      #- https://code.google.com/p/{{pkg_name}}/downloads/detail?name=libpgm-{{version}}.tar.gz
      - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}.tar.gz
      - salt://{{slspath}}/sources/{{pkg_name}}-{{version}}-i18n-off.patch
      - salt://{{slspath}}/sources/BZ-676193-debug-rpms-repo-name.patch
      - salt://{{slspath}}/sources/BZ-669178-fs-snapshot-hard-failure.patch
      - salt://{{slspath}}/sources/BZ-659740-Force-ASCII-apostrophes-in-man-page-examples.patch
      - salt://{{slspath}}/sources/BZ-616408-yumdownloader-man-page-archlist.patch
      - salt://{{slspath}}/sources/BZ-1097560-repoquery-handle-yum-config-exceptions.patch
      - salt://{{slspath}}/sources/BZ-1097297-save-setopt-with-wildcards.patch
      - salt://{{slspath}}/sources/BZ-1078724-needs-restarting-traceback.patch
      - salt://{{slspath}}/sources/BZ-1078724-needs-restarting-start-time.patch
      - salt://{{slspath}}/sources/BZ-1078724-needs-restarting-get-open-files.patch
      - salt://{{slspath}}/sources/BZ-1078724-handle-ioerrors.patch
      - salt://{{slspath}}/sources/BZ-1078724-filenames-deleted.patch
      - salt://{{slspath}}/sources/BZ-1078724-catch-ioerror.patch
      - salt://{{slspath}}/sources/BZ-1075705-yum-config-manager-save.patch
      - salt://{{slspath}}/sources/BZ-1045494-yum-post-transaction-fail-when-package-removed.patch
      - salt://{{slspath}}/sources/BZ-1026317-yum-security-manpage-sec-severity-option.patch
      - salt://{{slspath}}/sources/BZ-1015191-reposync-manpage-plugins-option.patch
      - salt://{{slspath}}/sources/BZ-1013475-yum-complete-transaction.patch
      - salt://{{slspath}}/sources/BZ-1004089-yumdownloader-download-existing-oversize-rpms.patch
      - salt://{{slspath}}/sources/BZ-998892-yumdownloader-print-depsolving-errors.patch
      - salt://{{slspath}}/sources/BZ-984119-yum-complete-transaction-leaves-yum-pid.patch
      - salt://{{slspath}}/sources/BZ-981773-missing-man-pages.patch
      - salt://{{slspath}}/sources/BZ-981773-all_manpages.patch
      - salt://{{slspath}}/sources/BZ-971598-yum-config-manager-repo-name.patch
      - salt://{{slspath}}/sources/BZ-954358-revert-fs-snapshot-workaround.patch
      - salt://{{slspath}}/sources/BZ-954358-fs-snapshot-LVM.patch
      - salt://{{slspath}}/sources/BZ-901506-fix-exit-status.patch
      - salt://{{slspath}}/sources/BZ-880944-repoquery-repofrompath-timestamps.patch
      - salt://{{slspath}}/sources/BZ-850612-fs-snapshot.patch
      - salt://{{slspath}}/sources/BZ-838158-debuginfo-install-meaningful-error-couldnt-find-package.patch
      - salt://{{slspath}}/sources/BZ-808347-source-rpms.patch
      - salt://{{slspath}}/sources/BZ-802784-repodiff-file-uri.patch
      - salt://{{slspath}}/sources/BZ-782338-package-cleanup-man-page.patch
      - salt://{{slspath}}/sources/BZ-769775-package-cleanup-oldkernels-kernel-PAE.patch
      - salt://{{slspath}}/sources/BZ-737597-yum-debug-restore-man.patch
      - salt://{{slspath}}/sources/BZ-737597-restore-installonly-pkgs.patch
      - salt://{{slspath}}/sources/BZ-734428-workaround-update-man-excludes.patch
      - salt://{{slspath}}/sources/BZ-720967-security-man-page-typos.patch
      - salt://{{slspath}}/sources/BZ-713108-reposync-reposetup-rhn.patch
      - salt://{{slspath}}/sources/BZ-711767-dont-download-again.patch
      - salt://{{slspath}}/sources/BZ-710579-add-compare-arch.patch
      - salt://{{slspath}}/sources/BZ-710469-rhn-source-repos.patch
      - salt://{{slspath}}/sources/BZ-709043-check-doutilbuildtransaction.patch
      - salt://{{slspath}}/sources/BZ-701096-reposync-exit.patch
      - salt://{{slspath}}/sources/BZ-699469+699470-yumdownloader-exit-err-failed-to-download.patch
      - salt://{{slspath}}/sources/BZ-694188-yum-groups-manager-config-file.patch
      - salt://{{slspath}}/sources/BZ-684925-show-changed-rco.patch
      - salt://{{slspath}}/sources/BZ-679098-y-c-m-interpreted-values.patch
{% endif %}
