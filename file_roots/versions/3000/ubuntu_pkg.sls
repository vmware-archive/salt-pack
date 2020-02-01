{% import "setup/ubuntu/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'ubuntu1804' %}

    - pkg.salt.3000.ubuntu1804

{% elif buildcfg.build_release == 'ubuntu1604' %}

    - pkg.python-libcloud.1_5_0.ubuntu1604  ## xenial 0.20.0-1
    - pkg.salt.3000.ubuntu1604

{% endif %}
