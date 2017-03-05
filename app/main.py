import bottle
import os
import random
import math

my_name = "elttab ekans"
color = "#234864"
taunt = "Get some!"



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    global board_width
    global board_height
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': taunt,
        'head_url': head_url,
        'name': my_name
    }


@bottle.post('/move')
def move():
    global board_width
    global board_height
    #Get request data
    data = bottle.request.json
    my_id = data['you']
    snakes = data['snakes']
    turn = data['turn']
    food = data['food']
    board_width = data['width']
    board_height = data['height']
    #Get our snake
    for snake in snakes:
    	    if snake['id'] == my_id:
    	    	my_snake = snake
    	    	health = snake['health_points']
    #Head coordinates and coordinates of adjacent spaces
    my_head = my_snake['coords'][0]
    
    adjacent = {}
    adjacent['up'] = [my_head[0], my_head[1]-1]
    adjacent['down'] = [my_head[0], my_head[1]+1]
    adjacent['left'] = [my_head[0]-1, my_head[1]]
    adjacent['right'] = [my_head[0]+1, my_head[1]]
    
    #Determine which directions are clear to move
    viable_move = {}
    for direction, coord in adjacent.items():
    	    viable_flag = True
    	    if coord[0] < 0 or coord[0] > board_width - 1: #if X coord is a wall value don't include direction
    	    	    viable_flag = False
	    elif coord[1] < 0 or coord[1] > board_height - 1: #if Y coord is a wall value don't include direction
		    viable_flag = False
	    for snake in snakes:
		    if viable_flag == False: #if coord == a point in previous snake then break
			    break
		    for point in snake['coords']: #compare coord to all body points of snake
			    if point == coord: #if this point in snake == coord then don't include direction and break
				    viable_flag = False
				    break
	    if viable_flag == True: #if viable flag is still true then add direction to possible moves	    	    	    	    	    	    
    	    	    viable_move[direction] = coord
    if health < 50: #go get apple
        if len(food) > 0:
            distance = []
            target = []
            for i in range(len(food)):
                distance[i] = math.fabs(food[i][0] - my_head[0]) + math.fabs(food[i][1] - my_head[1])
            	if i == 0:
            		target = food[i]
            	elif distance[i] < distance[i-1]:
            		target = food[i]
            for dist in distance:
                if target > dist:
                    target = dist
        if (my_head[0] > target[0]):    # If the food is to the left of the head
            if 'left' in viable_move:
                # Clear other viable moves
                viable_move = 'left' 
        elif (my_head[0] < target[0]):  # If the food is to the right of the head
            if 'right' in viable_move:
                # Clear other viable moves
                viable_move = 'right'
        elif (my_head[1] > target[1]):  # If the food is above the head
            if 'up' in viable_move:
                # Clear other viable moves
                viable_move = 'up'
        else:                           # If the food is below the head
            if 'down' in viable_move:
                # Clear other viable moves
                viable_move = 'down'
        
    else: #keep doing other stuff #TODO: Implement Snake behavioural AI

            for snake in snakes:
                for dir,coord in adjacent.items():
                    if snake['coords'] == coord:
                        if len(my_snake['coord']) > len(snake['coord']):
                            kill_flag = True
                            saveDir = dir
                            taunt = 'kill flag'
                            break
                        else:
                            kill_flag = False




        #pick and send move
        directions = {'up': 'up', 'down':'down', 'left':'left', 'right':'right'}
        if kill_flag == True:
            if saveDir in viable_move:
             move = saveDir
        else:
            move = random.choice(viable_move.key())

    return {
        'move': move,
        'taunt': taunt
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
