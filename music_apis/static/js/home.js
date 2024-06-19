$(document).ready(function() {
    
    // Function to fetch and display playlists
    function fetchPlaylists() {
        const resultTbody = $('#result');

        // Fetch data from the API
        fetch('http://localhost:8000/api/playlists/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Process the data and update the DOM
                let resultHtml = '';
                data.forEach(playlist => {
                    // debugger;
                    resultHtml += `
                        <tr>
                            <td class="playlist-name" onclick="openPlaylist(${playlist.id})">
                        ${playlist.name}
                        <ul>
                            ${playlist.tracks.map(trackInfo => `<li>Order: ${trackInfo.order} - ${trackInfo.track_name}</li>`).join('')}
                        </ul>    
                    </td>

                    <td><a href="#" class="edit-btn"data-id="${playlist.id}"><i class="bi bi-pencil-square"></i></a></td>
                    <td><a href="#" class="delete-btn" data-id="${playlist.id}"><i class="bi bi-trash"></i></a></td>
                    </tr>
                    `;
                });
                resultTbody.html(resultHtml);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                resultTbody.html('<tr><td colspan="3">Error fetching data</td></tr>');
            });
    }

    // Initial fetch and display of playlists
    fetchPlaylists();
    

    // Edit functionality
    $(document).on('click', '.edit-btn', function() {
        var row = $(this).closest('tr');
        var playlistId = $(this).data('id');
        var playlistNameElement = row.find('.playlist-name');
        var playlistName = playlistNameElement.text();
        debugger;
        
        var newName = prompt("Edit Playlist Name", playlistName);
        
        if (newName !== null) {
            // Update the playlist name on the frontend
            playlistNameElement.text(newName);
            // debugger;

            // AJAX call to update the playlist name on the server
            var playlistId = $(this).data('id');  
            // Assuming you have a data attribute for playlist ID
            $.ajax({
                url: '/api/playlists/' + playlistId + '/',  // Replace with your actual server endpoint URL
                method: 'PUT',  // Use POST or PUT based on your server's API
                data: {
                    playlistId: playlistId,
                    newName: newName
                },
                success: function(response) {
                    // Handle success, if needed
                    console.log('Playlist name updated successfully.');
                },
                error: function(xhr, status, error) {
                    // Handle error
                    console.error('Error updating playlist name:', error);
                    // You can revert the playlist name on error, if required
                    playlistNameElement.text(playlistName);
                }
            });
        }
    });
    

    // Delete functionality
    $(document).on('click', '.delete-btn', function(event) {
        event.preventDefault();
        debugger;
        var playlistId = $(this).data('id');
        // var confirmation = confirm("Are you sure you want to delete this playlist?");

        // if (confirmation) {
            $.ajax({
                url: '/api/playlists/' + playlistId + '/',  // Replace <playlist_id> with actual playlist ID
                type: 'DELETE',
                success: function(result) {
                    // Handle success
                    console.log('Playlist deleted successfully');
                },
                error: function(xhr, status, error) {
                    // Handle error
                    console.error('Error deleting playlist:', error);
                }
            });

            
            
        // }
    });
    $(document).on('click', '#track', function(event){
        $.ajax({
            url: '/api/tracks/',
            type: "GET",
            dataType: "json",
            success: function(response) {
                debugger;
                console.log("API Response:", response);
    
                $.each(response, function(index, track) {
                    $('#track_data').append('<option>' + track.name + '</option>');
                });
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    })
    $(document).on('click', '.playlist_save', function(event){
        debugger;
        $.ajax({
            url: '/api/playlists/',
            type: "post",
            dataType: "json",
            success: function(response) {
                debugger;
                console.log("API Response:", response);
    
                
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    })

});
