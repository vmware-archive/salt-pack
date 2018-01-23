base:
  '*':
    - gpg_keys
    - pkgbuild
{% if grains['virtualization'] == 'vagrant' %}
    - vagrant
{% endif %}