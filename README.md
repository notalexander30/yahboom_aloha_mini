# yahboom_aloha_mini

Current-file snapshot of shareable files from `/home/pi` on the Yahboom Raspberry Pi, uploaded on 12 October 2026.

Project folders, demos, scripts, documents, datasets, and model files below GitHub's regular file limit retain their original directory layout. This repository is not a complete system or home-directory backup.

## Exclusions

`UPLOAD_MANIFEST.json` lists every excluded path or directory and the reason. Exclusions include private account and application state, credentials, caches, installed software environments, nested Git history, special files, and files at or above 100 MiB. A secret scan also excluded one documentation JavaScript file with an API-key finding. Some third-party binary assets use Git LFS pointer files in their original projects; these pointers require the original upstream LFS storage to recover the assets.

Original files on the Pi were not deleted or changed. The source code was not modified or tested as part of this upload.

## Third-party projects

Project-specific README and LICENSE files remain within their respective directories. Original project attribution and licenses still apply.

- `lerobot_alohamini/`: source from https://github.com/liyiteng/lerobot_alohamini, original commit `7843e588`.
- `ultralytics/`: existing Ultralytics checkout from the Pi.

Secrets and installed dependency environments must not be added to this public repository.

## Installed software for another Pi

The installed software and shareable home files are available as split archives in the [Pi software release](https://github.com/notalexander30/yahboom_aloha_mini/releases/tag/pi-home-software-2026-10-12). This includes Miniforge environments, .local packages, caches and oversized files omitted from the regular Git tree. See [PI_RESTORE.md](PI_RESTORE.md) for downloading and restoring on a compatible ARM64 Debian 12 Pi. Credential/account state is excluded.
