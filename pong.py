from sense_hat import SenseHat, ACTION_PRESSED
import time

def printBoard(sense, game):
	if game['changed'] == False:
		return

	sense.clear()

	# print paddles
	for y in range(0, 3):
		sense.set_pixel(0, game['left'] + y, [255, 0, 0])
		sense.set_pixel(7, game['right'] + y, [0, 255, 0])
	
	# print dot
	sense.set_pixel(game['dot']['x'], game['dot']['y'], game['dot']['color'])

	game['changed'] = False

def moveDot(game):
        game['dot']['x'] += game['dot']['direction']['x']
	game['dot']['y'] += game['dot']['direction']['y']
	#print("moved to (%d, %d)" % (game['dot']['x'], game['dot']['y']))

def moveComputer(game):

        if time.time() - game['lastAIMove'] < 0.1:
		return
	else:
		game['lastAIMove'] = time.time()
		
        y = game['dot']['y']
        p = game['left']

        if y - p > 1 and y < 5:
                game['left'] += 1
                game['changed'] = True
        elif y - p < 1 and y > 0:
                game['left'] -= 1
                game['changed'] = True

def updateGame(game):
	if time.time() - game['lastDotMove'] < 0.25:
		return
	else:
		game['lastDotMove'] = time.time()
		game['changed'] = True

	moveDot(game)

	x = game['dot']['x']
	y = game['dot']['y']

	if x < 0:
		print("Human wins!")
		return 2
	elif x > 7:
		print("The machine wins!")
		return 1
	elif y < 0 or y > 7:
                # Reverse direction and move ("undo move")
                game['dot']['direction']['x'] *= -1
                game['dot']['direction']['y'] *= -1
                moveDot(game)

                # Restore x direction
                game['dot']['direction']['x'] *= -1
                
                moveDot(game)

        x = game['dot']['x']
	y = game['dot']['y']

	if x == 0 and y - game['left'] >= 0 and y - game['left'] < 3:
                hit = y - game['left']

                # Reverse direction and move ("undo move")
                game['dot']['direction']['x'] *= -1
                game['dot']['direction']['y'] *= -1
                moveDot(game)

                if hit == 0:
                        game['dot']['direction']['y'] = -1
                elif hit == 2:
                        game['dot']['direction']['y'] = 1

                #moveDot(game)
        elif x == 7 and y - game['right'] >= 0 and y - game['right'] < 3:
                hit = y - game['right']

                # Reverse direction and move ("undo move")
                game['dot']['direction']['x'] *= -1
                game['dot']['direction']['y'] *= -1
                moveDot(game)

                if hit == 0:
                        game['dot']['direction']['y'] = -1
                elif hit == 2:
                        game['dot']['direction']['y'] = 1

                #moveDot(game)

        return 0
                

def readInput(sense, game):
	for event in sense.stick.get_events():
		if event.action == "pressed" and event.direction == "up" and game['right'] > 0:
			game['right'] -= 1
			game['changed'] = True
		elif event.action == "pressed" and event.direction == "down" and game['right'] < 5:
			game['right'] += 1
			game['changed'] = True

def gameLoop(sense, dotColor):
	game = {
		'dot': {'x': 3, 'y': 3, 'direction': {'x': 1, 'y': 0}, 'color': dotColor},
		'left': 3,
		'right': 2,
		'lastDotMove': time.time(),
                'lastAIMove': time.time(),
		'changed': True
	}
	
	while (True):
		# print board
		printBoard(sense, game)
		
		# read actions
		readInput(sense, game)
		moveComputer(game)

		# respond to events
		out = updateGame(game)

		if out == 1:
                        return (255, 0, 0)
                elif out == 2:
                        return (0, 255, 0)

		time.sleep(0.05)

sense = SenseHat()
sense.low_light = True
sense.clear()
#printBoard(sense)

dotColor = (255, 255, 255)

while True:
        dotColor = gameLoop(sense, dotColor)
