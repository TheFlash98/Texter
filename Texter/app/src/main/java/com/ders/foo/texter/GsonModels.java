package com.ders.foo.texter;

import java.util.ArrayList;

public class GsonModels {
    public class ImageResponse {
        ArrayList<String> img_urls;
        ArrayList<String> data;

        public ImageResponse(ArrayList<String> img_urls, ArrayList<String> data) {
            this.img_urls = img_urls;
            this.data = data;
        }

        public ArrayList<String> getImg_urls() {
            return img_urls;
        }

        public void setImg_urls(ArrayList<String> img_urls) {
            this.img_urls = img_urls;
        }

        public ArrayList<String> getData() {
            return data;
        }

        public void setData(ArrayList<String> data) {
            this.data = data;
        }
    }
}
