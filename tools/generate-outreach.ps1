param(
  [Parameter(Mandatory=$true)] [string]$Name,
  [Parameter(Mandatory=$true)] [string]$Company,
  [Parameter(Mandatory=$true)] [string]$Track,
  [string]$Language = "EN"
)

$offers = @{
  "firmware-ci-saas-kit" = "ESP32 firmware CI/release automation";
  "android-ble-field-toolkit" = "Android BLE field diagnostics toolkit";
  "matter-device-ops-kit" = "Matter deployment and ops toolkit";
}

if (-not $offers.ContainsKey($Track)) {
  Write-Error "Unknown track: $Track"
  exit 1
}

if ($Language -eq "CN") {
@"
你好 $Name，
我是 bitdeckai，最近在做 $($offers[$Track])。
我可以为 $Company 提供一个 1 周内可交付的最小集成版本（含文档和演示）。
如果你愿意，我可以先给你一个免费技术评估，再决定是否进入付费集成。
项目入口：https://github.com/bitdeckai/income-lab
"@
} else {
@"
Hi $Name,
I am building $($offers[$Track]).
I can deliver a 1-week MVP integration package for $Company (with docs and demo).
If helpful, I can start with a free technical assessment before paid integration.
Project: https://github.com/bitdeckai/income-lab
"@
}
