# Ansibles

Ansible configurations for a Proxmox server with mainly AlmaLinux VMs running Podman. This repo uses quadlet container configs from [tygoee/quadlets](https://github.com/tygoee/quadlets).

Most configuration values are in `inventory/`. Ones usually not needing configuration are in `roles/<role>/defaults/` and `roles/<role>/vars/`.

> [!IMPORTANT]  
> For most containers you will need to modify these variables, otherwise the container might fail silently

# Dependencies

Run the following on the ansible host to install the dependencies required for proxmox playbooks

```sh
ansible-galaxy collection install community.proxmox

# Debian-based
apt install python3-proxmoxer
# RHEL-based
dnf install python3-pip
python3 -m pip install proxmoxer requests
```

# Running

To run the playbooks, run `ansible-playbook playbooks/<playbook>.yml`
