# Firmware CI SaaS Kit

CN: 面向 ESP32 团队的固件构建与发布自动化方案。
EN: Firmware build and release automation for ESP32 teams.

## Included
- PlatformIO sample firmware (`platformio.ini`, `src/main.cpp`)
- CI workflow: build on PR/push
- Release workflow: build on tag and publish binaries to GitHub Release
- auto release notes script

## Run Local Build
```bash
cd projects/firmware-ci-saas-kit
pio run
```

## Release Flow
1. push a tag like `v0.1.0`
2. workflow builds firmware
3. release notes are generated from commits
4. `firmware.bin`, `bootloader.bin`, `partitions.bin` uploaded to GitHub Release

## Key Files
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `scripts/generate_release_notes.py`
