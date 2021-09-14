import pygame, random, sys, copy, os
from pygame.locals import *

#window
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080
FPS = 60
FSCREEN = False

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (25,253,218)

#game
GRIDSIZE = 8 #ONLY EVEN SIZES!!!

#checks if running windows Vista or newer. Code used to determine whether winodw stretching needs to be disabled
if os.name != 'nt' or sys.getwindowsversion()[0]<6:
    raise NotImplementedError('this game requires Windows Vista or newer')
else:
    import ctypes
    #prevent stretching
    ctypes.windll.user32.SetProcessDPIAware()

#class for creating temporary surfaces. Only one object is required per program
class tempSurfaces:
    #initialisation
    def __init__(self):
        self.surfaces = []
    #adds surface to the que
    def add(self,text,surface,rect,time):
        contains = False
        for i in self.surfaces:
            if text == i[0]:
                contains = True
        if not contains:
            self.surfaces.append([text,surface,rect,int(time)*1000 if time.isdigit() else time])               

    #displays temporary surface, if it has a timer it uses the timer, otherwise keeps it until a delete is requested   
    def display(self):
        for surf in self.surfaces[:]:
            if str(surf[3]).isdigit():
                surf[3]-= mainClock.get_time()

                if surf[3] > 0:
                    windowSurface.blit(surf[1],surf[2])
                    drawText(surf[0],getFont(getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)[0]),windowSurface,surf[2].centerx,surf[2].centery,True)

                if surf[3] <= 0:
                    self.surfaces.remove(surf)
            else:
                windowSurface.blit(surf[1],surf[2])
                drawText(surf[0],getFont(getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)[0]),windowSurface,surf[2].centerx,surf[2].centery,True)
    #deltes an infinite temporary surface by text
    def delete(self,text):
        for i in self.surfaces[:]:
            if text == i[0]:
                self.surfaces.remove(i)
                
