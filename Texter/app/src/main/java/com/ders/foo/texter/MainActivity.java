package com.ders.foo.texter;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;
import java.util.ArrayList;

import okhttp3.RequestBody;
import okhttp3.Response;
import retrofit2.Call;
import retrofit2.Callback;

public class MainActivity extends AppCompatActivity implements Callback<GsonModels.ImageResponse> {

    private static final String TAG = "MainActivity";
    private ProgressDialog progressDialog;
    EditText editText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent intent = getIntent();
        String action = intent.getAction();
        String type = intent.getType();
        editText = findViewById(R.id.content);

        if (Intent.ACTION_SEND.equals(action) && type != null) {
            if ("text/plain".equals(type)) {
                handleSendText(intent); // Handle text being sent
            }
        }
    }

    void handleSendText(Intent intent) {
        String sharedText = intent.getStringExtra(Intent.EXTRA_TEXT);
        if (sharedText != null) {
            // Update UI to reflect text being shared
            editText.setText(sharedText);
            Button submitButton = findViewById(R.id.submit);
            submitButton.performClick();
        }
    }

    public void sendImageRequest(View view) {
        progressDialog = new ProgressDialog(this);
        progressDialog.setMessage("Generating Images");
        progressDialog.setIndeterminate(true);
        progressDialog.setCancelable(false);
        progressDialog.show();
        String content = filter(editText.getText().toString());
        StringBuilder sb = new StringBuilder();
        sb.append("{\"textcontent\":\"");
        sb.append(content);
        sb.append("\"}");
        String body = sb.toString();
        RequestBody requestBody = RequestBody.create(okhttp3.MediaType.parse("application/json; charset=utf-8"), body);
        RetrofitInterface retrofitInterface = ServiceGenerator.createService(RetrofitInterface.class);
        retrofitInterface.getImageUrls(requestBody).enqueue(this);
    }

    private String filter(String s) {
        String newString = "";
        for (int i = 0 ; i < s.length() ; i++) {
            char c = s.charAt(i);
            if (c == '\n') {
                newString += "\\n";
            } else {
                newString += c;
            }
        }
        Log.d(TAG, "filter: " + newString);
        return newString;
    }

    @Override
    public void onResponse(Call<GsonModels.ImageResponse> call, retrofit2.Response<GsonModels.ImageResponse> response) {
        if (response.isSuccessful()) {
            GsonModels.ImageResponse imageResponse = response.body();
            ArrayList<String> imageUrls = imageResponse.getImg_urls();
            ArrayList<String> data = imageResponse.getData();
            Intent intent = new Intent(MainActivity.this, DisplayActivity.class);
            intent.putStringArrayListExtra("IMAGE_URL_LIST", imageUrls);
            intent.putStringArrayListExtra("DATA", data);
            startActivity(intent);
        } else {
            Log.d(TAG, "onResponse: Server Error " + response.code());
        }
        progressDialog.dismiss();
    }

    @Override
    public void onFailure(Call<GsonModels.ImageResponse> call, Throwable t) {
        Toast.makeText(this, "No Internet Connection", Toast.LENGTH_SHORT).show();
        progressDialog.dismiss();
    }
}
