package com.example.hacktues

import androidx.appcompat.app.AppCompatActivity
import android.os.*
import android.widget.Button

class MainActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.login_page)
        val button1: Button = findViewById(R.id.map)
        button1.setOnClickListener(){
            setContentView(R.layout.activity_maps)
        }
    }
}