#gets a font size which will fit instructions within window
def getMenuSize(wWidth, wHeight):
    size = int(((wWidth+wHeight)//2)//30)
    space = int(((wWidth+wHeight)//2)//40)
    return (size,space)
    
#draws text
def drawText(text,font,surface,x,y,centered = False):
    textobj = font.render(text,1,WHITE)
    textrect = textobj.get_rect()
    if not centered:
        textrect.topleft = (x,y)
    elif centered:
        textrect.center = (x,y)
    surface.blit(textobj,textrect)

#creates a font
def getFont(size):
    return pygame.font.SysFont(None,size)

#exits system
def terminate():
    pygame.quit()
    sys.exit()

#creates a new board
def newBoard(size):
    board = []
    for i in range(0,size+1):
        board.append([' '] * (size+1))
    size = int(size/2)
    board[size][size],board[size + 1][size],board[size][size + 1],board[size + 1][size + 1] = 'B','W','W','B'
    return board

#Waits for an input in the menu and displays results (Instructions, Play Game, or Quit
def menuInput(wWidth,wHeight):
    size = getMenuSize(wWidth,wHeight)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == ord('i'):
                    windowSurface.fill(BACKGROUND)
                    drawText('Reversi',getFont(60),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/10),True)
                    drawText('A game by prokopchukdim',getFont(30),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/10)+ 50,True)
                    drawText('Reversi is a board game. Each reversi piece has a black and white side.',getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*1,True)
                    drawText('On your turn you place one piece on the board with your color facing up.',getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*2,True)
                    drawText('You must place the piece so that an opponent\'s piece, or a row of opponent\'s pieces, is flanked by your pieces.',getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*3,True)
                    drawText('All of the opponent\'s pieces between your pieces are then turned over to become your color.',getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*4,True)
                    drawText('The aim of the game is to own more pieces than your opponent when the game is over.',getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*5,True)
                    drawText("The game is over when neither player can make more moves.", getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*6,True)
                    drawText("Press 'Enter/Return' to play", getFont(size[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+size[1]*8,True)

                
                    pygame.display.update()
                    menuInput(wWidth,wHeight)
                    return

                if event.key == K_RETURN:
                    return

#Asks player whether they would like to play as the black or white pieces
def getPlayer(wWidth,wHeight,black,white):
    windowSurface.fill(BACKGROUND)
    size = getMenuSize(wWidth,wHeight)
    
    drawText('Do you want to be Black or White?',getFont(size[0]),windowSurface, wWidth/2, wHeight/3, True)

    wRect = pygame.Rect(0,0,size[1]*3,size[1]*3)
    bRect = pygame.Rect(0,0,size[1]*3,size[1]*3)
    white = pygame.transform.scale(white,(wRect.width,wRect.height))
    black = pygame.transform.scale(black,(bRect.width,bRect.height))

    wRect.center = (wWidth/2 - size[1]*2,wHeight/3 + size[1]*5)
    bRect.center = (wWidth/2 + size[1]*2,wHeight/3 + size[1]*5)
    
    windowSurface.blit(white,wRect)
    windowSurface.blit(black,bRect)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if event.pos[0] in range(wRect.left,wRect.right+1) and event.pos[1] in range(wRect.top,wRect.bottom+1):
                        return ('W','B')
                    if event.pos[0] in range(bRect.left,bRect.right+1) and event.pos[1] in range(bRect.top,bRect.bottom+1):
                        return ('B','W')

#returns true if player is going first
def playerFirst():
    return random.choice([True,False])

#displays to player who will go first
def displayFirstTurn(turn):
    fSize = getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)
    windowSurface.fill(BACKGROUND)
    if turn:
        drawText('You will go first',getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,WINDOWHEIGHT/2,True)
    else:
        drawText('The AI will go first',getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,WINDOWHEIGHT/2,True)
    drawText("Press 'Enter'/'Return' to start",getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,WINDOWHEIGHT/2 + fSize[1],True)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN:
                    return 
            
#draws board onto screen
def drawBoard(board,size,white,black):
    
    windowSurface.fill(BACKGROUND)
    width = WINDOWHEIGHT - 200
    white = pygame.transform.scale(white,(int((width/size)*0.8),int((width/size)*0.8)))
    black = pygame.transform.scale(black,(int((width/size)*0.8),int((width/size)*0.8)))
    #draws board lines
    for i in range(size + 1):
        pygame.draw.line(windowSurface,BLACK,((WINDOWWIDTH/2)-(width/2)+(i*(width/size)), 100), ((WINDOWWIDTH/2)-(width/2)+(i*(width/size)),WINDOWHEIGHT - 100), 4)
        pygame.draw.line(windowSurface,BLACK,((WINDOWWIDTH/2)-(width/2),(WINDOWHEIGHT/2)-(width/2)+(i*(width/size))),((WINDOWWIDTH/2)+(width/2),(WINDOWHEIGHT/2)-(width/2)+(i*(width/size))), 4)

    #create template for piece size depending on resolution and board size
    swidth = sheight = int((width/size)*0.8)
    pieceTemplate = pygame.Rect(0,0,swidth,sheight)
    
    #draws placed pieces onto board
    for i in range(size):
        for j in range(size):
            if board[i+1][j+1] in ['B','W']:
                centerX = (WINDOWWIDTH/2)-(width/2)+((width/size)/2)+((width/size)*i)
                centerY = (WINDOWHEIGHT/2)-(width/2)+((width/size)/2)+((width/size)*j)
                pieceTemplate.center = (centerX,centerY)
                if board[i+1][j+1] == 'B':
                    windowSurface.blit(black,pieceTemplate)
                if board[i+1][j+1] == 'W':
                    windowSurface.blit(white,pieceTemplate)

#Draws user's and AI's points on screen
def drawPoints(points):
    drawText('You have %s points'%(points[0]),getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,25,True)
    drawText('The AI has %s points'%(points[1]),getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,75,True)

#draws FPS on screen
def drawFPS(clock):
    fSize = getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)
    fps = clock.get_fps()
    drawText('FPS: %s'%(str(int(fps))),getFont(fSize[0]),windowSurface,0,0)
    return(str(int(fps)))

#draws writing on screen which states that the player's move is invalid(0 is an invalid move during player turn, 1 is during AI turn)
def drawInvalidMove(t,time):
    
    invRect = pygame.Rect(0,0,WINDOWWIDTH,getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)[0]*2)
    invRect.center = (WINDOWWIDTH/2,WINDOWHEIGHT/2)
    invSurf = pygame.Surface((invRect.width,invRect.height))
    invSurf.fill(BLACK)
    invSurf.set_alpha(175)
    if t == 0:
        #drawText('This is an invalid move',getFont(getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)[0]),text,text.get_width()/2,text.get_height()/2,True)
        text = 'This is an invalid move'
    elif t == 1:
        text = 'It is not your turn'
        #drawText('It is not your turn',getFont(getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)[0]),text,text.get_width()/2,text.get_height()/2,True)
    else:
        text = t
    tempSurf.add(text,invSurf,invRect,str(time))
    
#counts players and computer's points and draws result on screen
def countPoints(board,size,player):
    fSize = getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)
    #counts points
    pCount = 0
    aCount = 0
    for i in range(size):
        for j in range(size):
            if board[i+1][j+1] == player[0]:
                pCount += 1
            if board[i+1][j+1] == player[1]:
                aCount += 1
    return [pCount,aCount]

