from src.psi_backend.tictactoe.game import check_winner


class TestCheckWinner:
    def test_check_winner_horizontal(self):
        board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
        assert check_winner(board) == "X"

    def test_check_winner_vertical(self):
        board = [["O", "", ""], ["O", "", ""], ["O", "", ""]]
        assert check_winner(board) == "O"

    def test_check_winner_diagonal(self):
        board = [["X", "", ""], ["", "X", ""], ["", "", "X"]]
        assert check_winner(board) == "X"

    def test_check_winner_anti_diagonal(self):
        board = [["", "", "O"], ["", "O", ""], ["O", "", ""]]
        assert check_winner(board) == "O"

    def test_check_winner_no_winner(self):
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        assert check_winner(board) is None
