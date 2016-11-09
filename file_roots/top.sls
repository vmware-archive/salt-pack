# Import build branch
{% import "setup/base_map.jinja" as versioncfg %}

'base':
  'G@os_family:Redhat and G@os:Amazon':
   - {{versioncfg.amazon_pkg}}

  'G@os_family:Redhat and not G@os:Amazon':
   - {{versioncfg.redhat_pkg}}

  'G@osfullname:Debian or G@osfullname:Raspbian':
    - {{versioncfg.debian_pkg}}

  'G@osfullname:Ubuntu':
    - {{versioncfg.ubuntu_pkg}}