#Checks if given move is valid
def isValidMove(board, size, move, player):
    #if move is out of board bounds return false
    for i in move:
        if i > size or i < 1:
            return False
    #if occupied return false
    x,y = move[0],move[1]
    if not board[x][y] == ' ':
        return False
    #variable initialization
    posDir = []
    posFlip = []
    flip = []
    directions = [[1,0],[-1,0],[0,-1],[0,1],[1,-1],[-1,-1],[1,1],[-1,1]]
    opp = ''
    if player == 'B':
        opp = 'W'
    else:
        opp = 'B'

    #checks if move is adjacent to any opponents pieces and adds those pieces to possible valid moves
    for dx, dy in directions:
        newx = dx + x
        newy = dy + y
        if newx > 0 and newx < size + 1 and newy > 0 and newy < size + 1:
            if not board[newx][newy] == ' ':
                if not board[newx][newy] == player:
                    posDir.append([dx,dy])
    #checks each possibly valid direction whether it is valid. If valid adds to possible move list.
    for dx, dy in posDir:
        posFlip = []
        newx = x
        newy = y
        while True:
            newx += dx
            newy += dy
            if newx > 0 and newx < size+1 and newy > 0 and newy < size+1:
                if board[newx][newy] == ' ':
                    posFlip = []
                    break
                if board[newx][newy] == opp:
                    posFlip.append([newx,newy])
                if board[newx][newy] == player:
                    flip += posFlip
                    break
            else:
                break
    #if list of possible moves is empty, return false. Otherwise return pieces that the move would flip
    if bool(flip):
        return flip
    else:
        return False

#Gets a list of valid moves
def getValidMoves(board, size, player):
    validMoves = []
    for x in range(1,size+1):
        for y in range(1,size+1):
            if isValidMove(board, size, [x,y], player) != False:
                validMoves.append([x,y])
    return validMoves

#gets player's move
def getPlayerMove(board, size, player, black, white, wrong, mousePress):
    width = WINDOWHEIGHT - 200
    
    white = pygame.transform.scale(white,(int((width/size)*0.8),int((width/size)*0.8)))
    black = pygame.transform.scale(black,(int((width/size)*0.8),int((width/size)*0.8)))
    wrong = pygame.transform.scale(wrong,(int((width/size)*0.8),int((width/size)*0.8))) 
    wrongR = wrong.get_rect()

    if player[0] == 'B':
        piece = black
    else:piece = white
    
    pieceR = piece.get_rect()
    
    #when mouse is over an empty tile on the board, displays to the user whether that tile would be a valid move
    mx,my = pygame.mouse.get_pos()
    by = int((my-100)/(width/size))+1
    bx = int((mx - (WINDOWWIDTH - width)/2)/(width/size))+1
    if bx >= 1 and bx <= size and by >= 1 and by <= size:
        if board[bx][by] == ' ':
            centerX = (WINDOWWIDTH/2)-(width/2)+((width/size)/2)+((width/size)*(bx-1))
            centerY = (WINDOWHEIGHT/2)-(width/2)+((width/size)/2)+((width/size)*(by-1))
            if not bool(isValidMove(board,size,(bx,by),player)):
                wrongR.center = (centerX,centerY)
                windowSurface.blit(wrong,wrongR)
                if mousePress:
                    drawInvalidMove(0,1)
            else:
                pieceR.center = (centerX,centerY)
                windowSurface.blit(piece,pieceR)
                if mousePress:
                    return [bx,by]
                
      
    return False

