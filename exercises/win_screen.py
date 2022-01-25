class WinScreen:

    def __init__(self):
        # two text for winand lose
        self.text_a = "You Won :)"
        self.text_b = "You Lost :"

    def detect_win(self, player_coord, runner_coord, ai_coord):
        # if the player catches the runner he/she won
        if player_coord == runner_coord:
            print(self.text_a)
        # if the ai catches the player he/she lost
        if player_coord == ai_coord:
            print(self.text_b)
        # if the ai catches the runner the player lost
        if runner_coord == ai_coord:
            print(self.text_b)
