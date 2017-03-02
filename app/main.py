import bottle
import os
import random

my_name = "elttab ekans"
color = "#234864"
taunt = "Get some!"



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
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
    #Get request data
    data = bottle.request.json
    my_id = data['you']
    snakes = data['snakes']
    turn = data['turn']
    health = data['health']
    food = data['food']
    
    #Get our snake
    for snake in snakes:
    	    if snake.id == my_id:
    	    	my_snake = snake
    	    	
    #Head coordinates and coordinates of adjacent spaces
    my_head = my_snake[0]
    adjacent = {}
    adjacent['up'] = [my_head[0], my_head[1]-1]
    adjacent['down'] = [my_head[0], my_head[1]+1]
    adjacent['left'] = [my_head[0]-1, my_head[1]]
    adjacent['right'] = [my_head[0]+1, my_head[1]]
    
    #Determine which directions are clear to move
    viable_move = {}
    for direction, coord in adjacent.items():
    	    viable_flag = true
    	    if coord[0] < 0 or coord[0] >= board_width: #if X coord is a wall value don't include direction
    	    	    viable_flag = false
	    elif coord[1] < 0 or coord[1] >= board_height: #if Y coord is a wall value don't include direction
		    viable_flag = false
	    for snake in snakes:
		    if viable_flag == false: #if coord == a point in previous snake then break
			    break
		    for point in snake.coords: #compare coord to all body points of snake
			    if point == coord: #if this point in snake == coord then don't include direction and break
				    viable_flag = false
				    break
	    if viable_flag == true: #if viable flag is still true then add direction to possible moves	    	    	    	    	    	    
    	    	    viable_move[direction] = coord
    #TODO: Implement Snake behavioural AI
    
    #pick and send move
    directions = {'up': 'up', 'down':'down', 'left':'left', 'right':'right'}
    #move = direction['thedirection']
    return {
        'move': move,
        'taunt': taunt
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
