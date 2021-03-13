package com.example.hacktues

import androidx.appcompat.app.AppCompatActivity
import android.os.*
import android.widget.Button
import kotlinx.android.synthetic.main.login_page.*
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.login_page)
        val button: Button = findViewById(R.id.map)
        button.setOnClickListener() {
            setContentView(R.layout.activity_maps)
        }

        val log_in_button: Button = findViewById(R.id.submit)
        log_in_button.setOnClickListener() {

            var reqParam = URLEncoder.encode("username", "UTF-8") + "=" + URLEncoder.encode(
                et_user.toString(),
                "UTF-8"
            )

            reqParam += "&" + URLEncoder.encode("password", "UTF-8") + "=" + URLEncoder.encode(
                et_password.toString(),
                "UTF-8"
            )

            var myURL = URL("192.168.100.166:5000")
            with(myURL.openConnection() as HttpURLConnection) {
                requestMethod = "POST"

                val wr = OutputStreamWriter(getOutputStream());
                wr.write(reqParam);
                wr.flush();

                println("URL : $url")
                println("Response Code : $responseCode")

                BufferedReader(InputStreamReader(inputStream)).use {
                    val response = StringBuffer()

                    var inputLine = it.readLine()
                    while (inputLine != null) {
                        response.append(inputLine)
                        inputLine = it.readLine()
                    }
                    println("Response : $response")
                }
            }
        }
    }
}