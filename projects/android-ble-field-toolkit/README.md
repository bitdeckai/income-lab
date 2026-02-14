# Android BLE Field Toolkit

CN: 面向现场调试和产线测试的 Android BLE 工具。
EN: Android BLE toolkit for field diagnostics and production tests.

## MVP Features
- BLE permission request flow
- BLE scan/stop
- device list display
- connect preview (MVP placeholder)
- session logs export to app storage

## Run
```bash
cd projects/android-ble-field-toolkit
./gradlew assembleDebug
```
Windows:
```powershell
cd projects/android-ble-field-toolkit
.\gradlew.bat assembleDebug
```

## Code Entry
- `app/src/main/java/com/bitdeck/bletoolkit/MainActivity.kt`
- `app/src/main/java/com/bitdeck/bletoolkit/ble/BleRepository.kt`

## Sponsor Add-ons (planned)
- batch provisioning
- CSV/JSON report export
- device profile presets
