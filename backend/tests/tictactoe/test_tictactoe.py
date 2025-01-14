from src.psi_backend.tictactoe.game import check_winner


class TestCheckWinner:
    def test_check_winner_horizontal(self):
        board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
        assert check_winner(board) == (True, "X")

    def test_check_winner_vertical(self):
        board = [["O", "", ""], ["O", "", ""], ["O", "", ""]]
        assert check_winner(board) == (True, "O")

    def test_check_winner_diagonal(self):
        board = [["X", "", ""], ["", "X", ""], ["", "", "X"]]
        assert check_winner(board) == (True, "X")

    def test_check_winner_anti_diagonal(self):
        board = [["", "", "O"], ["", "O", ""], ["O", "", ""]]
        assert check_winner(board) == (True, "O")

    def test_check_winner_no_winner(self):
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        assert check_winner(board) == (True, None)

    def test_check_winner_game_not_over(self):
        board = [["X", "", "O"], ["", "", ""], ["", "", ""]]
        assert check_winner(board) == (False, None)
