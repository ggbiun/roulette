from random import randint as r
from math import log2, floor

class Roulette:
    """ Roulette class for representing and manipulating a roulette spin wheel. """

    def __init__(self, color_streak, min_bet, max_bet, spin_time, max_dur, net_gain_stop):
        self.color_streak=color_streak  #Sets how many same color spins need to occur until a bet is placed on the opposite color.
        self.min_bet=min_bet
        self.max_bet=max_bet
        self.spin_time=spin_time
        self.max_dur=max_dur
        self.net_gain_stop=net_gain_stop
        self.game_counter=0
        self.loss_streak=0
        self.max_loss_streak=0
        self.game_bet=min_bet
        self.start_balance=min_bet*(2*(2**floor(log2(max_bet/min_bet)))-1) #calculate starting balance where n=log2(max bet/min bet))
        self.game_balance=self.start_balance
        self.max_game_counter=floor(60*self.max_dur/self.spin_time)
        self.game_color_streak=0
        self.previous_color=''  #Used to determine color streak
        self.wheel_color_landed='NONE'
        self.bet_color='NA'
        self.bet_next_spin=False
        self.game_outcome='NA'
    
    def wait_for_streak(self):
        if self.wheel_color_landed != 'g':
            if self.wheel_color_landed == self.previous_color:
                self.game_color_streak+=1
                if self.game_color_streak >= self.color_streak:
                    if self.wheel_color_landed == 'r':
                        self.bet_color='b'
                    self.bet_color='r'
            else:
                self.game_color_streak=1
                if self.game_counter !=0:
                    self.previous_color=self.wheel_color_landed
        else:
            self.game_color_streak=1
       
    def spin_wheel(self):
        self.game_counter+=1
        list_pos=0
        available = ['-0g', '28b', '09r', '26b', '30r', '11b', '07r', '20b', '32r', '17b',
            '05r', '22b', '34r', '15b', '03r', '24b', '36r', '13b', '01r', '00g',
            '27r', '10b', '25r', '29b', '12r', '08b', '19r', '31b', '18r', '06b', 
            '21r', '33b', '16r', '04b', '23r', '35b', '14r', '02b']
        list_pos=r(0,37)
        self.wheel_color_landed = available[list_pos][2:] #returns (r)ed, (b)lack, (g)reen
        if self.bet_color=='NA':
            if self.wheel_color_landed in ('g', 'r'):
                self.bet_color='b'
            else:
                self.bet_color='r'
        
    def bet_or_pass(self):
        #Determine if a bet should be made or wait for streak
        if self.game_color_streak>=self.color_streak:
            self.bet_next_spin = True
        else:
            self.bet_next_spin=False
        return self.bet_next_spin

    def process_bet(self):
        if self.wheel_color_landed == self.bet_color: #Won or Lost
            self.game_outcome='Won'
            self.game_balance+=self.game_bet
            self.game_bet=self.min_bet
            self.loss_streak=0
            self.game_color_streak
        else:
            self.game_outcome='Lost'
            self.game_balance-=self.game_bet
            self.game_bet*=2
            self.loss_streak+=1
            if self.loss_streak>self.max_loss_streak:
                self.max_loss_streak=self.loss_streak
        self.game_color_streak=0
        return self.game_outcome

    def game_over(self):
        if ((self.game_counter >= self.max_game_counter and self.game_outcome == 'Won') or 
            self.game_bet > self.max_bet or self.game_bet > self.game_balance or
            (self.game_balance-self.start_balance)>=self.net_gain_stop):
            return 'Game Over'

    def final_results(self):
        net=(self.game_balance-self.start_balance) #/(self.game_counter*self.spin_time/60)
        return (self.game_counter, self.min_bet, self.max_bet, self.start_balance, 
        self.game_balance, net, self.max_loss_streak)

    def __repr__(self):
        return 'Hello World'

def main():
    day=0
    net_gain=0
    min_bet=int(input('Enter Min Bet: '))
    color_streak=int(input("Enter Color Streak Before Bet: "))
    net_gain_stop=int(input("Daily Net Gain: "))
    for y in range(365):
        x=''
        min_bet=5 #int(input('Enter Min Bet: '))
        max_bet=5000 #int(input('Enter Max Bet: '))
        spin_time=1 #float(input('Enter Time Between Spins (minutes): '))
        max_dur=4 #float(input('Enter Max Play time (hours): '))
        gambler=Roulette(color_streak, min_bet, max_bet, spin_time, max_dur, net_gain_stop)
        while x !='Game Over':
            gambler.wait_for_streak()
            if gambler.bet_or_pass():
                    gambler.spin_wheel()
                    gambler.process_bet()
            else:
                gambler.spin_wheel()
            x=gambler.game_over()
            net=gambler.final_results()
        day+=1
        net_gain+=net[5]
        print('Day: ', day, gambler.final_results(), 'Net= ', net_gain)
        
if __name__ == "__main__":
    main()


# This is a Test
# Test add by ggbiun