var isExist = ClipMenu.require('fhconvert');
if (!isExist) {
    throw new Error('Cound not find the library');
}

var lines = clipText.split('\n');

for (var i = 0; i < lines.length; i++) {
    lines[i] = FHConvert.kktohg(lines[i]);
}

return lines.join('\n');

