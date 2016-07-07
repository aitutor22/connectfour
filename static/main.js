$(document).ready(function() {

	var numberGridsFilled = [0, 0, 0, 0, 0, 0, 0];
	var playerOne = true;
	var board = '';

	function getMark(playerOne) {
		return playerOne ? 'X' : 'O';
	};

	function makeMove(row, col, playerOne) {
		$('.red').removeClass('red');
		$('#' + row + '-' + col).addClass('red');
		$('#' + row + '-' + col)[0].innerText = getMark(playerOne);		
	}

	$('.top').click(function(evt) {
		//only for human player
		if (!playerOne) {
			alert('AI is still thinking.');
			return false;
		}

		var colSelected = parseInt(evt.currentTarget.id.split('-')[1]);
		if (numberGridsFilled[colSelected] == 6) {
			alert('Column is already full. Please select another column');
			return false;
		};
		var currentRow = 6 - numberGridsFilled[colSelected] - 1;
		makeMove(currentRow, colSelected, playerOne);
		playerOne = !playerOne;
		numberGridsFilled[colSelected]++;

		//kiv - need to check if victory

		//now for ai move
		getAIMove(colSelected, board, function(data){
			//player two hasn't put board yet
			if (data['status'] != 'ongoing' && data['last_move'] == 'player_two') {
				makeMove(data['row'], data['col'], playerOne);
			};

			if (data['status'] == 'win') {
				if (data['last_move'] == 'player_one') {
					alert('Player one wins');
				}
				else {
					alert('Player two wins');
				};
			}

			else if (data['status'] == 'draw') {
				alert('Drawn game');
			}

			else {
				makeMove(data['row'], data['col'], playerOne);
				board = data['board'];
				playerOne = !playerOne;
				numberGridsFilled[data['col']]++;
			}
		});
	});

	function getAIMove(col, board, success) {
		$.ajax({
			type: 'POST',
			url: '/move',
			data: {
				col: col,
				board: board
			},
			success: success
		});
	};
});