#returns a board with the pieces flipped after a move is made
def flipPieces(board, pieces, move, player):
    for X,Y in pieces:
        if board[X][Y] == 'B':
            board[X][Y] = 'W'
        elif board[X][Y] == 'W':
            board[X][Y] = 'B'

    board[move[0]][move[1]] = player
    return board

#checks who is the winner and returns text to display
def checkWinner(board, player, outMoves = False):
    points = countPoints(board, GRIDSIZE, player)
    toReturn = []
    if outMoves:
        toReturn.append('There were no more possible moves!')
    if points[1] > points[0]:
        toReturn.append('You lost!')
    elif points[0] > points[1]:
        toReturn.append('Good job, you won!')
    elif points[0] == points[1]:
        toReturn.append('Whoops, it\'s a tie!')
    return toReturn

#gets AI move
def getAiMove(board, player):

    possibleMoves = getValidMoves(board,GRIDSIZE, player[1])

    random.shuffle(possibleMoves)

    for x,y in possibleMoves:
        if isOnCorner(x,y):
            return [x,y]
    
    bestScore = -1
    bestMove = []
    for x,y in possibleMoves:
        dupeBoard = copyBoard(board)
        flipPieces(dupeBoard, isValidMove(dupeBoard, GRIDSIZE,[x,y], player[1]), [x,y], player[1])
        score = countPoints(dupeBoard,GRIDSIZE,player)[1]
        if score > bestScore:
            bestMove = [x,y]
            bestScore = score
    return bestMove

#returns true if position is on the corner of the board
def isOnCorner(x,y):
    return (x == 1 and y == 1) or (x==GRIDSIZE and y == 1) or (x == 1 and y == GRIDSIZE) or (x == GRIDSIZE and y == GRIDSIZE)

#gives the image an alpha
def alphaImage(source,target,opacity):
    x = 0
    y = 0
    temp = pygame.Surface((source.get_width(),source.get_height())).convert()
    temp.blit(target,(-x,-y))
    temp.blit(source, (0,0))
    temp.set_alpha(opacity)
    return temp

#returns a copy of the board           
def copyBoard(board):
    board1 = copy.deepcopy(board)
    return board1

#initiate pygame and window 
pygame.init()
mainClock = pygame.time.Clock()
if FSCREEN:
    windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),pygame.FULLSCREEN)
else:
    windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption('Reversi Graphics')

#images
blackP = pygame.image.load('black.png')
whiteP = pygame.image.load('white.png')
wrongP = pygame.image.load('wrong.png')


#start screen
windowSurface.fill(BACKGROUND)
#images with alpha
blackA = alphaImage(blackP,windowSurface,200)
whiteA = alphaImage(whiteP,windowSurface,200)
wrongA = alphaImage(wrongP,windowSurface,200)

drawText('Reversi',getFont(60),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/10),True)
drawText('A game by prokopchukdim',getFont(30),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/10)+ 50,True)
drawText("Press 'Enter/Return' to play", getFont(45),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3),True)
drawText("Press 'i' for instructions",getFont(45),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+50,True)
drawText("Or press 'Escape' at any time to quit",getFont(45),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3)+100,True)
pygame.display.update()
menuInput(WINDOWHEIGHT,WINDOWWIDTH)

fSize = getMenuSize(WINDOWWIDTH,WINDOWHEIGHT)
    
