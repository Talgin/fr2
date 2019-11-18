 $(function() {

    var pathname = window.location.pathname;
    var res = pathname.split("/");
    var currentPage = res[2];
    $('#current_page_id').text(currentPage);

    if (currentPage == '1') {
      var newUrl = '/main_page/' + '1'
      $('#previous_page_id').attr('href', newUrl);
      var newUrl = '/main_page/' + '2'
      $('#next_page_id').attr('href', newUrl);



      $('#table').bootstrapTable({
          autoRefreshInterval: 1,
          autoRefreshSilent: true
       });
       $(".fixed-table-toolbar").append("<div id='loading_status_icon' class='clearfix'style='padding-top:11px;'><div class='spinner-border text-warning float-right' role='status' style='color: #D93D04!important;'><span class='sr-only'>Loading...</span></div></div>");
    }
    else {
      $('#table').bootstrapTable({
          autoRefresh: false,
          autoRefreshStatus: false,
          autoRefreshSilent: true
       });
      var currentPagePrevious = (parseInt(currentPage, 10) - 1).toString();
      var currentPageNext = (parseInt(currentPage, 10) + 1).toString();
      var newUrlPrevious = '/main_page/' + currentPagePrevious;
      var newUrlNext = '/main_page/' + currentPageNext;
      $('#previous_page_id').attr('href', newUrlPrevious);
      $('#next_page_id').attr('href', newUrlNext);
    }

    $( '#table' ).on( 'click', 'tr', function () {
       var unique_image_id = $(this).children('td').children('img').attr('id');
       location.href = "/main_page/detail_view/" + unique_image_id
    });


    $('.auto-refresh').click(function () {
      var className = $(this).attr('class');
      if(className == 'auto-refresh btn btn-secondary active'){
        $(".fixed-table-toolbar").append("<div id='loading_status_icon' class='clearfix'style='padding-top:11px;'><div class='spinner-border text-warning float-right' role='status' style='color: #D93D04!important;'><span class='sr-only'>Loading...</span></div></div>");
      } else{
        $('#loading_status_icon').remove();
      };
    });
  });
