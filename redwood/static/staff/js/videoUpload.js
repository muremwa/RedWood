/* 
    Ensure all fields are entered before enabling video upload form
*/
const videoFormCheck = document.forms['form-video'];

if (videoFormCheck) {
    videoFormCheck.addEventListener('change', () => {
        const uploadButton = document.getElementById('video-submit-button');
        const formElement = [...videoFormCheck.elements].filter((element) => element.type !== 'submit' && !['file', 'video_art'].includes(element.name));
        const formElementValues = formElement.map((element) => element.value);

        // ensure length is greater than intro start and end
        // find all time values
        const ogTiming = ['intro_start', 'intro_end', 'length'].map((timing) => formElement.find((element) => element.name === timing));

        // make all items integers
        const timings = ogTiming.every(Boolean) && ogTiming.length === 3? ogTiming.map((timing) => parseInt(timing.value)): [];

        if (formElementValues.every(Boolean) && timings.length === 3 && timings.every((y) => y >= 0)) {
            const [start, end, length] = timings;

            if (((end > start || (end === start && end === 0)) && ([start, end].every((y) => y < length)))) {
                uploadButton.disabled = false;
            } else {
                uploadButton.disabled = true;
            };
        } else {
            uploadButton.disabled = true;
        };
    });
};


function increaseCounter (value) {    
    /* 
        Change the progress bar on upload
    */
    document.getElementById('progress-per-num').innerText = `${value}%`;
    document.getElementById('progress-level').style.width = `${value}%`;
};


function successfullUpload (response_) {
    /* 
        called when the upload returned a response from the backend
    */
    const response = response_.response;

    if (response.success) {
        // add the returned video_id on the movie/episode form
        document.getElementById('id_video').value = response.video_id;
        document.getElementById('video_id_').innerText = response.video_id;

        // add additional info about the video you uploaded 'if'
        if (response.video_url) {
            document.getElementById('current-video').href = response.video_url;
            const name = response.video_url.match(/\/\w+\.\w+$/g);
            if (name && name.length === 1) {
                const videoName = document.getElementById('video_name_');
                videoName.innerText = name[0].replace('/', '');
                videoName.style.display = 'block';
            };
        };

        // show message that the movie/episode is ready for upload
        document.getElementById('video_id_available').style.display = 'block';

        // disable all elements of the video form
        [...document.forms['form-video'].elements].forEach((element) => element.disabled = true);
    } else {
        // on error with data display errors on the form
        document.getElementById('form-video-error').style.display = 'block';
        const errorMessages = document.getElementById('video-form-errors');

        const errors = Object.keys(response.error).map((key) => {
            const fieldErrors = response.error[key];
            const fieldErrorsLI = fieldErrors.map((error) => `<li>${error}</li>`);
            return `${key}: <ul>${fieldErrorsLI.join('')}</ul>`;
        });

        errorMessages.innerHTML = errors; 
    };
}


// on clicking the video submit button, show the progress bar, and upload the file first
const videoSubmit = document.getElementById('video-submit-button');
const videoSubmitForm = document.getElementById('form-video');
if (videoSubmitForm) {
    videoSubmitForm.addEventListener('submit', function (event) {
        event.preventDefault();
    
        // upload data
        const videoFormData = document.forms['form-video'];
    
        if (videoFormData) {
    
            ajax.post(
                {
                    url: videoFormData.action,
                    form: videoFormData,
                    responseType: 'json',
                    success: successfullUpload,
                    error: function () {
                        document.getElementById('form-video-error').style.display = 'block';
                    },
                    uploadstart: function () {
                        document.getElementById('upload-field').style.visibility = 'visible';
                    },
                    uploadprogress: function (up, total) {
                        increaseCounter(Math.floor((up/total) * 100));
                    },
                    uploadend: function () {
                        document.getElementById('upload-field').style.visibility = 'hidden';
                        document.getElementById('upload-field-done').innerHTML = `<div class='alert alert-success'>Upload done</div>`;
                    }
                }
            );
        };
    })
};