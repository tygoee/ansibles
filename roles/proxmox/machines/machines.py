#!/usr/bin/python3
from json import dump
from os import path
from typing import Any, cast
from proxmox import authorized_keys, auth, node, passwords, dns, network

images = {
    "almalinux": "AlmaLinux-10-GenericCloud-latest.x86_64.qcow2"
}


def deep_merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    result = a.copy()

    for key, value in b.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], cast(dict[str, Any], value))
        else:
            result[key] = value

    return result


def almalinux_template(
    name: str, vmid: str | int,
    size: int = 10, override: dict[str, Any] | None = None
): return deep_merge({
    "kvm": {
        "name": name,
        "vmid": vmid,
        "node": node,
        "onboot": True,

        # "vga": "virtio",
        "machine": "q35",
        "bios": "ovmf",
        "efidisk0": {
            "efitype": "4m",
            "format": "raw",
            "pre_enrolled_keys": True,
            "storage": "local-lvm"
        },
        "scsihw": "virtio-scsi-single",
        "agent": "1",
        "tpmstate0": {
            "storage": "local-lvm",
            "version": "2.0"
        },

        "scsi": {
            "scsi0": f"local-lvm:0,import-from=local:import/{images['almalinux']},iothread=on"
        },

        "sockets": "1",
        "cores": "4",
        "cpu": "host",
        "numa_enabled": True,

        "memory": "4096",
        # "balloon": "2048",

        "net": {
            "net0": "virtio,bridge=vmbr0,firewall=1"
        },

        "searchdomains": dns["searchdomains"],
        "nameservers": dns["nameservers"],

        "hotplug": "network,disk,cpu,memory,usb",

        "ide": {
            "ide2": "local-lvm:cloudinit,format=raw"
        },
        "sshkeys": authorized_keys,
        "ciupgrade": True,
        "ciuser": "almalinux",
        "cipassword": passwords[name],
        "ipconfig": network(vmid)
    },
    "firewall": {
        "level": "vm",
        "vmid": vmid,
        "rules": [
            {
                "type": "in",
                "action": "ACCEPT",
                "macro": "SSH",
                "pos": 0,
                "log": "nolog",
                "enable": True
            }
        ]
    },
    "disk": {
        "when":
            f"proxmox_vms[{vmid}].config.scsi0 | trim == "
            f"'local-lvm:vm-{vmid}-disk-1,iothread=1,size=10G'",
            "set": {
                "vmid": vmid,
                "disk": "scsi0",
                "size": f"+{int(size)-10}G",
                "state": "resized"
            }
    }
}, override if override is not None else {})


machines = {
    "almalinux_infra": almalinux_template("almalinux-infra", 101, 40, {"kvm": {"memory": "8192"}}),
    "almalinux_main": almalinux_template("almalinux-main", 102, 40),
    "almalinux_media": almalinux_template("almalinux-media", 103, 40, {"kvm": {"onboot": False}}),
    "almalinux_games": almalinux_template("almalinux-games", 104, 100, {"kvm": {"memory": "8192", "onboot": False}})
}

with open(path.join(path.dirname(path.realpath(__file__)), "machines.json"), 'w') as fp:
    dump({
        "auth": auth,
        "node": node,
        "machines": machines
    }, fp, indent=4)
