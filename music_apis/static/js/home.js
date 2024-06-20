$(document).ready(function () {
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
                    resultHtml += `
                        <tr>
                            <td class="playlist-name" onclick="openPlaylist(${playlist.id})">
                                ${playlist.name}
                                <ul>
                                    ${playlist.tracks.map(trackInfo => `<li>Order: ${trackInfo.order} - ${trackInfo.track_name}</li>`).join('')}
                                </ul>    
                            </td>
                            <td><a href="#" class="edit-btn" data-id="${playlist.id}"><i class="bi bi-pencil-square"></i></a></td>
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


// Edit functionality for opening popup
$(document).on('click', '.edit-btn', function () {
    var playlistId = $(this).data('id');

    // Fetch playlist details via AJAX
    $.ajax({
        url: '/api/playlists/' + playlistId + '/',  // Replace with your actual server endpoint URL
        type: 'GET',
        success: function (playlist) {
            // Populate modal fields with playlist data
            $('#editPlaylistId').val(playlist.id);
            $('#editPlaylistNameInput').val(playlist.name);

            // Fetch tracks data and populate the edit modal
            $.ajax({
                url: '/api/tracks/',  // Replace with your actual server endpoint URL for tracks
                type: "GET",
                dataType: "json",
                success: function (tracks) {
                    var editTrackOrderList = $('#editTrackOrderList');
                    editTrackOrderList.empty();

                    // Process each trackInfo from playlist.tracks
                    playlist.tracks.forEach(trackInfo => {
                        var trackOrderItem = `
                            <div class="trackOrderItem">
                                <div class="form-group">
                                    <label for="editTrackSelect">Track</label>
                                    <select class="form-control editTrackSelect" name="track">
                                        ${tracks.map(track => `
                                            <option value="${track.id}" ${track.id == trackInfo.track ? 'selected' : ''}>${track.name}</option>
                                        `).join('')}
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="editOrderInput">Order</label>
                                    <input type="number" class="form-control editOrderInput" name="order" value="${trackInfo.order}">
                                </div>
                            </div>
                        `;
                        editTrackOrderList.append(trackOrderItem);
                    });
                    fetchPlaylists(); 
                },
                error: function (xhr, status, error) {
                    console.error("Error fetching tracks:", error);
                }
            });

            // Open the edit playlist modal
            $('#editPlaylistModal').modal('show');
        },
        error: function (xhr, status, error) {
            console.error('Error fetching playlist details:', error);
        }
    });
});


    // Save changes to playlist in edit
    $(document).on('click', '.saveEditPlaylist', function () {
        var playlistId = $('#editPlaylistId').val();
        var newName = $('#editPlaylistNameInput').val();

        // Prepare updated playlist data
        var updatedPlaylistData = {
            name: newName,
            tracks: []
        };

        $('.trackOrderItem').each(function () {
            var trackId = $(this).find('.editTrackSelect').val();
            var order = $(this).find('.editOrderInput').val();
            if (trackId && order) {
                updatedPlaylistData.tracks.push({
                    track: trackId,
                    order: order
                });
            }
        });

        // Send updated playlist data via AJAX PUT request
        $.ajax({
            url: '/api/playlists/' + playlistId + '/',  // Replace with your actual server endpoint URL
            type: 'PUT',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
            },
            data: JSON.stringify(updatedPlaylistData),
            success: function (response) {
                $('#editPlaylistModal').modal('hide');  // Hide the modal after successful update
                location.reload();  // Refresh the window
                fetchPlaylists();  // Refresh the playlist display
            },
            error: function (xhr, status, error) {
                console.error('Error updating playlist:', error);
                // Handle error scenario (e.g., show an alert)
            }
        });
    });

    $(document).ready(function () {

        // Function to add track order fields dynamically
        $(document).on('click', '.addEditTrackOrderButton', function () {
            var newTrackOrderItem = `
                <div class="trackOrderItem">
                    <div class="form-group">
                        <label for="editTrackSelect">Track</label>
                        <select class="form-control editTrackSelect" name="track">
                            <!-- Options will be populated dynamically -->
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="editOrderInput">Order</label>
                        <input type="number" class="form-control editOrderInput" name="order" placeholder="Enter order number">
                    </div>
                </div>
            `;
            $('#editTrackOrderList').append(newTrackOrderItem);
    
            // Fetch tracks and populate the select element
            $.ajax({
                url: '/api/tracks/',  // Replace with your actual server endpoint URL for tracks
                type: "GET",
                dataType: "json",
                success: function (response) {
                    var editTrackSelect = $('.editTrackSelect').last();  // Select the last added track select
                    editTrackSelect.empty();  // Clear existing options
                    response.forEach(track => {
                        editTrackSelect.append(`<option value="${track.id}">${track.name}</option>`);
                    });
                },
                error: function (xhr, status, error) {
                    console.error("Error fetching tracks:", error);
                }
            });
        });
    
        // Other existing JavaScript code goes here...
    
    });

    // Delete functionality
    $(document).on('click', '.delete-btn', function (event) {
        event.preventDefault();
        var playlistId = $(this).data('id');

        $.ajax({
            url: '/api/playlists/' + playlistId + '/',  // Replace <playlist_id> with actual playlist ID
            type: 'DELETE',
            headers: {
                "X-CSRFToken": getCookie('csrftoken')   // Include CSRF token in headers
            },
            success: function (result) {
                fetchPlaylists();  // Refresh the playlist display
            },
            error: function (xhr, status, error) {
                console.error('Error deleting playlist:', error);
            }
        });
    });

    // Fetch tracks and populate the select element when modal opens
    $(document).on('click', '#track', function () {
        $.ajax({
            url: '/api/tracks/',
            type: "GET",
            dataType: "json",
            success: function (response) {
                var trackSelect = $('#track_data');
                trackSelect.empty();  // Clear existing options
                $.each(response, function (index, track) {
                    trackSelect.append('<option value="' + track.id + '">' + track.name + '</option>');
                });
            },
            error: function (xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    });

    // Save playlist with tracks
    $('.playlist_save').click(function () {
        var playlistData = {
            name: $('.playlistNameInput').val(),
            tracks: []
        };

        $('.trackOrderItem').each(function () {
            var track = {
                track: $(this).find('.trackSelect').val(), // Use 'track' instead of 'track_id'
                order: $(this).find('.orderInput').val()
            };
            playlistData.tracks.push(track);
        });

        $.ajax({
            url: '/api/playlists/',
            type: "POST",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')   // Include CSRF token in headers
            },
            contentType: "application/json",
            data: JSON.stringify(playlistData),
            success: function (response) {
                playlistData = [];
                console.log("API Response:", response);
                fetchPlaylists();  // Refresh the playlist display
                $('#exampleModal').modal('hide');  // Hide the modal
            },
            error: function (xhr, status, error) {
                console.error("Error saving playlist:", error);
            }
        });
    });

    // Add new track order input fields
    $(document).on('click', '.addTrackOrderButton', function () {
        var newTrackOrderItem = `
            <div class="trackOrderItem">
                <div class="form-group">
                    <label for="trackSelect">Track</label>
                    <select class="form-control trackSelect" name="track">
                        ${$('#track_data').html()} <!-- Copy options from the existing track select -->
                    </select>
                </div>
                <div class="form-group">
                    <label for="orderInput">Order</label>
                    <input type="number" class="form-control orderInput" name="order" placeholder="Enter order number">
                </div>
            </div>
        `;
        $('#trackOrderList').append(newTrackOrderItem);
    });

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}