package com.ders.foo.texter;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;

public class DisplayActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display);

        if (getIntent() != null) {
            Intent intent = getIntent();
            ArrayList<String> imageUrls = intent.getStringArrayListExtra("IMAGE_URL_LIST");
            ArrayList<String> data = intent.getStringArrayListExtra("DATA");

            LinearLayout linearLayout = findViewById(R.id.linearlayout);
            ViewGroup.LayoutParams lparams = new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            for (int i = 0 ; i < data.size() ; i++) {
                TextView textView = new TextView(this);
                textView.setLayoutParams(lparams);
                textView.setText(data.get(i));
                textView.setTextColor(getResources().getColor(R.color.colorBlack));
                linearLayout.addView(textView);
                if (imageUrls.get(i) != null && !imageUrls.get(i).isEmpty()) {
                    ImageView imageView = new ImageView(this);
                    imageView.setLayoutParams(lparams);
                    Picasso.with(this).load(imageUrls.get(i)).into(imageView);
                    linearLayout.addView(imageView);
                }
            }
        }
    }
}
