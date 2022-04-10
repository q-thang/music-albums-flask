/** Load the list of albums */
async function listAlbums() {
  // TODO make an AJAX request to /albums
  // then populate the "albums_list" list with the results
  const response = await fetch("http://127.0.0.1:5000/albums", {
    method: "GET",
    mode: "cors",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const albumEl = document.getElementById("albums_list");

  response.json().then(
    (data) =>
      (albumEl.innerHTML = data
        .map((album) => {
          return `
        <li class="album" onclick="showAlbum(${album.album_id})">
          <h3 class="title">${album.album_id}. ${album.album_artist} - ${album.album_title}</h3>
        </li>
        `;
        })
        .join(""))
  );
}

/** Show details of a given album */
async function showAlbum(album_id) {
  // TODO make an AJAX request to /albuminfo with the selected album_id as parameter (i.e., /albuminfo?album_id=xxx),
  // then show the album cover in the "album_cover" div and display the tracks in a table inside the "album_songs" div
  const response = await fetch(
    `http://127.0.0.1:5000/albuminfo?album_id=${album_id}`,
    {
      method: "GET",
      mode: "cors",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  const albumCover = document.getElementById("album_cover");
  const albumSongs = document.getElementById("album_songs");

  response.json().then(async (data) => {
    await fetch(`http://127.0.0.1:5000/images/${data.album_image}`)
      .then((res) => res.blob())
      .then((imageBlob) => {
        const imageObjectURL = URL.createObjectURL(imageBlob);

        albumCover.innerHTML = `<img src=${imageObjectURL} alt="Album Cover" />`;
      });
    albumSongs.innerHTML = `
    <table>
          <tr>
            <th>No.</th>
            <th>Title</th>
            <th>Length</th>
          </tr>
          ${data.album_tracks
            .map((el) => {
              return `<tr>
            <td class="song_no">${el.track_id}.</td>
            <td class="song_title">${el.track_title}</td>
            <td class="song_length">${el.track_length}</td>
          </tr>`;
            })
            .join("")}
          <tr>
            <td colspan="2"><strong>Total length:</strong></td>
            <td class="song_length"><strong>${data.album_length}</strong></td>
          </tr>
        </table>`;
  });
}
