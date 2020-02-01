{% import "setup/ubuntu/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'ubuntu1804' %}

    - pkg.salt.master.ubuntu1804

{% elif buildcfg.build_release == 'ubuntu1604' %}

    - pkg.python-backports-abc.0_5.ubuntu1604
    - pkg.python-libcloud.1_5_0.ubuntu1604  ## xenial 0.20.0-1
    - pkg.python-msgpack.0_6_2.ubuntu1604
    - pkg.salt.master.ubuntu1604

{% endif %}
