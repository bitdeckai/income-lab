package com.bitdeck.bletoolkit.ble

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.content.ContextCompat
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class BleRepository(private val context: Context) {
    private val bluetoothManager = context.getSystemService(BluetoothManager::class.java)
    private val adapter: BluetoothAdapter? = bluetoothManager?.adapter
    private val scanner get() = adapter?.bluetoothLeScanner

    private val seen = linkedMapOf<String, String>()
    private val logLines = mutableListOf<String>()

    private val callback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val name = result.device.name ?: "Unknown"
            val addr = result.device.address ?: "N/A"
            val rssi = result.rssi
            seen[addr] = "$name ($addr) RSSI=$rssi"
            log("scan: $name $addr rssi=$rssi")
        }
    }

    fun canScan(): Boolean {
        return hasPermissions() && adapter?.isEnabled == true
    }

    fun startScan(): Boolean {
        if (!canScan()) return false
        log("scan:start")
        scanner?.startScan(callback)
        return true
    }

    fun stopScan() {
        scanner?.stopScan(callback)
        log("scan:stop")
    }

    fun deviceList(): List<String> = seen.values.toList()

    fun connectPreview(index: Int): String {
        val item = deviceList().getOrNull(index) ?: return "No device selected"
        log("connect:preview:$item")
        return "MVP preview connect to: $item"
    }

    fun exportLogs(): String {
        if (logLines.isEmpty()) log("export:empty")
        return logLines.joinToString(separator = "\n")
    }

    private fun log(message: String) {
        val ts = SimpleDateFormat("HH:mm:ss", Locale.US).format(Date())
        logLines += "[$ts] $message"
    }

    private fun hasPermissions(): Boolean {
        return if (Build.VERSION.SDK_INT >= 31) {
            has(Manifest.permission.BLUETOOTH_SCAN) && has(Manifest.permission.BLUETOOTH_CONNECT)
        } else {
            has(Manifest.permission.ACCESS_FINE_LOCATION)
        }
    }

    private fun has(permission: String): Boolean {
        return ContextCompat.checkSelfPermission(context, permission) == PackageManager.PERMISSION_GRANTED
    }
}
