var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

eel.expose(load_lists);
function load_lists(data){

    /*
        This function calls the python backend in order to get the publishers, platforms
        and genres applicable to the videogames from the dataset.
    */
    data.publishers.sort((a, b) => {
        let fa = a.toLowerCase(),
            fb = b.toLowerCase();
    
        if (fa < fb) {
            return -1;
        }
        if (fa > fb) {
            return 1;
        }
        return 0;
    });
    Publisher.innerHTML += '<option selected value=""> Choose a publisher</option>';
    data.publishers.forEach((publisher) => {

        Publisher.innerHTML += `<option value="${publisher}"> ${publisher} </option>`;
        
    });

    data.platforms.sort((a, b) => {
        let fa = a.toLowerCase(),
            fb = b.toLowerCase();
    
        if (fa < fb) {
            return -1;
        }
        if (fa > fb) {
            return 1;
        }
        return 0;
    });
    Platform.innerHTML += '<option selected value=""> Choose a platform</option>';
    data.platforms.forEach((platform) => {

        Platform.innerHTML += `<option value="${platform}"> ${platform} </option>`;
        
    });
    
    data.genres.sort((a, b) => {
        let fa = a.toLowerCase(),
            fb = b.toLowerCase();
    
        if (fa < fb) {
            return -1;
        }
        if (fa > fb) {
            return 1;
        }
        return 0;
    });
    Genre.innerHTML += '<option selected value=""> Choose a genre</option>';
    data.genres.forEach((genre) => {

        Genre.innerHTML += `<option value="${genre}"> ${genre} </option>`;
        
    });

    data.ratings.sort((a, b) => {
        let fa = a.toLowerCase(),
            fb = b.toLowerCase();
    
        if (fa < fb) {
            return -1;
        }
        if (fa > fb) {
            return 1;
        }
        return 0;
    });
    Rating.innerHTML += '<option selected value=""> Choose a rating</option>';
    data.ratings.forEach((rating) => {

        Rating.innerHTML += `<option value="${rating}"> ${rating} </option>`;
        
    });

}

eel.expose(display_prediction)
function display_prediction(data_){

    info_modal_ = new bootstrap.Modal(info_modal, {
        keyboard: false
      });

    if (data_.message === 'success'){
        
        let prediction = data_.prediction;
        let resulting_label = translate_label(prediction.label);
        let labels = data_.possibilities;

        info_msg.innerHTML =`<p>Your game has <b>${prediction.value.toFixed(2)*100}%</b> chance of being :</p>`;
        info_msg.innerHTML += '<ul class="list-group">';
        
        labels.forEach((label) =>{
            
            translated_label = translate_label(label);

            if(translated_label == resulting_label){
                info_msg.innerHTML += `<li class="list-group-item active" aria-current="true">${translated_label}</li>
                `;
            }else{
                info_msg.innerHTML += `<li class="list-group-item">${translated_label}</li>
                `;
            }
    
        });
        
        info_msg.innerHTML += '</ul>';

        info_img.innerHTML = "<img class='rounded mx-auto d-block' src='media/success.gif'>";
    }
    else if (data_.message === 'error'){
        info_msg.innerHTML = data_.error;
        info_img.innerHTML = "<img class='rounded mx-auto d-block' src='media/error.gif'>";
    }
    info_modal_.show();

    submit_button.classList.remove('loading_button');
    submit_button.innerHTML = "<h4><b> Submit </b></h4>";
    submit_button.disabled = false;

}

function translate_label(label){

    let translated = '';

    if (label == 'Aceptable'){
        translated = 'Acceptable';
    }
    else if (label == 'Bueno'){            
        translated = 'Good';
    }
    else if (label == 'Excelente'){
        translated = 'Excellent';
    }
    else if (label == 'Malo'){
        translated = 'Bad';
    }

    return translated;

}

eel.load_unique_field_values();

submit_button.addEventListener('click', function(){

    submit_button.disabled = true;
    submit_button.innerHTML = "";
    submit_button.classList.add('loading_button');

    let platform;
    let genre;
    let publisher;
    let na_sales;
    let eu_sales;
    let jp_sales;
    let other_sales;
    let rating;

    platform = Platform[Platform.selectedIndex].value;
    genre = Genre[Genre.selectedIndex].value;
    publisher = Publisher[Publisher.selectedIndex].value;
    na_sales = NA_Sales.value;
    eu_sales = EU_Sales.value;
    jp_sales = JP_Sales.value;
    other_sales = Other_Sales.value;
    rating = Rating[Rating.selectedIndex].value;

    eel.get_prediction(
        platform, genre, publisher,
        na_sales, eu_sales, jp_sales, other_sales,
        rating
    );

    
});