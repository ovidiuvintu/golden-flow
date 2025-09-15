Photo Organizer — Golden Flow

A minimal static web app to group uploaded photos into date-based albums, reorder albums by drag-and-drop, and preview photos in a tile-like grid.

How to use

1. Open `index.html` in a browser (or run a local static server).
2. Click the file picker and select one or more images. Files are grouped by their last-modified date into albums.
3. Click an album to open the photo viewer. Close to return.
4. Drag albums to reorder them on the main page — the order is persisted in localStorage.
5. Use "Clear Data" to remove stored albums and photos.

Notes
- This demo stores image object URLs and metadata in localStorage. It is intended as a local demo and not for long-term storage of many large images.
- For a production app: upload photos to cloud storage, generate thumbnails, and store references/metadata server-side.
