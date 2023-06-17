$(document).ready(function(){


    function readURL(input) {
        if (input.files && input.files[0]) {
            for(var i =0; i <= input.files.length; i++) {
                var reader = new FileReader();
                // var id = 'imagePreview'.concat(String(i));
                // var next_div = $("<div></div>").attr('id', id);
                // $('#img-preview').append(next_div);
                // var img = $("<img>").attr({"height":"300", "width": "400", "id": "image".concat(String(i))});
                // $('#imagePreview'.concat(String(i))).append(img);
                reader.onload = function (e) {
                    // $('div.img-preview div:last-child').css('background-image', 'url(' + e.target.result + ')');
                    // $('div.img-preview div:last-child').hide();
                    // $('div.img-preview div:last-child').fadeIn(650);
                    var img = "<div class='container my-2'><img src='" + this.result + "' width='400' height='300'></div>";
                    $('#img-preview').append(img);
                };
                reader.readAsDataURL(input.files[i]);
            }
        }
    }

    $("#imageUpload").change(function () {
        // $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });


    $('#oct-pred').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        //$(this).hide();
        //$('.loader').show();
        //$('#btn-predict').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/OCT_pre',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // var item = data.split(';');
                // Get and display the result
                //$('.loader').hide();
                //$('#result').fadeIn(600);
                console.log(data)
                    
                    $('#pre').append(" <div>"+data+"</div>");
                    console.log('Success!');
                
                
            },
        });
    });



    $('#chest-pred').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        //$(this).hide();
        //$('.loader').show();
        //$('#btn-predict').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/chest_pre',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // var item = data.split(';');
                // Get and display the result
                //$('.loader').hide();
                //$('#result').fadeIn(600);
                console.log(data)
                    
                    $('#pre').append(" <div>"+data+"</div>");
                    console.log('Success!');
                
                
            },
        });
    });
    
    document.querySelector('#scrollButton').addEventListener('click', function() {
        window.scrollBy(0, document.body.scrollHeight);
    });










    
})