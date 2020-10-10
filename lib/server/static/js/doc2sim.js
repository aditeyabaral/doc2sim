let fList = [];
let fileDialogCache = null;
let sem = 0;

function isEmpty(str){
    return (str == null || str == '');
}

function addToFileList(files){
    for (const f of files){
        const uuid = Date.now().toString(16)
        fList.push(
            {
                _id: uuid,
                filename: f.name,
                file: f,
            }
        );
        const row = $('<div>').addClass('row mt-2');
        // First col
        $('<div>').addClass('col-11').text(f.name).appendTo(row);
        // Second col with button
        $('<i>').addClass('far fa-trash-alt').appendTo(
            $('<button>').addClass('btn btn-danger').attr('data-id', uuid).on('click', removeFile).appendTo(
                $('<div>').addClass('col-1').appendTo(
                    row
                )
            )
        );
        row.appendTo($('#file-list'));
    }
}

function removeFile(e){
    const uuid = $(e.currentTarget).attr('data-id');
    const fIndex = fList.findIndex((i) => i._id === uuid);
    if (fIndex > -1){
        fList.splice(fIndex, 1);
    }
    $(e.currentTarget.parentElement.parentElement).remove();
}

function resultMatrix(simMatrix, filesComp){
    const tbody = $('#resultTable');
    let htmlTemplate = '';
    tbody.html('');
    for (const i of Array(simMatrix.length).keys()){
        htmlTemplate += '<tr>';
        for (const j of Array(simMatrix.length).keys()){
            htmlTemplate += `<td class="text-center">${simMatrix[i][j]}</td>`;
        }
        htmlTemplate += '</tr>';
    }
    tbody.html(htmlTemplate);
}

$(document).ready(function(){
    $('#filename').change(function(e){
        // console.log(e);
        const fname = e.currentTarget.files[0].name;
        $('#lblfilename').text(fname);
        addToFileList(e.currentTarget.files)
    });

   $('#btcheck').click(function(e){
        if (fList.length > 1) {
            sem = 0;
            $('#waitDialog').modal('show');
            const waitDialog = $('#waitDialog');
            const uploadFiles = new FormData();
            for (const f of fList) {
                uploadFiles.append('files_up', f.file, f.name);
            }
            $.ajax({
                url: ajax.fileUpload.url,
                type: 'POST',
                dataType: 'json',
                processData: false,
                cache: false,
                contentType: false,
                data: uploadFiles,
                complete: function(){
                }
            }).done(function(data){
                // Get similarity matrix
                resultMatrix(data.sim_matrix, data.filenames);
            }).fail(function(){
                // console.log('AJAX request faill!!!');
                sem = 1;
            }).always(function(){
                sem = 1;
                $('#waitDialog').modal('hide');
            });
        }
        else {
            $('#errorDialogText').html('Add more than one file to compare!!');
            $('#errorDialog').modal('show');
        }
   });

   $('#waitDialog').on('shown.bs.modal', function(e){
       if (sem === 1){
           $('#waitDialog').modal('hide');
       }
   });
});