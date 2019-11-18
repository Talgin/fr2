
$(document).ready(function(){
    //Read mode for hide second column
    $('.toggle-first').click(function () {
     if ($('.first-column').css('display')==='block'){
         $('.first-column').css({"display":"none"});
         $('.second-column').removeClass('col-md-8 col-lg-8');
     } else {
         $('.first-column').css({"display":"block"});
         $('.second-column').addClass('col-md-8 col-lg-8');
     }
});

    //File upload by itself without button
    $('#id_document').change(function() {
        $('#download_file_to_server').submit();
    });

    $('#analyze_id').click(function () {
        var t = $('.text-area').html();
        $('#html_div').val(t);
    });
    $('#save-button-id').click(function () {
        var t = $('.text-area').html();
        $('#html_div_save').val(t);
        // Take all count_ids which were founded a model or user chose
        var tt = $('.check-count-id').map(function () {
            return this.id
        }).get();
        $('#html_div_save_count_id').val(tt);

        var ttt = $('.check-count-color').toArray();
        var a = [];
        for (var i = 0; i<ttt.length; i++){
            a.push(ttt[i].innerHTML)
        }
        $('#html_div_save_count_color').val(a);


    });

    $('.text-area').each(function () {
        this.contentEditable =true;
    });


});