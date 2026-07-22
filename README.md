# Ansibles

Ansible configurations for a Proxmox server with mainly AlmaLinux VMs running Podman. This repo uses quadlet container configs from [tygoee/quadlets](https://github.com/tygoee/quadlets).

Most configuration values are in `inventory/`. Ones usually not needing configuration are in `roles/<role>/defaults/` and `roles/<role>/vars/`.

> [!IMPORTANT]  
> For most containers you will need to modify these variables, otherwise the container might fail silently

# Dependencies

Run the following on the ansible host (here configured to be a 'toolbox' lxc inside proxmox) to install the dependencies required for proxmox playbooks

```sh
ansible-galaxy collection install community.proxmox containers.podman

# Debian-based
apt install -y python3-proxmoxer
# RHEL-based
dnf install -y python3-pip
python3 -m pip install proxmoxer requests
```

# Running

Before creating new virtual machines, generate the `machines.json` file with `python3 inventory/host_vars/toolbox/machines.py`

To run the playbooks, run `ansible-playbook playbooks/<playbook>.yml`
