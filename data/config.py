# api id, hash
API_ID = 8888888888
API_HASH = ''

USE_TG_BOT = False  # True if you want use tg, else False
BOT_TOKEN = '99999999:asdasdasdasdasd'  # API TOKEN get in @BotFather
CHAT_ID = '99999999'  # Your telegram id

# Delay between account connections
ACC_DELAY = [5, 15]

# proxy type ( ignore if you are not using proxies)
PROXY_TYPE = "socks5"  # http/socks5

# Sessions folder ( DO NOT CHANGE )
WORKDIR = "sessions/"

# Proxy usage
USE_PROXY = False  # True/False

# max level value that bot will upgrade to
UPGRADE_LEVEL = 20

# tapsCount range ( how many taps the bot will send per request, maximum cap on the server is 200, don't use value higher than that or you will send less taps or no taps at all)
TAPS_COUNT_RANGE = (190, 200)  # (min, max)

hello = ''' 
___________                    ________               
\__    ___/___   _____ ________\______ \   _______  __
  |    |_/ __ \ /     \\___   / |    |  \_/ __ \  \/ /
  |    |\  ___/|  Y Y  \/    /  |    `   \  ___/\   / 
  |____| \___  >__|_|  /_____ \/_______  /\___  >\_/  
             \/      \/      \/        \/     \/     
'''

TOOLS = {
    'Bombucks',
    'coinflip',
    'BrawlPirates',
    'RocketQueen',
    'RoyalMines',
    'LuckyJet',
    'Double',
    'AnubisPlinko',
    'Mines',
    'LuckyLoot',
    'RocketX',
    'SpeednCash',
    'Tower'
}

REQUIRED = {
    'coinflip': None,
    'Mines': None,
    'Bombucks': None,
    'Tower': None,
    'Double': 'Mines8',
    'RoyalMines': 'coinflip5',
    'LuckyLoot': 'coinflip11',
    'BrawlPirates': 'Bombucks3',
    'AnubisPlinko': 'Tower7',
    'RocketX': 'BrawlPirates7',
    'SpeednCash': 'AnubisPlinko7',
    'RocketQueen': 'LuckyLoot3',
    'LuckyJet': 'SpeednCash5'
}


class Price:
    def __init__(self, base, levels):
        self.base = base
        self.levels = levels

    def get_prices(self):
        return {f"{self.base}{level}": self.levels[level - 1] for level in range(1, len(self.levels) + 1)}


# Define prices for each tool
price_configs = [
    Price('coinflip', [150, 205, 275, 370, 500, 675, 910, 1230, 1650, 2230,
          3020, 4100, 5500, 7400, 10000.0, 13500, 18300, 24600, 33300, 45000.0]),
    Price('Mines', [340, 440, 570, 750, 950, 1250, 1650, 2150, 2750, 3600,
          4700, 6100, 7900, 10300, 13400, 17400, 22600, 29400, 38200, 50000.0]),
    Price('Bombucks', [480, 640, 850, 1150, 1500, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0,
          8000.0, 11000.0, 15000.0, 20000.0, 26000.0, 35000.0, 46000.0, 61000.0, 81000.0, 110000.0]),
    Price('Tower', [555, 745, 995, 1350, 1790, 2400, 3000.0, 4000.0, 6000.0, 8000.0, 10000.0,
          14000.0, 19000.0, 25000.0, 33000.0, 45000.0, 60000.0, 80000.0, 110000.0, 145000.0]),
    Price('Double', [1200, 1600, 2200, 3000.0, 4000.0, 5400, 7000.0, 10000.0, 13000.0, 18000.0,
          24000.0, 33000.0, 44000.0, 59000.0, 80000.0, 110000.0, 150000.0, 200000.0, 270000.0, 360000.0]),
    Price('RoyalMines', [1500, 2100, 2900, 4050, 5600, 7800, 11000.0, 15000.0, 21000.0, 29000.0,
          40000.0, 56000.0, 78000.0, 108000.0, 151000.0, 210000.0, 290000.0, 400000.0, 560000.0, 800000.0]),
    Price('LuckyLoot', [2200, 3100, 4300, 6000.0, 8500, 11800, 17000.0, 23000.0, 32000.0, 45000.0,
          65000.0, 90000.0, 125000.0, 175000.0, 250000.0, 350000.0, 480000.0, 670000.0, 950000.0, 1500000.0]),
    Price('BrawlPirates', [4000.0, 5550, 7700, 10600, 14500, 20500, 28000.0, 39000.0, 54000.0, 75000.0,
          105000.0, 140000.0, 199000.0, 275000.0, 400000.0, 550000.0, 750000.0, 1000000.0, 1400000.0, 1950000.0]),
    Price('AnubisPlinko', [5500, 7700, 11000.0, 15000.0, 21000.0, 30000.0, 41000.0, 60000.0, 82000.0, 115000.0,
          160000.0, 225000.0, 310000.0, 440000.0, 610000.0, 850000.0, 1200000.0, 1700000.0, 2500000.0, 3300000.0]),
    Price('RocketX', [20000.0, 30000.0, 45000.0, 70000.0, 100000.0, 150000.0, 250000.0, 350000.0, 500000.0, 770000.0,
          1150000.0, 1750000.0, 2600000.0, 3900000.0, 5800000.0, 9000000.0, 13000000.0, 19500000.0, 29500000.0, 44500000.0]),
    Price('SpeednCash', [33333, 50000.0, 75000.0, 110000.0, 170000.0, 255000.0, 400000.0, 550000.0, 850000.0, 1300000.0,
          1900000.0, 3000000.0, 4300000.0, 6500000.0, 9700000.0, 14500000.0, 22000000.0, 33000000.0, 50000000.0, 75000000.0]),
    Price('RocketQueen', [50000.0, 77500, 120000.0, 200000.0, 300000.0, 450000.0, 700000.0, 1100000.0, 1700000.0, 2600000.0,
          4000000.0, 6000000.0, 9600000.0, 14900000.0, 23100000.0, 36000000.0, 55500000.0, 86000000.0, 130000000.0, 205000000.0]),
    Price('LuckyJet', [100000.0, 165000.0, 300000.0, 450000.0, 700000.0, 1200000.0, 2000000.0, 3300000.0, 5500000.0, 9100000.0,
          15000000.0, 25000000.0, 41000000.0, 65000000.0, 110000000.0, 185000000.0, 300000000.0, 500000000.0, 820000000.0, 1500000000.0]),
]

# Generate the PRICES dictionary
PRICES = {}
for config in price_configs:
    PRICES.update(config.get_prices())

# Add any specific price overrides here if necessary
PRICES.update({
    'key': 666.00
})
