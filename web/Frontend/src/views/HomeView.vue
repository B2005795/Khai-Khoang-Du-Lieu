<template>
  <h1 class="heading">Hệ Thống Nhận Dạng Sâu Bệnh Hại</h1>

  <div class="container">
    <div class="row">
      <div class="col-5">
        <div class="side-left">
          <button type="button" class="btn btn-primary" @click="clickToInputFile()">
            Upload hình ảnh
          </button>
          <input type="file" id="upload-img" accept="image/png, image/jpeg" hidden @change="displayImg()" />

          <div class="img-wrapper">
            <img class="cur-img" src="../assets/logo-ctu.png" />
          </div>
        </div>        
      </div>
      <div class="col-2">
        <div class="btn-recognize">
          <button type="button" class="btn btn-success" @click="predictClassName()">Nhận dạng</button>
        </div>
      </div>
      <div class="col-5">
        <h2>Kết quả nhận dạng: </h2>
        <br />
        <h3 v-for="(name, index) in names" :key="index">{{name}} ({{confidences[index]}})</h3>
      </div>
    </div>

    <div class="row">
      <div class="col-2" v-for="(cropped, index) in imagesDetect" :key="index">
        <div class="img-wrapper">
            <img class="crop-img" :src="'data:image/jpeg;base64,' + cropped" />
          </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      names: [],
      confidences: [],
      imagesDetect: []
    }
  },
  methods: {
    async clickToInputFile() {
      const file = await document.getElementById('upload-img');
      file.click();
    },

    async displayImg() {
      const file = await document.getElementById('upload-img').files[0]

      const imgElement = await document.getElementsByClassName('cur-img')[0]
      imgElement.src = URL.createObjectURL(file)
    },

    async predictClassName() {
      const classnames = ["Sâu đục quả", "Châu chấu", "Sâu cuốn lá", "Bọ hung", "Bươm bướm đêm", "Nhện đỏ", "Rệp sáp", "Ốc", "Bọ sừng", "Bọ xít"]

      const file = await document.getElementById('upload-img').files[0]
      const form = new FormData()
      form.append('file', file)
      const res = await axios.post('http://127.0.0.1:2409/api/predict', form, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      const temp = res.data.detected_classes;
      this.confidences = res.data.confidences;
      this.imagesDetect = res.data.detected_images;
      
      for(let i = 0; i < temp.length; i++) {
        const idx = temp[i];
        this.names.push(classnames[idx]);
      }
    }
  }
}
</script>
<style scoped>
.heading {
  margin-top: 24px;
  text-align: center;
  color: red;
  text-transform: uppercase;
}

.container {
  margin-top: 32px;
}

.img-wrapper {
  margin-top: 24px;
  width: 100%;
}

.cur-img,
.img,
.crop-img {
  width: 100%;
}

.btn-recognize {
  display: flex;
  align-items: center;
  height: 100%;
}

.btn-recognize .btn {
  min-width: 100%;
  padding-top: 10px;
  padding-bottom: 10px;
  font-size: 18px;
}
</style>