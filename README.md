# README.md

A simple automation tool to test your robot in different maps and hopefully beat BruteBot.

## Overview

<img src="https://github.com/Celqaz/beatBruteBot/blob/main/img/overview.png" alt="beatBruteBot Overview" style="zoom:33%;" />



## Getting Started

### Download files 

- `graded_maps.zip`
  - Download graded_maps.zip 
  - extract the zip file to get a graded_maps folder 
  - move the graded_maps folder to the same location of your robot code (i.e. root directory).
- `beatBruteBot.py`
  - Download `beatBruteBot.py`
  - move the `beatBruteBot.py` file to the same location of your robot code (i.e root directory).

```html
(💡 The file structure may differ)
.
├── Bot.py
├── Bot010101.py
├── BruteBot.py
├── Game.py
├── Map.py
├── RandomBot.py
├── app.py
├── beatBruteBot.py
├── graded_maps
│   ├── 10
│   │   ├── map_10_20_10_1_1_3_10_3_.csv
│   │   ├── map_10_20_1_1_3_3_15_3_.csv
│   │   ├── map_10_30_10_2_1_7_15_5_.csv
│   │   └── map_10_30_2_3_20_3_20_3_.csv
│   ├── 6
│   │   ├── map_6_30_10_3_0_0_0_0_.csv
│   │   ├── map_6_30_1_3_0_0_0_0_.csv
│   │   ├── map_6_30_2_3_0_0_0_0_.csv
│   │   └── map_6_30_5_3_0_0_0_0_.csv
│   ├── 7
│   │   ├── map_7_15_10_1_0_0_0_0_.csv
│   │   ├── map_7_25_1_4_0_0_0_0_.csv
│   │   ├── map_7_30_5_3_0_0_0_0_.csv
│   │   └── map_7_50_50_1_0_0_0_0_.csv
│   ├── 8
│   │   ├── map_8_20_1_3_10_2_0_0_.csv
│   │   ├── map_8_30_1_1_20_1_0_0_.csv
│   │   ├── map_8_30_3_2_5_2_0_0_.csv
│   │   └── map_8_30_5_1_2_5_0_0_.csv
│   └── 9
│       ├── map_9_20_1_1_1_5_1_9_.csv
│       ├── map_9_30_20_1_1_3_10_3_.csv
│       ├── map_9_30_2_3_5_3_5_4_.csv
│       └── map_9_40_1_1_1_3_30_3_.csv
├── logs
```

### Edit `Game.py`

In `Game.py` , change the following code snippets:

```python
def play(self):
  	...
		if self.energy<=0:
			print("game over, " +botName+  " ran out of energy")
		elif self.map.remainingStains<=0:
			print(botName + " finished the map with a score of ", self.energy)
```

to:

```python
def play(self, debug):
  	...
		if self.energy<=0:
			# print("game over, " +botName+  " ran out of energy")
			return 'Game Over'
		elif self.map.remainingStains<=0:
			# print(botName + " finished the map with a score of ", self.energy)
			return self.energy
```

and add the following lines right under `time.sleep(self.latency)` on line 27:

```python
if debug:
	next = input()
	if next:
		return 'Next'
```

### Edit `Map.py`
Lastly, in `Map.py`, add:

```python
self.overlap = [str(i) for i in range(10)]
```

on line 19, right below:

```python
self.botPosition = self.checkpoint[:] #bot always starts at the checkpoint` on line 18.
```

Then, change the signature of the `moveRobot()` method on line 58, from:

```python
def moveRobot(self, move)
```

to:

```python
def moveRobot(self, move, debug=False)
```

and change the lines after:

```python
elif move == 'right':
	self.botPosition[1] = self.botPosition[1]+1
	if self.map[self.botPosition[0]][self.botPosition[1]] == '@':
		self.remainingStains -=1
```

to the ones below, but make sure to stay within the `moveRobot()` method:

```python
self.currentSign = self.map[self.botPosition[0]][self.botPosition[1]]
self.map[self.botPosition[0]][self.botPosition[1]] = 'B'
if currentPosition == self.checkpoint:
	self.map[currentPosition[0]][currentPosition[1]] = '1'
else:
	if self.currentSign in self.overlap:
		if self.currentSign == '9' or self.currentSign == 'S':
			self.overlap.append('S')
			self.map[currentPosition[0]][currentPosition[1]] = 'S'
		else:
			self.map[currentPosition[0]][currentPosition[1]] = self.overlap[self.overlap.index(self.currentSign) + 1]
	else:
		self.map[currentPosition[0]][currentPosition[1]] = '1'
```



## Settings in `beatBruteBot.py` 

### Choose your hero

In `beatBruteBot.py` , change the value of the variable `CHALLENGER` on the 10th line to your robot name.

```python
# Change this to your robot name
CHALLENGER = 'Bot010101'
```

### Customize the testing levels

At the bottom of the `beatBruteBot.py`, you can customized the levels you want to test your robot.

```python
#......

if __name__ == "__main__":
    # 1. By default, it will test all the maps in level 6 and level 7
    beatBruteBot()

    # 2. To test a specific level:
    # beatBruteBot([8])

    # 2. To test all levels:
    # beatBruteBot([6,10])
```

## Run the game

In jupyter-lab terminal, run

```shell
python beatBruteBot.py

# or

python3 beatBruteBot.py
```



Good luck!





