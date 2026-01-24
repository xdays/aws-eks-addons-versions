#!/usr/bin/env python3
"""Fetch AWS EKS addon versions and save to JSON."""

import json
from collections import defaultdict
from pathlib import Path

import boto3


def fetch_addon_versions():
    """Fetch all EKS addon versions using boto3 paginator."""
    client = boto3.client("eks")
    paginator = client.get_paginator("describe_addon_versions")

    addons = {}

    for page in paginator.paginate():
        for addon in page.get("addons", []):
            addon_name = addon["addonName"]
            owner = addon.get("owner", "")
            addon_type = addon.get("type", "")

            # Skip marketplace addons - only include AWS-owned addons
            if owner and "aws" not in owner.lower():
                continue

            if addon_name not in addons:
                addons[addon_name] = {
                    "name": addon_name,
                    "owner": owner,
                    "type": addon_type,
                    "publisher": addon.get("publisher", ""),
                    "versions_by_eks": defaultdict(list),
                }

            for version_info in addon.get("addonVersions", []):
                addon_version = version_info["addonVersion"]
                requires_config = version_info.get("requiresConfiguration", [])
                if isinstance(requires_config, list):
                    requires_iam = any(
                        config.get("requiresIamPermissions", False)
                        for config in requires_config
                    )
                else:
                    requires_iam = bool(requires_config)

                for compat in version_info.get("compatibilities", []):
                    eks_version = compat["clusterVersion"]
                    is_default = compat.get("defaultVersion", False)

                    addons[addon_name]["versions_by_eks"][eks_version].append({
                        "version": addon_version,
                        "default": is_default,
                        "requires_iam": requires_iam,
                    })

    # Convert defaultdict to regular dict and sort versions
    result = []
    for addon_name, addon_data in sorted(addons.items()):
        versions_by_eks = {}
        for eks_version, versions in addon_data["versions_by_eks"].items():
            # Sort versions: default first, then by version string descending
            sorted_versions = sorted(
                versions,
                key=lambda v: (not v["default"], v["version"]),
                reverse=False,
            )
            # Remove duplicates while preserving order
            seen = set()
            unique_versions = []
            for v in sorted_versions:
                if v["version"] not in seen:
                    seen.add(v["version"])
                    unique_versions.append(v)
            versions_by_eks[eks_version] = unique_versions

        result.append({
            "name": addon_data["name"],
            "owner": addon_data["owner"],
            "type": addon_data["type"],
            "publisher": addon_data["publisher"],
            "versions_by_eks": versions_by_eks,
        })

    # Get all EKS versions and sort them
    all_eks_versions = set()
    for addon in result:
        all_eks_versions.update(addon["versions_by_eks"].keys())

    eks_versions = sorted(all_eks_versions, key=lambda v: [int(x) for x in v.split(".")], reverse=True)

    return {
        "eks_versions": eks_versions,
        "addons": result,
    }


def main():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    data = fetch_addon_versions()

    output_file = output_dir / "addons_data.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Fetched {len(data['addons'])} addons across {len(data['eks_versions'])} EKS versions")
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()
