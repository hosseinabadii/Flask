function editNote(note_id) {
    var editUrl = "/edit-note/" + note_id;
    window.location.href = editUrl;
}


function deleteNote(note_id) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ note_id: note_id}),
    }).then((_res) => {
        window.location.href = "/all-notes";
    });
}