#game loop
while True:

    #Initiate Game
    board = newBoard(GRIDSIZE)
    player = getPlayer(WINDOWWIDTH,WINDOWHEIGHT,blackP,whiteP)
    windowSurface.fill(BACKGROUND)
    winner = None

    #active keys
    mousePress = False
    enterPress = False

    turn = playerFirst()

    #displays to the user who will go first
    displayFirstTurn(turn)
    
    #draws starting board
    drawBoard(board,GRIDSIZE,whiteP,blackP)
    points = countPoints(board,GRIDSIZE,player)
    pygame.display.update()

    #creates a temporary surface which displays objects for a temporary amount of time
    tempSurf = tempSurfaces()


    fpsWait = 0
    fps = 0
    #play loop
    while True:
        
       
        #drawBoard(board,GRIDSIZE,whiteP,blackP)
        #drawPoints(points)
        #drawFPS(mainClock)

        #checks for user input
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN:
                    enterPress = True
            if event.type == MOUSEBUTTONUP:
                mousePress = True
                
                
        #code during user's turn
        if turn:
            drawBoard(board,GRIDSIZE,whiteP,blackP)

            drawText('It is your turn',getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,WINDOWHEIGHT-50,True)
            if len(getValidMoves(board, GRIDSIZE, player[0])) > 0:
                move = getPlayerMove(board, GRIDSIZE, player[0], blackA, whiteA, wrongA, mousePress)
                if bool(move):
                    board = flipPieces(board,isValidMove(board,GRIDSIZE,move,player[0]),move,player[0])
                    turn = not turn
                    points = countPoints(board,GRIDSIZE,player)

                    drawBoard(board,GRIDSIZE,whiteP,blackP)
            else:
                winner = checkWinner(board,player,True)
                break

        #code during AI turn
        else:
            drawText('It is the computer\'s turn',getFont(fSize[0]),windowSurface,WINDOWWIDTH/2,WINDOWHEIGHT-50,True)
            text = 'Press Enter/Return to see the computer\'s move'
            drawInvalidMove(text,'inf')
            if enterPress:
                drawBoard(board,GRIDSIZE,whiteP,blackP)
                if len(getValidMoves(board, GRIDSIZE, player[1])) > 0:
                    move = getAiMove(board, player)    
                    board = flipPieces(board, isValidMove(board,GRIDSIZE,move,player[1]), move, player[1])
                    turn = not turn
                    tempSurf.delete(text)
                    points = countPoints(board,GRIDSIZE,player)
                else:
                    winner = checkWinner(board,player,True)
                    break

        #end of frame variables and functions
        mousePress = False
        enterPress = False
        tempSurf.display()

    
        if fpsWait >= 30:
            fps = drawFPS(mainClock)
            fpsWait = 0
        fpsWait+=1
        fpsSurface = pygame.Surface((200,200))
        fpsSurface.fill(BACKGROUND)

        
        drawText('FPS: %s'%(fps),getFont(fSize[0]),fpsSurface,0,0)
        windowSurface.blit(fpsSurface,pygame.Rect(0,0,200,200))
        
        pygame.display.update()
        
        mainClock.tick()
        
    #displays ending screen
    windowSurface.fill(BACKGROUND)
    print('1')
    drawText('Reversi',getFont(60),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/10),True)
    print('2')
    drawText('A game by prokopchukdim',getFont(30),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/10)+ 50,True)
    print('3')
    for i in range(len(winner)):
        drawText(winner[i], getFont(fSize[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3) + 50*i,True)
    drawText('You finished with %s points'%(countPoints(board,GRIDSIZE,player)[0]), getFont(fSize[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3) + (50 * (len(winner)+1)),True)
    drawText('The computer finished with %s points'%(countPoints(board,GRIDSIZE,player)[1]), getFont(fSize[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3) + (50 * (len(winner)+2)),True)
    drawText("Press Enter/Return to play again",getFont(fSize[0]),windowSurface,(WINDOWWIDTH/2),(WINDOWHEIGHT/3) + (50 * (len(winner)+3)),True)
    pygame.display.update()
    inLoop = True
    while inLoop:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN:
                    inLoop = False
       
