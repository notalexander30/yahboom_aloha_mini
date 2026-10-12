# Restore directly on a fresh compatible Pi

This option avoids keeping both an extracted staging copy and a second final home-directory copy.

Use a fresh 64-bit ARM Debian 12 / Raspberry Pi OS Bookworm Pi with the user home at /home/pi. Allow at least 32 GB of free space before downloading: the archive parts total about 10.7 GB and the restored files about 16.6 GB. Additional system packages and operating-system files need their own space.

1. Download all release assets using download-software.py.
2. Open a terminal in the generated pi-home-download folder.
3. Verify the downloaded files:

       sha256sum --check SHA256SUMS

4. Review HOME_MANIFEST.json, the source OS/package metadata, and any existing destination files you need to preserve. The following command overwrites matching files under /home/pi, including .bashrc and .profile. Use it on a fresh destination rather than an existing configured Pi.

5. Stream the archive directly into its original home path:

       cat pi-home-software.tar.gz.part-* | tar -xz --strip-components=2 -C /home/pi home/pi

Only the home/pi subtree is selected. No combined archive file or second extracted copy is required. Hard links and symlinks are preserved by GNU tar; stripping the prefix adjusts hard-link paths too.

6. Review the restored .bashrc and .profile for old proxy settings and machine-specific commands before opening a new shell. Then check and activate the copied environment:

       /home/pi/miniforge3/bin/python --version
       source /home/pi/miniforge3/bin/activate /home/pi/miniforge3/envs/lerobot_alohamini
       python --version
       conda env list

The source environment paths are /home/pi/miniforge3 and /home/pi/miniforge3/envs/lerobot_alohamini. Moving them to other paths can break embedded Conda prefixes. Use Conda-Pack or recreate the environment if you need a different location.

This archive does not contain the source Pi's /usr, /etc, kernel, drivers, Docker image storage, or full operating system. Check debian-packages.tsv and the OS metadata for required system dependencies. Reconfigure credentials and account logins separately. Copying the files preserves the existing software state; it does not establish that every application or robot device works.

The stream-extraction command and preservation of hard links were checked with GNU tar on the source Pi using a small fixture.

