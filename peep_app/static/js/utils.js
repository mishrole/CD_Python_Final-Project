const getLastItem = path => path.substring(path.lastIndexOf('/') + 1);
const getItemByReferenceAndReversePosition = (path, reference, position) =>  {
    let splitPathByReference = path.substring(path.indexOf(reference)).split('/');

    if (splitPathByReference[0] === '') {
        splitPathByReference = splitPathByReference.slice(1);
    }

    if (position < 0 || position > splitPathByReference.length || position.length == 0) {
        return false;
    }

    return splitPathByReference[(splitPathByReference.length - 1) - position]
}