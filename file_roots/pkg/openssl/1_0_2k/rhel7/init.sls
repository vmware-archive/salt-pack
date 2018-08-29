{% import "setup/redhat/map.jinja" as buildcfg %}
{% import "setup/macros.jinja" as macros with context %}
{% set pkg_data = salt["pillar.get"]("pkgbuild_registry:" ~ buildcfg.build_release, {}) %}
{% set force = salt["pillar.get"]("pkgbuild_force.all", False) or salt["pillar.get"]("pkgbuild_force." ~ slspath, False) %}
{% set sls_name = "openssl" %}
{% set pypi_name = "openssl" %}

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
    - spec: salt://{{slspath}}/spec/openssl.spec
    - template: jinja
    - tgt: {{buildcfg.build_tgt}}

{{ macros.build_deps(sls_name, pkg_data) }}
{{ macros.requires(sls_name, pkg_data) }}

    - sources:
      - salt://{{slspath}}/sources/renew-dummy-cert
      - salt://{{slspath}}/sources/README.legacy-settings
      - salt://{{slspath}}/sources/README.FIPS
      - salt://{{slspath}}/sources/openssl-thread-test.c
      - salt://{{slspath}}/sources/opensslconf-new-warning.h
      - salt://{{slspath}}/sources/opensslconf-new.h
      - salt://{{slspath}}/sources/openssl-1.0.2k-starttls.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-req-x509.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-ppc-update.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-no-ssl2.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-long-hello.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-fips-randlock.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-cve-2017-3738.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-cve-2017-3737.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-cve-2017-3736.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-cc-reqs.patch
      - salt://{{slspath}}/sources/openssl-1.0.2k-backports.patch
      - salt://{{slspath}}/sources/openssl-1.0.2j-new-fips-reqs.patch
      - salt://{{slspath}}/sources/openssl-1.0.2j-krb5keytab.patch
      - salt://{{slspath}}/sources/openssl-1.0.2j-downgrade-strength.patch
      - salt://{{slspath}}/sources/openssl-1.0.2j-deprecate-algos.patch
      - salt://{{slspath}}/sources/openssl-1.0.2i-trusted-first-doc.patch
      - salt://{{slspath}}/sources/openssl-1.0.2i-secure-getenv.patch
      - salt://{{slspath}}/sources/openssl-1.0.2i-fips.patch
      - salt://{{slspath}}/sources/openssl-1.0.2i-enginesdir.patch
      - salt://{{slspath}}/sources/openssl-1.0.2i-enc-fail.patch
      - salt://{{slspath}}/sources/openssl-1.0.2i-chil-fixes.patch
      - salt://{{slspath}}/sources/openssl-1.0.2h-pkgconfig.patch
      - salt://{{slspath}}/sources/openssl-1.0.2g-manfix.patch
      - salt://{{slspath}}/sources/openssl-1.0.2e-wrap-pad.patch
      - salt://{{slspath}}/sources/openssl-1.0.2e-speed-doc.patch
      - salt://{{slspath}}/sources/openssl-1.0.2e-rpmbuild.patch
      - salt://{{slspath}}/sources/openssl-1.0.2e-remove-nistp224.patch
      - salt://{{slspath}}/sources/openssl-1.0.2d-secp256k1.patch
      - salt://{{slspath}}/sources/openssl-1.0.2c-ecc-suiteb.patch
      - salt://{{slspath}}/sources/openssl-1.0.2c-default-paths.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-x509.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-version.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-version-add-engines.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-test-use-localhost.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-rsa-x931.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-readme-warning.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-padlock64.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-no-rpath.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-issuer-hash.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-ipv6-apps.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-fips-md5-allow.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-fips-ec.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-fips-ctor.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-env-zlib.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-dtls1-abi.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-defaults.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-compat-symbols.patch
      - salt://{{slspath}}/sources/openssl-1.0.2a-apps-dgst.patch
      - salt://{{slspath}}/sources/openssl-1.0.1i-algo-doc.patch
      - salt://{{slspath}}/sources/openssl-1.0.1c-perlfind.patch
      - salt://{{slspath}}/sources/openssl-1.0.1c-aliasing.patch
      - salt://{{slspath}}/sources/openssl-1.0.0-timezone.patch
      - salt://{{slspath}}/sources/openssl-1.0.0-beta4-ca-dir.patch
      - salt://{{slspath}}/sources/Makefile.certificate
      - salt://{{slspath}}/sources/make-dummy-cert
      - salt://{{slspath}}/sources/hobble-openssl
      - salt://{{slspath}}/sources/ectest.c
      - salt://{{slspath}}/sources/ec_curve.c
      - salt://{{slspath}}/sources/openssl-1.0.2k-hobbled.tar.xz

## {#      - {{ macros.pypi_source(pypi_name, version) }} #}

{% endif %}
