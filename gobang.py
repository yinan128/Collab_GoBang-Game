from cmu_112_graphics import *
import time

def appStarted(app):
    app.rows = 10
    app.cols = 10
    app.margin = 10
    app.textSpace = 40
    app.winner = ""
    app.dotX = -1
    app.dotY = -1
    app.listWhite = []
    app.listBlack = []
    app.listToCheck = []
    app.isWhite = False
    app.gameOver = False
    app.AIMode = False
    app.startTime = 0
    app.currentTime = 5

def timerFired(app):
    app.currentTime = time.time()

def reset(app):
    app.rows = 10
    app.cols = 10
    app.margin = 10
    app.textSpace = 40
    app.winner = ""
    app.dotX = -1
    app.dotY = -1
    app.listWhite = []
    app.listBlack = []
    app.listToCheck = []
    app.isWhite = False
    app.gameOver = False
    app.AIMode = False

def mousePressed(app,event):
    if not app.gameOver:
        app.dotX = event.x
        app.dotY = event.y
        row, col = getCell(app, event.x, event.y)
        if ((0 <= row <= app.rows and 0 <= col <= app.cols)
                and ((row,col) not in app.listWhite)
                and ((row,col) not in app.listBlack)):
            if not app.AIMode:
                if app.isWhite:
                    app.listWhite.append((row,col))
                    if scorer(app, app.listWhite):
                        app.winner = "White"
                        app.gameOver = True
                else:
                    app.listBlack.append((row,col))
                    if scorer(app, app.listBlack):
                        app.winner = "Black"
                        app.gameOver = True
                app.isWhite = not app.isWhite
            else:
                app.listBlack.append((row, col))
                AIModifyWhite(app, row, col)
                if scorer(app, app.listBlack):
                    app.winner = "YOU"
                    app.gameOver = True
                if scorer(app, app.listWhite):
                    app.winner = "AI"
                    app.gameOver = True

def scorerBlack(app, listToCheck):
    # input = virtualBlackList
    for item in listToCheck:
        (row, col) = item
        for i in range(col-3, col+1):
            if 0 <= i < app.cols - 3:
                win = True
                for j in range(4):
                    if (row, i+j) not in listToCheck:
                        win = False
                if win:
                    return True
        # row
        for i in range(row-3, row+1):
            if 0 <= i < app.rows - 3:
                win = True
                for j in range(4):
                    if (i+j, col) not in listToCheck:
                        win = False
                if win:
                    return True
        # diag lefttop-rightbottom
        for i in range(4):
            if 3 <= row + i < app.rows and 3 <= col + i < app.cols:
                win = True
                for j in range(4):
                    if (row + i - j, col + i - j) not in listToCheck:
                        win = False
                if win:
                    return True
        # diag righttop-leftbottom
        for i in range(4):
            if 0 <= row - i < app.rows - 3 and 3 <= col + i < app.cols:
                win = True
                for j in range(4):
                    if (row - i + j, col + i - j) not in listToCheck:
                        win = False
                if win:
                    return True
        return False

def AIModifyWhite(app, row, col):
    AIrow, AIcol = -1, -1
    # selection based on 4 consecutive black
    for i in range(app.rows):
        for j in range(app.cols):
            virtualBlackList = app.listBlack[:]
            if ((i,j) not in app.listWhite
                    and (i,j) not in app.listBlack):
                virtualBlackList.append((i,j))
                if scorerBlack(app, virtualBlackList):
                    AIrow, AIcol = i, j
                    break
        if AIrow != -1 and AIcol != -1:
            break
    if AIrow == -1 and AIcol == -1:
        # selection within 3x3 grid
        for i in range(row-1,row+2):
            for j in range(col-1,col+2):
                if ((i, j) not in app.listWhite
                        and (i, j) not in app.listBlack):
                    if 0<=i<app.rows and 0<=j<app.cols:
                        AIrow, AIcol = i, j
        if AIrow == -1 and AIcol == -1:
        # random selection
            for i in range(app.rows):
                for j in range(app.cols):
                    if ((i, j) not in app.listWhite
                            and (i, j) not in app.listBlack):
                        AIrow, AIcol = i, j
                        break
                if AIrow != -1 and AIcol != -1:
                    break
    app.listWhite.append((AIrow, AIcol))

def keyPressed(app,event):
    if event.key == "r":
        reset(app)
    elif event.key == "i":
        reset(app)
        app.AIMode = True
        app.startTime = time.time()

def scorer(app, listToCheck):
    for item in listToCheck:
        (row, col) = item
        # col
        for i in range(col-4, col+1):
            if 0 <= i < app.cols - 4:
                win = True
                for j in range(5):
                    if (row, i+j) not in listToCheck:
                        win = False
                if win:
                    return True
        # row
        for i in range(row-4, row+1):
            if 0 <= i < app.rows - 4:
                win = True
                for j in range(5):
                    if (i+j, col) not in listToCheck:
                        win = False
                if win:
                    return True
        # diag lefttop-rightbottom
        for i in range(5):
            if 4 <= row + i < app.rows and 4 <= col + i < app.cols:
                win = True
                for j in range(5):
                    if (row + i - j, col + i - j) not in listToCheck:
                        win = False
                if win:
                    return True
        # diag righttop-leftbottom
        for i in range(5):
            if 0 <= row - i < app.rows - 4 and 4 <= col + i < app.cols:
                win = True
                for j in range(5):
                    if (row - i + j, col + i - j) not in listToCheck:
                        win = False
                if win:
                    return True
    return False

def getCell(app, x, y):
    gridWidth = app.width - 2 * app.margin
    gridHeight = app.height - app.margin - app.textSpace
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    col = int((x - app.margin) // cellWidth)
    row = int((y - app.textSpace) // cellHeight)
    return row, col

def getCellBound(app, row, col):
    gridWidth = app.width - 2*app.margin
    gridHeight = app.height - app.margin - app.textSpace
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = cellWidth * col + app.margin
    y0 = cellHeight * row + app.textSpace
    x1 = cellWidth * (col+1) + app.margin
    y1 = cellHeight * (row+1) + app.textSpace
    return x0,y0,x1,y1

def drawGrid(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0,y0,x1,y1 = getCellBound(app, row, col)
            canvas.create_rectangle(x0,y0,x1,y1)

def drawText(app,canvas):
    font = "Arial 16 bold"
    canvas.create_text(app.width/2, 20,
                       text = "GoBang Game", font = font)
    if app.winner != "":
        canvas.create_text(app.width / 2, app.height / 2,
                           text=f'Winner:{app.winner}', font="Arial 50 bold", fill="red")

    if app.currentTime - app.startTime < 3:
        canvas.create_text(20, app.height - 20, anchor="sw",
                           text="AI mode Activated", font="Arial 20", fill="red")

def drawDot(app,canvas):
    if app.listWhite != 0:
        for item in app.listWhite:
            (row, col) = item
            x0,y0,x1,y1 = getCellBound(app,row,col)
            canvas.create_oval(x0+app.margin/2,y0+app.margin/2,
                               x1-app.margin/2,y1-app.margin/2,
                               fill="white")
    if app.listBlack != 0:
        for item in app.listBlack:
            (row, col) = item
            x0,y0,x1,y1 = getCellBound(app,row,col)
            canvas.create_oval(x0 + app.margin / 2, y0 + app.margin / 2,
                               x1 - app.margin / 2, y1 - app.margin / 2,
                               fill="black")

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    drawDot(app, canvas)
    drawText(app, canvas)

runApp(width=520, height=550)