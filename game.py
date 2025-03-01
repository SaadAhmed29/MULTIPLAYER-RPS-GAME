class Game:
    def __init__(self,id):
        self.p1Went=False
        self.p2Went=False
        self.ready=False
        self.id=id
        self.moves=[None,None]
        self.wins=[0,0]
        self.ties=0


    def get_player_move(self,p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]


    def play(self,player,move):
        self.moves[player]=move
        if player==0:
            self.p1Went=True
        else:
            self.p2Went=True


    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1=self.moves[0].upper()[0]  #takes first letter of move i.e, R for rock, S for scissors
        p2=self.moves[1].upper()[0]

        winner=-1  #if tie

        if p1 == p2:
            winner = -1
        elif p1+p2 in ('PR', 'RS', 'SP'):
            winner = 0
        else:
            winner = 1

        return winner
    
    def resetWent(self):
        self.p1Went=False
        self.p2Went=False
