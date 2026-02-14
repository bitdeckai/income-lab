package com.bitdeck.bletoolkit

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.ListView
import android.widget.TextView
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.bitdeck.bletoolkit.ble.BleRepository
import java.io.File

class MainActivity : AppCompatActivity() {
    private lateinit var repo: BleRepository
    private lateinit var status: TextView
    private lateinit var listView: ListView
    private lateinit var adapter: ArrayAdapter<String>

    private val permissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) {
            renderStatus("Permission result received")
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        repo = BleRepository(this)
        status = findViewById(R.id.statusText)
        listView = findViewById(R.id.deviceList)
        adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, mutableListOf())
        listView.adapter = adapter

        findViewById<Button>(R.id.btnPermission).setOnClickListener { requestBlePermissions() }
        findViewById<Button>(R.id.btnScan).setOnClickListener { startScan() }
        findViewById<Button>(R.id.btnStop).setOnClickListener { stopScan() }
        findViewById<Button>(R.id.btnConnectPreview).setOnClickListener { connectPreview() }
        findViewById<Button>(R.id.btnExport).setOnClickListener { exportLogs() }

        renderStatus("Ready")
    }

    private fun requestBlePermissions() {
        val perms = if (Build.VERSION.SDK_INT >= 31) {
            arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
        } else {
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
        }
        permissionLauncher.launch(perms)
    }

    private fun startScan() {
        if (!repo.canScan()) {
            renderStatus("Enable Bluetooth and grant permissions")
            return
        }
        repo.startScan()
        refreshList()
        renderStatus("Scanning...")
    }

    private fun stopScan() {
        repo.stopScan()
        refreshList()
        renderStatus("Scan stopped")
    }

    private fun connectPreview() {
        val msg = repo.connectPreview(0)
        renderStatus(msg)
    }

    private fun exportLogs() {
        val content = repo.exportLogs()
        val out = File(getExternalFilesDir(null), "ble_session_log.txt")
        out.writeText(content)
        renderStatus("Logs exported: ${out.absolutePath}")
    }

    private fun refreshList() {
        adapter.clear()
        adapter.addAll(repo.deviceList())
        adapter.notifyDataSetChanged()
    }

    private fun renderStatus(text: String) {
        status.text = text
    }
}
