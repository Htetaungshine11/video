const uploadForm = document.getElementById("upload-form");
const input = document.getElementById("id_video");
const alertBox = document.getElementById("alert-box");
const imageBox = document.getElementById("image-box");
const progressBox = document.getElementById("progress-box");
const cancelBox = document.getElementById("cancel-box");
const cancelBtn = document.getElementById("cancel-btn");
const name1 = document.getElementById("id_name");
const csrf = document.getElementsByName("csrfmiddlewaretoken");

input.addEventListener("change", () => {
  progressBox.classList.remove("not-visible");
  cancelBox.classList.remove("not-visible");

  const img_data = input.files[0];
  const fd = new FormData();
  fd.append("csrfmiddlewaretoken", csrf[0].value);
  fd.append("video", img_data);
  fd.append("name", name1.value);
  $.ajax({
    type: "POST",
    url: uploadForm.action,
    enctype: "multipart/form-data",
    data: fd,
    beforeSend: function () {
      alertBox.innerHTML = "";
    },
    xhr: function () {
      const xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", (e) => {
        if (e.lengthComputable) {
          const percent = (e.loaded / e.total) * 100;
          console.log(percent);
          progressBox.innerHTML = `<div class="progress">
                                                <div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <p>${percent.toFixed(1)}%</p>`;
        }
      });
      cancelBtn.addEventListener("click", () => {
        xhr.abort();
        setTimeout(() => {
          uploadForm.reset();
          progressBox.innerHTML = "";
          alertBox.innerHTML = "";
          cancelBox.classList.add("not-visible");
        }, 2000);
      });
      return xhr;
    },
    success: function (response) {
      name1.value = "";

      alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                    Successfully uploaded the image below
                                </div>`;
      cancelBox.classList.add("not-visible");
    },
    error: function (error) {
      console.log(error);
      alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                    Ups... something went wrong
                                </div>`;
    },
    cache: false,
    contentType: false,
    processData: false,
  });
});
