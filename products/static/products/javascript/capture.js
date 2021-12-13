(function () {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video, canvas, photo, startbutton = null;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton')

    video.addEventListener('canplay', function (ev) {
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width);

        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.

        if (isNaN(height)) {
          height = width / (4 / 3);
        }

        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
        setTimeout(takepicture, 1000);
      }
    }, false);
  }

  function startVideo() {
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      .then(function (stream) {
        video.srcObject = stream;
        video.play();
        startbutton.innerText = "Scanning..."
      })
      .catch(function (err) {
        console.log("An error occurred: " + err);
      });
  }

  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a JPEG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.
  let picturesCount = 1
  function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);

      var dataURL = canvas.toDataURL('image/jpeg');

      const data = { 'dataURL': dataURL };

      fetch('https://janscan.herokuapp.com/products/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then(response => response)
        .then(data => {
          if (data.ok) {
            console.log('Success:', data);
            window.location = data.url;
          } else if (picturesCount >= 10) {
            stopVideo(video);
            alert('Unable to process barcode. Please try again.');
          } else if (streaming) {
            console.log('Failed:', data);
            picturesCount++
            setTimeout(takepicture, 1000)
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }
  }

  function stopVideo(videoElem) {
    const stream = videoElem.srcObject;
    const tracks = stream.getTracks();

    tracks.forEach(function (track) {
      track.stop();
    });

    videoElem.srcObject = null;
    streaming = false;
    picturesCount = 0;
    startbutton.innerText = "Start Scanning"
  }

  // Set up our event listener to run the startup process
  // once loading is complete.
  window.addEventListener('load', startup, false);
  window.addEventListener('click', (e) => {
    if (e.target.id == "startbutton") {
      if (!streaming) {
        startVideo();
      } else {
        stopVideo(video);
      }
    }
  });
})();
