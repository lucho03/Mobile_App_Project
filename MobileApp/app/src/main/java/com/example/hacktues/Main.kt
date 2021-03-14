package com.example.hacktues

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private lateinit var imageView: ImageView
    private lateinit var imageButton: Button
    private lateinit var take_photoButton: Button
    private lateinit var locationButton: Button
    private lateinit var sendButton: Button
    private var imageData: ByteArray? = null
    private val postURL: String = "http://46.47.78.154:5000/report_test" // remember to use your own api

    companion object {
        private const val IMAGE_PICK_CODE = 999
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.send_image)

        imageView = findViewById(R.id.imageView)

        imageButton = findViewById(R.id.imageButton)
        imageButton.setOnClickListener {
            launchGallery()
        }

        take_photoButton = findViewById(R.id.take_photoButton)
        take_photoButton.setOnClickListener {
            setContentView(R.layout.camera_interface)

        }


        locationButton = findViewById(R.id.locationButton)
        locationButton.setOnClickListener {
            setContentView(R.layout.activity_maps)
        }

        sendButton = findViewById(R.id.sendButton)
        sendButton.setOnClickListener {
            uploadImage()
        }
    }

    private fun launchGallery() {
        val intent = Intent(Intent.ACTION_PICK)
        intent.type = "image/*"
        startActivityForResult(intent, IMAGE_PICK_CODE)
    }

    private fun uploadImage() {
        imageData?: return
        val request = object : VolleyFileUploadRequest(
            Method.POST,
            postURL,
            Response.Listener {
                println("response is: $it")
            },
            Response.ErrorListener {
                println("error is: $it")
            }
        ) {
            override fun getByteData(): MutableMap<String, FileDataPart> {
                var params = HashMap<String, FileDataPart>()
                params["imageFile"] = FileDataPart("image", imageData!!, "jpeg")
                return params
            }
        }
        Volley.newRequestQueue(this).add(request)
    }

    @Throws(IOException::class)
    private fun createImageData(uri: Uri) {
        val inputStream = contentResolver.openInputStream(uri)
        inputStream?.buffered()?.use {
            imageData = it.readBytes()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (resultCode == Activity.RESULT_OK && requestCode == IMAGE_PICK_CODE) {
            val uri = data?.data
            if (uri != null) {
                imageView.setImageURI(uri)
                createImageData(uri)
            }
        }
        super.onActivityResult(requestCode, resultCode, data)
    }
}


//package com.example.hacktues
//import android.os.Bundle
//import android.widget.Button
//import android.widget.EditText
//import androidx.appcompat.app.AppCompatActivity
//import java.io.BufferedReader
//import java.io.InputStreamReader
//import java.io.OutputStreamWriter
//import java.net.HttpURLConnection
//import java.net.URL
//import java.net.URLEncoder
//
//class MainActivity : AppCompatActivity() {
//    fun sendPostRequest(userName:String, password:String) {
//    var reqParam = URLEncoder.encode("username", "UTF-8") + "=" + URLEncoder.encode(userName, "UTF-8")
//    reqParam += "&" + URLEncoder.encode("password", "UTF-8") + "=" + URLEncoder.encode(password, "UTF-8")
//    val mURL = URL("http://46.47.78.154:5000/")
//
//    with(mURL.openConnection() as HttpURLConnection) {
//        // optional default is GET
//        requestMethod = "POST"
//
//        val wr = OutputStreamWriter(getOutputStream());
//        wr.write(reqParam);
//        wr.flush();
//
//        println("URL : $url")
//        println("Response Code : $responseCode")
//
//        BufferedReader(InputStreamReader(inputStream)).use {
//            val response = StringBuffer()
//
//            var inputLine = it.readLine()
//            while (inputLine != null) {
//                response.append(inputLine)
//                inputLine = it.readLine()
//            }
//            println("Response : $response")
//        }
//    }
//}
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//        setContentView(R.layout.login_page)
//        var etUserName = findViewById<EditText>(R.id.et_user)
//        var etPassword = findViewById<EditText>(R.id.et_password)
//        val mapButton = findViewById<Button>(R.id.map)
//        var logInButton : Button = findViewById<Button>(R.id.submit)
//        mapButton.setOnClickListener() {
//            setContentView(R.layout.activity_maps)
//        }
//        logInButton.setOnClickListener() {
////            Thread thread = new Thread(new Runnable() {
////
////                @Override
////                public void run() {
////                    try  {
//                        sendPostRequest(etUserName.toString(), etPassword.toString())
////                    } catch (Exception e) {
////                        e.printStackTrace();
////                    }
////                }
////            });
////
////            thread.start();
//
//        }
//    }
//}