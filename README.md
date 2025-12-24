# Ansibles

Ansible configurations for AlmaLinux/RHEL, with DNF, SELinux, firewalld, QEMU+libvirt and Podman. This repo uses quadlet container configs from [tygoee/quadlets](https://github.com/tygoee/quadlets).

Configuration values are in `inventories/`, `roles/<role>/defaults/`, `roles/<role>/vars/`, `host_vars/` and `group_vars/`.

# Running

To run the playbook, run `ansible-playbook main.yml -i inventories/stable.yml`