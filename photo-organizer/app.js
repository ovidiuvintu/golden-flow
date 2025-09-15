const fileInput = document.getElementById('file-input');
const albumsEl = document.getElementById('albums');
const viewer = document.getElementById('viewer');
const albumTitle = document.getElementById('album-title');
const photoGrid = document.getElementById('photo-grid');
const closeViewer = document.getElementById('close-viewer');
const clearBtn = document.getElementById('clear-storage');

const STORAGE_KEY = 'photo-organizer:v1';

let state = {
  albums: [] // {id, dateLabel, photos: [{id, url, name, ts}]}
};

// Utilities
const uid = () => Math.random().toString(36).slice(2,9);

function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function load() { try { const raw = localStorage.getItem(STORAGE_KEY); if(raw) state = JSON.parse(raw); } catch(e){console.error(e)} }

function formatDateLabel(ts){
  const d = new Date(ts);
  return d.toLocaleDateString();
}

// Group files by date (date only)
async function handleFiles(files){
  const fileArray = Array.from(files);
  for(const f of fileArray){
    const arrayBuffer = await f.arrayBuffer();
    const blob = new Blob([arrayBuffer], {type: f.type});
    const url = URL.createObjectURL(blob);
    // Use lastModified if available, else now
    const ts = f.lastModified || Date.now();
    const dateKey = new Date(ts).toDateString();
    let album = state.albums.find(a=>a.dateKey===dateKey);
    if(!album){
      album = { id: uid(), dateKey, dateLabel: formatDateLabel(ts), photos: [] };
      state.albums.push(album);
    }
    album.photos.unshift({ id: uid(), url, name: f.name, ts });
  }
  save();
  renderAlbums();
}

function renderAlbums(){
  albumsEl.innerHTML = '';
  if(state.albums.length===0){
    const empty = document.createElement('div'); empty.className='empty'; empty.textContent='No photos yet — add some using the file picker.'; albumsEl.appendChild(empty);
    return;
  }
  state.albums.forEach(album=>{
    const el = document.createElement('article'); el.className='album'; el.draggable=true; el.dataset.id=album.id;

    const header = document.createElement('div'); header.className='album-header';
    const title = document.createElement('div'); title.className='album-title'; title.textContent = album.dateLabel;
    const count = document.createElement('div'); count.className='album-count'; count.textContent = `${album.photos.length}`;
    header.appendChild(title); header.appendChild(count);

    const preview = document.createElement('div'); preview.className='album-preview';
    album.photos.slice(0,6).forEach(p=>{
      const img = document.createElement('img'); img.src = p.url; img.alt = p.name; preview.appendChild(img);
    });

    el.appendChild(header); el.appendChild(preview);

    el.addEventListener('click', ()=> openAlbum(album.id));

    // Drag events
    el.addEventListener('dragstart', (e)=>{
      el.classList.add('dragging'); e.dataTransfer.setData('text/plain', album.id);
      e.dataTransfer.effectAllowed = 'move';
    });
    el.addEventListener('dragend', ()=> el.classList.remove('dragging'));

    el.addEventListener('dragover', (e)=>{
      e.preventDefault(); e.dataTransfer.dropEffect='move';
    });

    el.addEventListener('drop', (e)=>{
      e.preventDefault(); const draggedId = e.dataTransfer.getData('text/plain'); reorderAlbums(draggedId, album.id);
    });

    albumsEl.appendChild(el);
  });
}

function reorderAlbums(draggedId, targetId){
  if(draggedId===targetId) return;
  const fromIdx = state.albums.findIndex(a=>a.id===draggedId);
  const toIdx = state.albums.findIndex(a=>a.id===targetId);
  if(fromIdx<0||toIdx<0) return;
  const [item] = state.albums.splice(fromIdx,1);
  state.albums.splice(toIdx,0,item);
  save(); renderAlbums();
}

function openAlbum(id){
  const album = state.albums.find(a=>a.id===id); if(!album) return;
  albumTitle.textContent = `${album.dateLabel} — ${album.photos.length} photos`;
  photoGrid.innerHTML='';
  album.photos.forEach(p=>{ const img = document.createElement('img'); img.src=p.url; img.alt=p.name; photoGrid.appendChild(img); });
  viewer.hidden=false;
}

closeViewer.addEventListener('click', ()=>{ viewer.hidden=true; });

fileInput.addEventListener('change', (e)=> handleFiles(e.target.files).then(()=> fileInput.value=''));
clearBtn.addEventListener('click', ()=>{ if(confirm('Clear saved photos and albums?')){ state={albums:[]}; localStorage.removeItem(STORAGE_KEY); renderAlbums(); }});

// Init
load(); renderAlbums();

// Basic cleanup: revoke object URLs on unload
window.addEventListener('unload', ()=>{
  state.albums.forEach(a=>a.photos.forEach(p=>{ try{ URL.revokeObjectURL(p.url);}catch(e){} }));
});
