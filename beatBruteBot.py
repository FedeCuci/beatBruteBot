# import the modules to run the game
from Map import Map
from Bot import Bot
from Game import Game
import importlib
import os
import sys
from typing import List, Dict, Union, Optional

DEFENDER = 'BruteBot'
# Change this to your robot name
CHALLENGER = 'Bot4331261'
    

def readTestMaps(levels: List[int], debug: bool, maps=[]):
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
                # If in debug mode, do not append solved maps
                if debug and f"graded_maps/{level}/{filename}" not in maps: 
                    continue
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

def playGame(settings, botName: str, debug: bool) -> Union[str, int]:
    """
    Play the game with the given settings and selected bot
    :param settings: maps settings
    :param botName: bot name
    :return:
    """
    MAX_STEPS = settings["nrCols"] * settings["nrRows"] * 2
    LATENCY = 0
    VISUALS = True if debug and botName != 'BruteBot' else False
    CLS = True

    module = importlib.import_module(botName)
    cls = getattr(module, botName)

    myMap = Map(settings)
    bot = cls(settings)
    if not getattr(bot, 'name', False):
        bot.setName(botName)
    game = Game(bot, myMap, MAX_STEPS, LATENCY, VISUALS, CLS)

    try:
        res = game.play(debug)

        if res == 'Game Over':
            return 'Out of Energy.'
        else:
            return res
        return
    except Exception as e:
        return f'Runtime Error:\n {e}' # Add a more specific error


def transformLevelRange(maps: List[int]) -> List[int]:
    """
    Transform the level range to a list of levels
    :param maps:
    :return: list of levels
    """
    """
    :param maps: 
    :return: 
    """
    if len(maps) == 1:
        return [maps[0]]
    if len(maps) == 2:
        return list(range(maps[0], maps[1] + 1))


def referee(scoreBoard: Dict[str, Union[int, str]], mapName: str, debug: bool) -> Optional[str]:
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
            if not debug:
                return mapName
    return


def beatBruteBot(maps: Union[List[int], List[str]] = [6, 7], debug: bool = False) -> None:
    
    failedMaps = []

    # Check if all maps need to be run or only failed maps
    if all(isinstance(x, int) for x in maps):
        mapInfoDict = readTestMaps(transformLevelRange(maps), debug)
    else:
        mapInfoDict = readTestMaps([6,7,8,9,10], debug, maps)

    for level, map in mapInfoDict.items():
        if not debug:
            print('\n🔒 Level:', level, '\n')
        for settings in map:
            if level < 8:
                scoreBoard = {
                    DEFENDER: 0,
                    CHALLENGER: 0
                }

                for robot in [DEFENDER, CHALLENGER]:
                    # print('currentMap:',settings['mapName'])
                    gameResults = playGame(settings, robot, debug)
                    totalEnergy = settings['nrCols'] * settings['nrRows'] * 2
                    totalStains = settings['nrStains'] * settings['sizeStains']
                    scoreBoard[robot] = gameResults
                failedMap = referee(scoreBoard, settings['mapName'], debug)
                if failedMap:
                    failedMaps.append(failedMap)

            elif level >= 8:
                scoreBoard = [playGame(settings, CHALLENGER, debug)]
                failedMap = referee(scoreBoard, settings['mapName'], debug)
                if failedMap: # Check if there were failed maps
                    failedMaps.append(failedMap)
    
    if failedMaps:
        debug = input('\nDo you want to debug the failed maps? (y/n)')
        if debug.lower() in ('y', 'yes'):
            # Clear screen for Linux or Windows
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            beatBruteBot(failedMaps, True)


if __name__ == "__main__":
    
    # By default, it will test all the level 6 and level 7 maps
    # beatBruteBot()

    # To test a specific level:
    # beatBruteBot([8])
    # To test all levels:
    beatBruteBot([6,10])