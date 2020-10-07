let fList = [];
let fileDialogCache = null

function isEmpty(str){
    return (str == null || str == '');
}

function removeFile(e){
    const uuid = $(e.currentTarget).attr('data-id');
    const fIndex = fList.findIndex((i) => i._id === uuid);
    if (fIndex > -1){
        fList.splice(fIndex, 1);
    }
    $(e.currentTarget.parentElement.parentElement).remove();
}

function pathClick(e){
    e.preventDefault();
    const uuid = $(e.currentTarget).attr('data-id');
    const fIndex = fileDialogCache.findIndex((i) => i.uuid === uuid);
    if (fIndex > -1){
        const fItem = fileDialogCache[fIndex];
        if (fItem.is_folder) {
            config.localPath = fItem.absolute_path;
            getFileList();
        }
        else {
            $('#filename').val(fItem.absolute_path);
            $('#file-dialog').modal('hide');
        }
    }
}

function getFileList(folderAction){
    $.ajax({
        url: config.fileBrowserURL,
        type: 'POST',
        dataType: 'json',
        data: {
            filepath: config.localPath,
            folderaction: folderAction || '',
        },
        success: function(response){
            if (response.data){
                const tbody = $('#table-path');
                fileDialogCache = response.data;
                config.localPath = response.current_folder;
                tbody.html('');
                $('#dialog-title').text(config.localPath);
                for (const f of fileDialogCache) {
                    const tr = $('<tr>');
                    const td = $('<td>');
                    if (f.is_folder) {
                        $('<i>').addClass('fas fa-folder').appendTo(
                            $('<span>').addClass('text-warning').appendTo(
                                td
                            )
                        );
                    }
                    $('<a>')
                        .attr('href', '#')
                        .attr('data-id', f.uuid)
                        .text(f.name)
                        .on('click', pathClick)
                        .appendTo(td);
                    td.appendTo(tr);
                    tr.appendTo(tbody);
                }
            }
        }
    });
}

$(document).ready(function(){
    $('#btfileadd').click(function(e){
        const fname = $('#filename').val();
        if (!isEmpty(fname)) {
            const uuid = Date.now().toString(16);
            fList.push(
                {
                    _id: uuid,
                    filename: fname
                }
            );
            const row = $('<div>').addClass('row mt-2');
            // First col
            $('<div>').addClass('col-11').text(fname).appendTo(row);
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
   });

   $('#btfilebrowse').click(function(e){
       $('#file-dialog').modal('show');
       if (fileDialogCache === null){
           getFileList();
       }
   });

   $('#btfolderup').click(function(e){
        e.preventDefault();
        getFileList('up');
   });

   $('#sim-form').submit(function(e){
       $('#filelist').val(JSON.stringify(fList));
   });
});