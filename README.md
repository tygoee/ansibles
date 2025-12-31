# Ansibles

Ansible configurations for AlmaLinux/RHEL, with DNF, SELinux, firewalld, QEMU+libvirt and Podman. This repo uses quadlet container configs from [tygoee/quadlets](https://github.com/tygoee/quadlets).

Most configuration values are in `inventory/`. Ones not needing configuration are in `roles/<role>/defaults/` and `roles/<role>/vars/`.

> [!IMPORTANT]  
> For most containers you will need to modify these variables, otherwise the container might fail silently

# Running

To run the playbook, run `ansible-playbook main.yml -i inventory/stable.yml`