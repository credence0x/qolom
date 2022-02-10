from random import choice

alpha           = ['A','B','C','D','E','F','G','H',
                    'I','J','K','L','M','N','O','P',
                    'Q','R','S','T','U','V','W','X',
                    'Y','Z','1','2','3','4','5','6',
                    '7','8','9','0']

beta               = ['A','B','C','D','E','F','G','H',
                    'I','J','K','L','M','N','P',
                    'Q','R','S','T','U','V','W','X',
                    'Y','Z','a','b','c','d','e','f',
                    'g','h','i','j','k','m','n',
                    'p','q','r','s','t','u','v',
                    'w','x','y','z','2','3','4',
                    '5','6','7','8','9']
                    # no 0,o,O,1,l to avoid confusion
                    # key must be 7

                    
def getRandomTicket(num):
        ticket = ""
        for _ in range(num):
            ticket += choice(alpha)
        return ticket
        


def getRandomKey(num):
        ticket = ""
        for _ in range(num):
            ticket += choice(beta)
        return ticket
        