# Restore the Pi software on another Raspberry Pi

This release preserves the installed files from the source Pi, including Miniforge, the lerobot_alohamini environment, .local packages, Demo_Project/env, other installed software, caches, and oversized project files. Credential/account state and nested Git history are excluded; HOME_MANIFEST.json lists the exclusions.

## Compatibility

Use a 64-bit ARM Raspberry Pi with a compatible Debian 12 / Raspberry Pi OS Bookworm installation. The source paths are /home/pi and /home/pi/miniforge3. Restoring to those same paths avoids changing Conda's embedded installation prefixes. A different OS, CPU architecture, Python ABI, username/path, kernel, or missing system library can prevent copied software from working.

This is a copy of the existing software state, not an SD-card image or proof that every package/application works. It does not include the source Pi's /usr, /etc, drivers, system services or full operating system. The included Debian package inventory and OS details are references for installing required system dependencies.

## Direct restore on a fresh Pi

For a workflow that avoids a second full extracted copy, see [DIRECT_RESTORE.md](DIRECT_RESTORE.md). The staged inspection workflow below requires more free space.

## Download and verify

Download download-software.py from this release, then run it with Python 3 on the destination Pi. It downloads the assets into pi-home-download and verifies SHA256SUMS.

    python3 download-software.py
    cd pi-home-download
    sha256sum --check SHA256SUMS

Use a filesystem with sufficient free space. The download, extracted staging copy and final home files can temporarily coexist; at least 50 GB free is a reasonable allowance for this workflow.

## Extract for inspection

    mkdir -p /home/pi/pi-import
    cat pi-home-software.tar.gz.part-* | tar -xz -C /home/pi/pi-import

The extracted files are under /home/pi/pi-import/home/pi. Metadata is under /home/pi/pi-import/_pi_transfer_metadata.

## Place software at its original paths

On a fresh destination Pi, after inspecting the files and preserving any existing destination files you need:

    cp -a /home/pi/pi-import/home/pi/. /home/pi/

This merges and overwrites matching destination files. Do not run it over an existing configured Pi without reviewing the affected files. It also restores startup files such as .bashrc and .profile; review them for machine-specific paths and old proxy settings before using a new shell.

The archives preserve hard links and symlinks. The optional copy step may require additional disk space. Keep the software under /home/pi/miniforge3 if you want to reuse the original Conda prefixes. To relocate an environment to a different path, use Conda-Pack or recreate it from environment specifications rather than moving this directory arbitrarily.

## Check the copied environment

    /home/pi/miniforge3/bin/python --version
    source /home/pi/miniforge3/bin/activate /home/pi/miniforge3/envs/lerobot_alohamini
    python --version
    conda env list

The source Python version probes are included in python-version-probes.json. These checks do not establish that the robot, camera, motors, GPU-dependent packages or every application works. Install matching system dependencies and test the intended application on the destination Pi.

Reconfigure Wi-Fi, VPN, SSH keys, account logins and other credentials yourself; those were excluded. Preserve each included package/project's original licenses.

Archive data comes from live source files rather than an atomic filesystem snapshot. Compression decoding and tar listing were checked during packaging, and every release asset was verified against GitHub's SHA256 digest.
