var video = document.getElementById('player');
var source = document.getElementById('player_source');

const lib_item_template = document.getElementById("libraryitem");
const lib = document.getElementById("library");

loadLibrary()
function loadLibrary()
{
    fetch('{{ media_host }}/api/media/list')
        .then(res => res.json())
        .then((out) => {
            for(var i = 0; i < out.length; i++)
            {
                const clone = lib_item_template.content.cloneNode(true);
                clone.querySelectorAll("img")[0].setAttribute("id", out[i]);
                clone.querySelectorAll("img")[0].src = '{{ thumb_host }}/api/thumb/' + out[i];
                clone.querySelector("a").addEventListener("click", play);
                lib.appendChild(clone);
            }
        })
        .catch(err => console.error(err));
}
function play(event)
{
    id = event.target.id;
    video.pause();
    source.setAttribute('src', '{{ media_host }}/api/media/' + id);
    source.setAttribute('type', 'video/webm');
    video.load();
    video.play();
    meta(id);
}
function meta(id)
{
    fetch('{{ meta_host }}/api/meta/' + id)
        .then(res => res.json())
        .then((out) => {
            console.log('Output: ', out);
        })
        .catch(err => console.error(err));
}