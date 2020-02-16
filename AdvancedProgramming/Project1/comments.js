// Check for the various File API support.
if (window.File && window.FileReader && window.FileList && window.Blob)
{
    // console.log('Great success! All the File APIs are supported.')
} else {
    alert('The File APIs are not fully supported in this browser.');
}

let line_comment = /\/\//;
let multi_comment = /\/\*([A-Za-z ])*\*+\/$/;

function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // Loop through the FileList
    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();

        reader.onload = function(e) {
            let lines = e.target.result.split('\n');
            console.log('total # of lines: ' +  lines.length);
            for(var i = 0; i < lines.length; i++)
            {
                if(line_comment.test(lines[i]))
                {
                    console.log('line comment found!\nline #' + (i + 1) + ': ' + lines[i]);
                }
            }
        };

        reader.readAsText(f);
    }

    // files is a FileList of File objects. List some properties.
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                  f.size, ' bytes, last modified: ',
                  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                  '</li>');
    }
    document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
  }

document.getElementById('files').addEventListener('change', handleFileSelect, false);
