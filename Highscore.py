
class Highscores:
    def __init__(self):
        self.file_name = "Highscore.txt"
        self.scores = []
        self.read_scores()
#        self.add_score("nisåss2", 2)
        self.print_scores()
        self.write_scores()
        return

    def read_scores(self):
        file = open(self.file_name,"r")
        scoreslines = file.readlines()
        for scorepairs in scoreslines:
            pair = scorepairs.split()
            name = pair[0]
            score = int(pair[1])
            scoreitem = (score, name)
            self.scores.append(scoreitem)
            print("Name = " + name + " had score = " + str(score))
        file.close()
        return

    def add_score(self,name,score):
        new_score_item = (score, name)
        self.scores.append(new_score_item)
        self.sort_scores()
        if len(self.scores) > 10:
            self.scores = self.scores[:10]
        self.write_scores()

    def sort_scores(self):
        sortedscores = sorted(self.scores,key = lambda score: score[0])
        self.scores = sortedscores
        return

    def get_scores(self):
        self.sort_scores()
        lines = ""
        self.scores.reverse()
        for score in self.scores:
            name = score[1]
            val  = score[0]
            lines = "Name = " + name + " had score = " + str(val) + "\n" + lines
        return lines

    def print_scores(self):
        print("Sorted")
        self.sort_scores()
        for score in self.scores:
            name = score[1]
            val  = score[0]
            print("Name = " + name + " had score = " + str(val))
        return

    def write_scores(self):
        file = open(self.file_name,"w")
        lines = []
        for score in self.scores:
            name = score[1]
            val = score[0]
            line = name + " " + str(val) + "\n"
            file.write(line)
        file.close()

        return
