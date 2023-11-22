# import the modules to run the game
from Map import Map
from Bot import Bot
from Game import Game
import importlib
import os

DEFENDER = 'BruteBot'
# Change this to your robot name
CHALLENGER = 'Bot010101'



def readTestMaps(levels):
    """
    Read all the maps in the graded_maps folder for certain levels range
    :param levels: list of levels
    :return: mapInfoDict: a dictionary of map information
    """
    mapInfoDict = {}
    for level in levels:
        mapInfoDict[level] = []
        for filename in os.listdir(f"graded_maps/{level}"):
            # only read csv files
            if filename.endswith('.csv'):
                parameters = filename.split('_')
                mapInfoDict[level].append(
                    {
                        "mapName": f"graded_maps/{level}/{filename}",
                        "nrCols": int(parameters[2]),
                        "nrRows": int(parameters[2]),
                        "nrStains": int(parameters[3]),
                        "nrPillars": int(parameters[5]),
                        "nrWalls": int(parameters[7]),
                        "sizeStains": int(parameters[4]),
                        "sizePillars": int(parameters[6]),
                        "sizeWalls": int(parameters[8]),
                        "checkpoint": [1, 1]
                    }
                )
    return mapInfoDict


def playGame(settings, botName):
    """
    Play the game with the given settings and selected bot
    :param settings: maps settings
    :param botName: bot name
    :return:
    """
    MAX_STEPS = settings["nrCols"] * settings["nrRows"] * 2
    LATENCY = 0
    VISUALS = False
    CLS = True

    module = importlib.import_module(botName)
    cls = getattr(module, botName)

    myMap = Map(settings)
    bot = cls(settings)
    if not getattr(bot, 'name', False):
        bot.setName(botName)
    game = Game(bot, myMap, MAX_STEPS, LATENCY, VISUALS, CLS)

    try:
        res = game.play()
        if res == 'Game Over':
            return 'Out of Energy.'
        else:
            return res
        return
    except Exception:
        return 'Running Error.'


def transformLevelRange(levelRange):
    """
    Transform the level range to a list of levels
    :param levelRange:
    :return: list of levels
    """
    """
    :param levelRange: 
    :return: 
    """
    if len(levelRange) == 1:
        return [levelRange[0]]
    if len(levelRange) == 2:
        return list(range(levelRange[0], levelRange[1] + 1))


def referee(scoreBoard, mapName):
    """
    Judge and print the game results.
    :param scoreBoard: the score of each robot
    :param mapNAme:
    :return: none
    """
    if len(scoreBoard) == 2:
        msg = {
            'CHALLENGER_WIN': f'✅ Passed!  '
                              f'\n\t{CHALLENGER}: {scoreBoard[CHALLENGER]} '
                              f'\n\t{DEFENDER}: {scoreBoard[DEFENDER]}',
            'CHALLENGER_LOSE': f'❌ Failed! '
                               f'\n\t{CHALLENGER}: {scoreBoard[CHALLENGER]}'
                               f'\n\t{DEFENDER}: {scoreBoard[DEFENDER]}.'
                               f'\n\tMap name: {mapName}'
        }
        # print('scoreBoard:', scoreBoard)
        if isinstance(scoreBoard[DEFENDER], int) and not isinstance(scoreBoard[CHALLENGER], int):
            print(msg['CHALLENGER_LOSE'])
        elif not isinstance(scoreBoard[DEFENDER], int) and isinstance(scoreBoard[CHALLENGER], int):
            print(msg['CHALLENGER_WIN'])
        elif not isinstance(scoreBoard[DEFENDER], int) and not isinstance(scoreBoard[CHALLENGER], int):
            print(msg['CHALLENGER_LOSE'])
        elif isinstance(scoreBoard[DEFENDER], int) and isinstance(scoreBoard[CHALLENGER], int):
            if scoreBoard[DEFENDER] > scoreBoard[CHALLENGER]:
                print(msg['CHALLENGER_LOSE'])
            elif scoreBoard[DEFENDER] < scoreBoard[CHALLENGER]:
                print(msg['CHALLENGER_WIN'])
    elif len(scoreBoard) == 1:
        if isinstance(scoreBoard[0], int) :
            print(f'✅ Passed. {CHALLENGER} Score: {scoreBoard[0]}')
        else:
            print(f'❌ Failed. Score: {scoreBoard[0]}'
                  f'\n\tMap name: {mapName}')


def beatBruteBot(levelRange=[6, 7]):
    mapInfoDict = readTestMaps(levels=transformLevelRange(levelRange))

    for level, maps in mapInfoDict.items():
        print('\n🔒 Level:', level, '\n')
        for settings in maps:
            if level < 8:
                scoreBoard = {
                    DEFENDER: 0,
                    CHALLENGER: 0
                }
                for robot in [DEFENDER, CHALLENGER]:
                    # print('currentMap:',settings['mapName'])
                    gameResults = playGame(settings, robot)
                    totalEnergy = settings['nrCols'] * settings['nrRows'] * 2
                    totalStains = settings['nrStains'] * settings['sizeStains']
                    scoreBoard[robot] = gameResults
                referee(scoreBoard, settings['mapName'])
            elif level >= 8:
                scoreBoard = [playGame(settings, CHALLENGER)]
                referee(scoreBoard, settings['mapName'])


if __name__ == "__main__":
    # By default, it will test all the level 6 and level 7 maps
    beatBruteBot()

    # To test a specific level:
    # beatBruteBot([8])

    # To test all levels:
    # beatBruteBot([6,10])
