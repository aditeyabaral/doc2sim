let fList = [];

function isEmpty(str){
    return (str == null || str == '');
}

$(document).ready(function(){
    $('#btfileadd').click(function(e){
        const fname = $('#filename').val();
        if (!isEmpty(fname)) {
            const divList = $('#file-list');
            $(`<div class="row mt-2">
                <div class="col-11">${fname}</div>
                <div class="col-1">
                    <button type="button" class="btn btn-danger">
                        <i class="far fa-trash-alt"></i>
                    </button>
                </div>
            </div>`).appendTo(divList);
            fList.push(fname);
        }
   });

   $('#sim-form').submit(function(e){
       $('#filelist').val(JSON.stringify(fList));
   });
});