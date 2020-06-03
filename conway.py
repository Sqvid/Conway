#!/usr/bin/env python
import curses
from time import sleep
from copy import deepcopy

def drawBoard(boardWin, boardData, cursPosY, cursPosX):
    boardHeight, boardWidth = boardWin.getmaxyx()
    boardWin.box()

    for row in range(1, boardHeight - 1):
        for col in range(1, boardWidth - 2, 2):
            if boardData[row - 1][col // 2] == 1:
                boardWin.addstr(row, col, "  ", curses.color_pair(4))

            elif row == cursPosY and col == cursPosX:
                boardWin.addstr(row, col, "  ", curses.color_pair(3))

            elif row % 2 != 0:
                if (col - 1) % 4 == 0:
                    boardWin.addstr(row, col, "  ", curses.color_pair(1))

                else:
                    boardWin.addstr(row, col, "  ", curses.color_pair(2))

            else:
                if (col - 1) % 4 != 0:
                    boardWin.addstr(row, col, "  ", curses.color_pair(1))

                else:
                    boardWin.addstr(row, col, "  ", curses.color_pair(2))

    boardWin.move(cursPosY, cursPosX)

def isLiveCell(boardData, row, col):
    if row >= 0 and row < len(boardData):
        if col >= 0 and col < len(boardData[row]):
            return boardData[row][col]
        else:
            return 0
    else:
        return 0

def checkNeighbours(boardData, row, col):
    count = 0
    directionList = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1],
            [1, 0], [1, -1]]

    for direction in directionList:
        count = count + isLiveCell(boardData, row + direction[0], col +
                direction[1])

    return count
        

def runConway(boardData):
    newBoardData = deepcopy(boardData)

    for row in range(len(boardData)):
        for col in range(len(boardData[row])):
            liveCount = checkNeighbours(boardData, row, col)

            # Current cell is alive.
            if boardData[row][col] == 1:
                if liveCount != 2 and liveCount != 3:
                    newBoardData[row][col] = 0
            else:
                if liveCount == 3:
                    newBoardData[row][col] = 1

    return newBoardData

def main(stdscr):
    if curses.has_colors() == False:
        print("Error: Terminal does not support colours.")
        return -1

    curses.curs_set(0)
    curses.use_default_colors()
    # Checkered board colors.
    curses.init_pair(1, -1, curses.COLOR_WHITE)
    curses.init_pair(2, -1, 240)
    # Selected cell colour.
    curses.init_pair(3, -1, 52)
    # Live cell colour.
    curses.init_pair(4, -1, 34)

    scrHeight, scrWidth = stdscr.getmaxyx()
    stdscr.refresh()
    
    # Initialise the board window.
    boardHeight = round(0.8 * scrHeight)
    boardWidth = round(0.8 * scrWidth)
    boardOriginX = round((scrWidth - boardWidth) / 2)
    boardOriginY = round((scrHeight - boardHeight) / 2) - 1
    boardWin = curses.newwin(boardHeight, boardWidth, boardOriginY, boardOriginX)

    # Initialise board data.
    boardData = []

    for _ in range(boardHeight - 2):
        boardRow = [0] * ((boardWidth - 2) // 2)
        boardData.append(boardRow)

    drawBoard(boardWin, boardData, 1, 1)
    boardWin.refresh()

    # Keyboard control.
    while True:
        key = boardWin.getch()
        posY, posX = boardWin.getyx()

        if key == ord('q'):
            break

        elif key == ord('h'):
            if posX > 2:
                posX -= 2

        elif key == ord('l'):
            if posX < boardWidth - 3:
                posX += 2

        elif key == ord('j'):
            if posY < boardHeight - 2:
                posY += 1

        elif key == ord('k'):
            if posY > 1:
                posY -= 1

        elif key == ord(' '):
            boardData[posY - 1][posX // 2] = 1

        elif key == ord('r'):
            while True:
                boardData = runConway(boardData)
                drawBoard(boardWin, boardData, 1, 1)
                boardWin.refresh()

                sleep(0.1)

        drawBoard(boardWin, boardData, posY, posX)
        boardWin.refresh()
        
curses.wrapper(main)
