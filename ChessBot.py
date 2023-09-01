import pygame as p

class Board:
    def __init__(self, start):
        self.Grid = [[0 for i in range(8)] for j in range(8)]
        self.PieceValue = [1, 3, 3, 5, 9, 15]
        self.PieceToNum = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6}
        self.NumToPiece = ["-", "P", "N", "B", "R", "Q", "K"]
        self.PieceHeuristics = [0, 0, 2, 2, 1, 2, -5]
        self.PieceLocations = [[], []]
        self.fen_str(start)  # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
        self.Vectors = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.PiecesVectors = {1: [], 2: [], 3: [1, 3, 5, 7], 4: [0, 2, 4, 6], 5: [i for i in range(8)],
                              6: [i for i in range(8)]}
        self.LinesOfAttack = [[], []]
        self.counter = 0

        pawn = [[0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        knight = [[-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 0, 0, 0, -20, -40],
                  [-30, 0, 10, 15, 15, 10, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30],
                  [-30, 5, 10, 15, 15, 10, 5, -30], [-40, -20, 0, 5, 5, 0, -20, -40],
                  [-50, -40, -30, -30, -30, -30, -40, -50]]
        bishop = [[-20, -10, -10, -10, -10, -10, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10],
                  [-10, 0, 5, 10, 10, 5, 0, -10],
                  [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 10, 10, 10, 10, 0, -10], [-10, 10, 10, 10, 10, 10, 10, -10],
                  [-10, 5, 0, 0, 0, 0, 5, -10], [-20, -10, -10, -10, -10, -10, -10, -20]]
        rook = [[0, 0, 0, 0, 0, 0, 0, 0], [5, 10, 10, 10, 10, 10, 10, 5], [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5], [0, 0, 0, 5, 5, 0, 0, 0]]
        queen = [[-20, -10, -10, -5, -5, -10, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-10, 0, 5, 5, 5, 5, 0, -10],
                 [-5, 0, 5, 5, 5, 5, 0, -5], [0, 0, 5, 5, 5, 5, 0, -5], [-10, 5, 5, 5, 5, 5, 0, -10],
                 [-10, 0, 5, 0, 0, 0, 0, -10], [-20, -10, -10, -5, -5, -10, -10, -20]]
        kingMiddleGame = [[-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-20, -30, -30, -40, -40, -30, -30, -20], [-10, -20, -20, -20, -20, -20, -20, -10],
                          [20, 20, 0, 0, 0, 0, 20, 20], [20, 30, 10, 0, 0, 10, 30, 20]]
        self.KingEndGame = [[-50, -40, -30, -20, -20, -30, -40, -50], [-30, -20, -10, 0, 0, -10, -20, -30],
                            [-30, -10, 20, 30, 30, 20, -10, -30], [-30, -10, 30, 40, 40, 30, -10, -30],
                            [-30, -10, 30, 40, 40, 30, -10, -30], [-30, -10, 20, 30, 30, 20, -10, -30],
                            [-30, -30, 0, 0, 0, 0, -30, -30], [-50, -30, -30, -30, -30, -30, -30, -50]]
        self.optimalLocations = [
            [list(reversed(pawn)), list(reversed(knight)), list(reversed(bishop)), list(reversed(rook)),
             list(reversed(queen)), list(reversed(kingMiddleGame))],
            [pawn, knight, bishop, rook, queen, kingMiddleGame]]

        self.width, self.height = 512, 512
        self.squareSize = self.width // 8
        # self.Grid = board
        # self.PieceLocations = pieceLocations

        self.images = {}
        for colour in [0, 8]:
            for i in range(1, 7):
                piece = colour + i
                self.images[piece] = p.transform.scale((p.image.load("images/" + str(piece) + ".png")),
                                                       (self.squareSize, self.squareSize))

    # Start of the foundation functions
    def vec_add(self, v1, v2, scale=1):
        return v1[0] + scale * v2[0], v1[1] + scale * v2[1]

    def vec_sub(self, v1, v2):
        return v2[0] - v1[0], v2[1] - v1[1]

    def vec_div(self, v1, v2):  # v1 is bigger than v2
        if v2[0] == 0:
            if v1[0] == 0:
                res = v1[1] / v2[1]
                if res == int(res): return int(res)
        else:
            scale = v1[0] / v2[0]
            if scale == int(scale):
                if v2[1] * scale == v1[1]: return int(scale)
        return - 1

    def fen_str(self, inp):
        r, c, ind = 0, 0, 0
        while ind < len(inp):
            if inp[ind].isalpha():
                num = 8 if inp[ind].isupper() else 0
                num |= self.PieceToNum[inp[ind].upper()]
                self.Grid[r][c] = num
                c += 1
            elif inp[ind].isnumeric():
                c += int(inp[ind])
            else:
                r, c = r + 1, 0
            ind += 1

        for i in range(8):
            for j in range(8):
                if self.Grid[i][j] != 0:
                    if self.Grid[i][j] & 8 == 8:
                        self.PieceLocations[1].append((i, j))
                    else:
                        self.PieceLocations[0].append((i, j))

        self.output()

    def readMove(self):
        inp = input()
        org = self.alnum_to_coordinates(inp[:2])
        coords = self.alnum_to_coordinates(inp[-2:])
        pieceNumber = self.Grid[org[0]][org[1]] & 7
        if pieceNumber == 6 and ((org == (0, 4) and (coords == (0, 6) or coords == (0, 2))) or (
                org == (7, 4) and (coords == (7, 6) or coords == (7, 2)))):
            self.PieceLocations, self.Grid = self.move(org, coords, self.PieceLocations, self.Grid)
            res = self.vec_sub(coords, org)[1]
            if res > 0:  # queen
                orgRook = coords[0], 0
                newRook = coords[0], 3
            else:  # king
                orgRook = coords[0], 7
                newRook = coords[0], 5
            self.PieceLocations, self.Grid = self.move(orgRook, newRook, self.PieceLocations, self.Grid)
        else:
            self.PieceLocations, self.Grid = self.move(org, coords, self.PieceLocations, self.Grid)
        self.output()

    def alnum_to_coordinates(self, str1):
        return int(8 - int(str1[1])), int(ord(str1[0]) - 97)

    def coordinates_to_alnum(self, coords):
        return chr(65 + coords[1]) + str(8 - coords[0])

    def output(self, grid=None):
        if grid is None: grid = self.Grid
        for row in grid:
            for item in row:
                char = self.NumToPiece[item & 7]
                if not item & 8: char = char.lower()
                print(char, end=" ")
            print("\n".strip())
        print("**********")

    def move(self, p1, p2, pieceLocations, GridCopy):
        num = GridCopy[p1[0]][p1[1]]
        colour = (GridCopy[p1[0]][p1[1]] & 8) // 8
        GridCopy[p1[0]][p1[1]] = 0

        if (num & 7 == 1) and ((p2[0] == 0 and colour == 1) or (p2[0] == 7 and colour == 0)):
            GridCopy[p2[0]][p2[1]] = 5 + colour * 8
        else:
            GridCopy[p2[0]][p2[1]] = num

        if p2 in pieceLocations[1 - colour]: pieceLocations[1 - colour].remove(p2)

        pieceLocations[colour].remove(p1)
        pieceLocations[colour].append(p2)

        if num & 7 == 6 and (p2[1] - p1[1] == 2 or p1[1] - p2[1] == 2):
            if p2[1] > p1[1]:
                newp1 = (colour * 7, 7)
                newp2 = (colour * 7, 5)
            else:
                newp1 = (colour * 7, 0)
                newp2 = (colour * 7, 3)
            pieceLocations, GridCopy = self.move(newp1, newp2, pieceLocations, GridCopy)

        return pieceLocations, GridCopy

    # end of the foundation functions

    # start of UI functions
    def drawGrid(self, screen):
        self.drawSquares(screen)
        self.drawPieces(screen)

    def drawSquares(self, screen):
        colours = [p.Color("burlywood"), p.Color("chocolate4")]
        for r in range(8):
            for c in range(8):
                color = colours[(r + c) % 2]
                p.draw.rect(screen, color,
                            p.Rect(c * self.squareSize, r * self.squareSize, self.squareSize, self.squareSize))

    def drawPieces(self, screen):
        for r in range(8):
            for c in range(8):
                if self.Grid[r][c] != 0:
                    piece = self.Grid[r][c]
                    screen.blit(self.images[piece],
                                p.Rect(c * self.squareSize, r * self.squareSize, self.squareSize, self.squareSize))

    def drawEndGameText(self, screen, text):
        font = p.font.SysFont("Arial", 64, True, False)
        line = font.render(text, False, p.Color("Green"))
        loc = p.Rect(0, 0, self.width, self.height).move(self.width / 2 - line.get_width() / 2,
                                                         self.height / 2 - line.get_height() / 2)
        screen.blit(line, loc)
        line = font.render(text, False, p.Color('Green'))
        screen.blit(line, loc.move(2, 2))
    # end of UI functions

    # start of Legal Move functions
    def returnPossibleMoves(self, coordinates, board):
        pieceNumber = board[coordinates[0]][coordinates[1]] & 7
        colour = board[coordinates[0]][coordinates[1]] & 8
        possible = []
        if pieceNumber == 0: return []
        if pieceNumber == 1:
            if colour == 0:
                moving = [self.Vectors[4]]
                capturing = [self.Vectors[3], self.Vectors[5]]
            else:
                moving = [self.Vectors[0]]
                capturing = [self.Vectors[1], self.Vectors[7]]
            if (coordinates[0] == 1 and colour == 0) or (coordinates[0] == 6 and colour == 8):
                res = self.vec_add(coordinates, moving[0])
                if board[res[0]][res[1]] == 0:
                    coords = moving[0]
                    moving.append((coords[0] * 2, coords[1] * 2))
            moving = [self.vec_add(coordinates, vec) for vec in moving]
            moving = [vec for vec in moving if (0 <= vec[0] <= 7 and 0 <= vec[1] <= 7)]
            capturing = [self.vec_add(coordinates, vec) for vec in capturing]
            capturing = [vec for vec in capturing if 0 <= vec[0] <= 7 and 0 <= vec[1] <= 7]
            for vec in capturing:
                if board[vec[0]][vec[1]] != 0 and ((board[vec[0]][vec[1]] & 8) != colour):
                    possible.append(vec)

            for vec in moving:
                if board[vec[0]][vec[1]] == 0:
                    possible.append(vec)
        elif pieceNumber == 2:
            for n1 in [-1, 1]:
                for n2 in [-2, 2]:
                    positions = [self.vec_add(coordinates, (n1, n2)), self.vec_add(coordinates, (n2, n1))]
                    for new in positions:
                        if 0 <= new[0] <= 7 and 0 <= new[1] <= 7 and (
                                (board[new[0]][new[1]] & 8) != colour or board[new[0]][new[1]] == 0): possible.append(
                            new)
        else:
            allDirections = [self.Vectors[el] for el in self.PiecesVectors[pieceNumber]]
            for dir in allDirections:
                scale = 1
                done = False
                while not done:
                    new = self.vec_add(coordinates, dir, scale)
                    if 0 <= new[0] <= 7 and 0 <= new[1] <= 7 and (
                            board[new[0]][new[1]] == 0 or (board[new[0]][new[1]] & 8) != colour):
                        possible.append(new)
                        scale += 1
                        if pieceNumber == 6: done = True
                        if board[new[0]][new[1]] & 8 != colour and board[new[0]][new[1]] != 0: done = True
                    else:
                        done = True

        return possible

    def castle(self, col, direction, board, pieceLocations):
        colour = col // 8
        kingPos = (colour * 7, 4)
        CastleThroughCheck = False

        if direction == "K":  # ie kingside
            rookPos = (kingPos[0], 7)
            positions = [(colour * 7, 4), (colour * 7, 5), (colour * 7, 6)]
        else:
            rookPos = (kingPos[0], 0)
            positions = [(colour * 7, 4), (colour * 7, 3), (colour * 7, 2)]

        for pos in positions:
            res = self.isKingInCheck(pos, board, pieceLocations)
            if not res and (board[pos[0]][pos[1]] and pos != kingPos): # checks if square is empty or not as long as square isn't king's original position
                self.output(board)
                CastleThroughCheck = True
                break

        return (board[rookPos[0]][rookPos[1]] == col + 4 and board[kingPos[0]][
            kingPos[1]] == col + 6) and not CastleThroughCheck

    def legalMoves(self, coordinates, kingInfo, isPinned, allowed, board):
        possible = self.returnPossibleMoves(coordinates, board)
        isCheck, isDoubleCheck, AttackSquare = kingInfo
        if AttackSquare:
            if isDoubleCheck:
                if board[coordinates[0]][coordinates[1]] & 7 != 6:
                    return []

            if isPinned:
                possible = [pos for pos in possible if pos == AttackSquare]
            else:
                if isCheck:
                    possible = [pos for pos in possible if pos in allowed]
        return possible

    def isKingInCheck(self, coordinates, grid, pieceLocations):
        colour = (grid[coordinates[0]][coordinates[1]] & 8) // 8
        opponentsPieces = pieceLocations[1 - colour]
        myPieces = pieceLocations[colour]
        allPieces = opponentsPieces[:]
        allPieces.extend(pieceLocations[colour])
        attack = []
        attackSquare = ()
        pinnedPiece = ()

        for piece in opponentsPieces:
            pieceNumber = grid[piece[0]][piece[1]] & 7
            direction = self.vec_sub(piece, coordinates)

            if not (direction[0] == direction[1] or direction[0] == - direction[1] or direction[0] == 0 or
                    direction[1] == 0 or pieceNumber == 2): continue

            if pieceNumber == 1 and ((colour == 1 and (direction == (1, 1) or direction == (1, -1))) or (
                    colour == 0 and (direction == (-1, 1) or direction == (-1, -1)))):
                attack.append(1)  # since this colour is for the opponent's pawns
                attackSquare = piece

            elif pieceNumber == 2 and (
                    (abs(direction[0]), abs(direction[1])) == (1, 2) or (abs(direction[0]), abs(direction[1])) == (
                    2, 1)):
                attack.append(2)
                attackSquare = piece

            elif (pieceNumber == 3 or pieceNumber == 5) and abs(direction[0]) == abs(direction[1]):
                scale = abs(direction[0])
                vec = (direction[0] // scale, direction[1] // scale)
                start = piece
                valid = True
                obstacles = []
                while valid:
                    start = self.vec_add(start, vec)
                    if start in myPieces: obstacles.append(start)
                    if (start[0] > 8 or start[0] < 0) or start in opponentsPieces or start == coordinates:
                        if start == coordinates: break
                        valid = False
                if valid and len(obstacles) == 1 and coordinates in obstacles:
                    attack.append(pieceNumber)
                    attackSquare = piece

                if len(obstacles) == 2:
                    pinnedPiece = obstacles[0]
                    attackSquare = piece

            if (pieceNumber == 4 or pieceNumber == 5) and (direction[0] == 0 or direction[1] == 0):
                if direction[0] == 0:
                    if direction[1] > 0:
                        vec = (0, 1)
                    else:
                        vec = (0, -1)
                else:
                    if direction[0] > 0:
                        vec = (1, 0)
                    else:
                        vec = (-1, 0)
                start = piece
                valid = True
                obstacles = []
                while valid:
                    start = self.vec_add(start, vec)
                    if start in myPieces: obstacles.append(start)
                    if start[0] > 8 or start[0] < 0 or start[1] > 8 or start[
                        1] < 0 or start in opponentsPieces or start == coordinates:
                        if start == coordinates: break
                        valid = False
                if valid and len(obstacles) == 1 and coordinates in obstacles:
                    attack.append(pieceNumber)
                    attackSquare = piece

                if len(obstacles) == 2:
                    pinnedPiece = obstacles[0]
                    attackSquare = piece

        return len(attack) >= 1, len(attack) >= 2, attackSquare, pinnedPiece

    def legalKingMoves(self, kingLoc, board, pieceLocations):

        possible = []
        colour = board[kingLoc[0]][kingLoc[1]] & 8
        attackSquare = ()

        for dir in ["K", "Q"]:
            newKingPos = (colour // 8 * 7, 6 if dir == "K" else 2)
            if self.castle(colour, dir, board, pieceLocations):
                possible.append(newKingPos)

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= kingLoc[0] + i <= 7 and 0 <= kingLoc[1] + j <= 7:
                    if board[kingLoc[0] + i][kingLoc[1] + j] == 0 or (
                            board[kingLoc[0] + i][kingLoc[1] + j] & 8 != colour) or (i == 0 and j == 0):
                        possible.append((kingLoc[0] + i, kingLoc[1] + j))

        valid = []

        for endCoords in possible:
            copy = [row[:] for row in board]
            pieceLocationsCopy = [row[:] for row in pieceLocations]
            pieceLocationsCopy, copy = self.move(kingLoc, endCoords, pieceLocationsCopy, copy)

            res, res1, squ, piece = self.isKingInCheck(endCoords, copy, pieceLocationsCopy)

            if not res:
                valid.append(endCoords)

            if endCoords == kingLoc:
                pinnedPiece = piece
                isCheck = res
                isDoubleCheck = res1
                attackSquare = squ

        if kingLoc in valid: valid.remove(kingLoc)

        return (isCheck, isDoubleCheck, attackSquare, pinnedPiece), valid

    def isCheckMate(self, board, pieceLocations, colour):
        pinned = []

        for coords in pieceLocations[colour]:
            if board[coords[0]][coords[1]] & 7 == 6:
                kingLoc = coords
                info, possible = self.legalKingMoves(coords, board, pieceLocations)
                isCheck, isDoubleCheck, attackSquare, pinnedPiece = info
                pinned.append(pinnedPiece)
                # pass to legal moves, isCheck and square which check coming from
                break

        if isCheck:
            allowed = []
            vec1 = self.vec_sub(attackSquare, kingLoc)
            piece = board[attackSquare[0]][attackSquare[1]] & 7
            if piece <= 2:
                allowed.append(attackSquare)
            else:
                for i in self.PiecesVectors[piece]:
                    vec = self.Vectors[i]
                    if self.vec_div(vec1, vec) > 0:
                        scale = self.vec_div(vec1, vec)
                        vec2 = vec
                        break
                for i in range(scale):
                    allowed.append(self.vec_add(attackSquare, vec2, i))
            for vector in allowed:
                canSquareBeAttacked = self.isUnderSevereAttack(vector, board, pieceLocations)  # ie the piece of the same colour as king can move to that square
                if canSquareBeAttacked: return False

        return isCheck and len(possible) == 0

    def allPossibleMoves(self, board, pieceLocations, colour):
        moves = {}
        pinned = []
        allowed = []

        for coords in pieceLocations[colour]:
            if board[coords[0]][coords[1]] & 7 == 6:
                kingLoc = coords
                info, possible = self.legalKingMoves(coords, board, pieceLocations)
                isCheck, isDoubleCheck, attackSquare, pinnedPiece = info
                pinned.append(pinnedPiece)
                kingInfo = (isCheck, isDoubleCheck, attackSquare)
                moves[coords] = possible
                # pass to legal moves, isCheck and square which check coming from
                break

        try:
            if isCheck:
                vec1 = self.vec_sub(attackSquare, kingLoc)
                piece = board[attackSquare[0]][attackSquare[1]] & 7
                if piece <= 2:
                    allowed.append(attackSquare)
                else:
                    for i in self.PiecesVectors[piece]:
                        vec = self.Vectors[i]
                        if self.vec_div(vec1, vec) > 0:
                            scale = self.vec_div(vec1, vec)
                            vec2 = vec
                            break
                    for i in range(scale + 1):
                        allowed.append(self.vec_add(attackSquare, vec2, i))

            for coords in pieceLocations[colour]:
                if board[coords[0]][coords[1]] & 7 != 6:
                    possible = self.legalMoves(coords, kingInfo, coords in pinned, allowed, board)
                    moves[coords] = possible
        except:
            pass
        return moves

    # end of Legal Move functions

    # start of evaluation functions
    def evaluation(self, board):
        weight = [0, 0]
        eval = 0
        HalfOpenFile = 20
        OpenFile = 40
        DoubledPawns = 20
        countByColour = [[0, 0] for i in range(8)]

        for i in range(8):
            countP = [0, 0]
            rookPresent = [False, False]
            for j in range(8):
                if board[i][j] & 7 != 0:
                    pieceNumber = board[i][j] & 7
                    colour = (board[i][j] & 8) // 8

                    weight[colour] += self.PieceValue[pieceNumber - 1] * 100
                    weight[colour] += self.optimalLocations[colour][pieceNumber - 1][i][j] * self.PieceValue[
                        pieceNumber - 1] * 0.2

                    if pieceNumber == 4:
                        rookPresent[colour] = True

                    if pieceNumber == 1:
                        countByColour[i][colour] += 1
                        countP[colour] += 1

            for k in range(2):
                if countP[k] == 2 or countP[k] == 3:
                    weight[k] -= DoubledPawns * (countP[k] - 1)

                if rookPresent[k]:
                    if sum(countP) == 1:
                        weight[k] += HalfOpenFile
                    elif sum(countP) == 0:
                        weight[k] += OpenFile

        eval -= weight[0] / 100
        eval += weight[1] / 100

        return round(eval, 3)

    def isUnderSevereAttack(self, coordinates, grid, pieceLocations):
        colour = (grid[coordinates[0]][coordinates[1]] & 8) // 8
        thisPieceNumber = grid[coordinates[0]][coordinates[1]] & 7
        opponentsPieces = pieceLocations[1 - colour]
        allPieces = opponentsPieces[:]
        allPieces.extend(pieceLocations[colour])
        attack = [float("inf")]

        for piece in opponentsPieces:
            pieceNumber = grid[piece[0]][piece[1]] & 7
            direction = self.vec_sub(piece, coordinates)

            if not (direction[0] == direction[1] or direction[0] == - direction[1] or direction[0] == 0 or
                    direction[1] == 0) or pieceNumber == 2: continue

            if pieceNumber == 1 and (colour == 1 and (direction == (1, 1) or direction == (1, -1))) or (
                    colour == 0 and (direction == (-1, 1) or direction == (-1, -1))):
                attack.append(1)  # since this colour is for the opponent's pawns
                break
            elif pieceNumber == 2 and (
                    (abs(direction[0]), abs(direction[1])) == [1, 2] or (abs(direction[0]), abs(direction[1])) == [
                2, 1]):
                attack.append(2)
                break
            elif (pieceNumber == 3 or pieceNumber == 5) and abs(direction[0]) == abs(direction[1]):
                scale = abs(direction[0])
                vec = (direction[0] // scale, direction[1] // scale)
                start = piece
                valid = True
                while valid:
                    start = self.vec_add(start, vec)
                    if start in allPieces or start[0] > 8 or start[0] < 0:
                        if start == coordinates: break
                        valid = False
                if valid: attack.append(pieceNumber)
            if (pieceNumber == 4 or pieceNumber == 5) and (direction[0] == 0 or direction[1] == 0):
                if direction[0] == 0:
                    if direction[1] > 0:
                        vec = (0, 1)
                    else:
                        vec = (0, -1)
                else:
                    if direction[0] > 0:
                        vec = (1, 0)
                    else:
                        vec = (-1, 0)
                start = piece
                valid = True
                while valid:
                    start = self.vec_add(start, vec)
                    if start in allPieces or start[0] > 8 or start[0] < 0 or start[1] > 8 or start[1] < 0:
                        if start == coordinates: break
                        valid = False
                if valid: attack.append(pieceNumber)

        return thisPieceNumber > min(attack) or len(attack) >= 2

    # end of evaluation functions

    # start of core functions
    def isMiddleGame(self, board, pieceLocations):
        totalPieceValue = [0, 0]
        isQueen = [False, False]

        for c in range(2):
            for piece in pieceLocations[c]:
                totalPieceValue[c] += self.PieceValue[(board[piece[0]][piece[1]] & 7) - 1]
                isQueen[c] |= board[piece[0]][piece[1]] & 7 == 5

        return (isQueen[0] or totalPieceValue[0] < 15) and (isQueen[1] or totalPieceValue[1] < 15)

    def bestMove(self, allPossibleMoves, colour, NumberOfMoves, Grid, pieceLocations):
        if colour == 0:
            maxi = [[(), (), float("inf")] for i in range(NumberOfMoves)]
        else:
            maxi = [[(), (), - float("inf")] for i in range(NumberOfMoves)]

        king = [(), ()]

        for i in range(8):
            for j in range(8):
                if Grid[i][j] & 7 == 6:
                    king[(Grid[i][j] & 8) // 8] = (i, j)

        flag = False

        goodMovesHeuristic = []

        for startSquare, moves in allPossibleMoves.items():
            myPiece = Grid[startSquare[0]][startSquare[1]] & 7
            myColour = Grid[startSquare[0]][startSquare[1]] & 8
            for endSquare in moves:
                oppPiece = Grid[startSquare[0]][startSquare[1]] & 7
                score = oppPiece + self.PieceHeuristics[myPiece]
                if myPiece == 6 and startSquare[1] == 4:
                    score += 7
                if myColour == 0:
                    forwardMovement = - endSquare[0] + startSquare[0]
                else:
                    forwardMovement = endSquare[0] - startSquare[0]
                score += forwardMovement * 0.5
                goodMovesHeuristic.append((startSquare, endSquare, score))

        goodMovesHeuristic.sort(key = lambda x : x[2], reverse=True)

        for move in goodMovesHeuristic:
            startSquare, endSquare, scoreHeuristic = move

            NewPieceLocations = [row[:] for row in pieceLocations]
            GridCopy = [row[:] for row in Grid]

            NewPieceLocations, GridCopy = self.move(startSquare, endSquare, NewPieceLocations, GridCopy)
            evaluation = self.evaluation(GridCopy)

            if startSquare in king:
                flag = True
                copy = king[:]
                if king[0] == startSquare:
                    king[0] = endSquare
                else:
                    king[1] = endSquare

            if colour == 0:
                for i in range(NumberOfMoves):
                    if evaluation < maxi[i][2]:
                        maxi.insert(i, [startSquare, endSquare, evaluation])
                        break
            else:
                for i in range(NumberOfMoves):
                    if evaluation > maxi[i][2]:
                        maxi.insert(i, [startSquare, endSquare, evaluation])
                        break

            if flag:
                king = copy[:]
                flag = False

            if len(maxi) > NumberOfMoves:
                maxi.pop()

        return maxi

    def decideMove(self, colour, depth, positions, alpha, beta, CurrentBoard, CurrentPieces):

        allPossibleMoves = self.allPossibleMoves(CurrentBoard, CurrentPieces, colour)

        if depth == 0:
            a = self.bestMove(allPossibleMoves, colour, 10, CurrentBoard, CurrentPieces)
            return (a[0][0], a[0][1]), a[0][2]

        SelectedBestMoves = self.bestMove(allPossibleMoves, colour, positions, CurrentBoard, CurrentPieces)

        for i, item in enumerate(SelectedBestMoves):
            sq1, sq2 = item[0], item[1]
            if sq1 == () or sq2 == (): break
            NewBoard = [row[:] for row in CurrentBoard]
            NewPieces = [row[:] for row in CurrentPieces]
            NewPieces, NewBoard = self.move(sq1, sq2, NewPieces, NewBoard)

            countermove, evaluation = self.decideMove(1 - colour, depth - 1, positions - 2, alpha, beta, NewBoard,
                                                      NewPieces)
            SelectedBestMoves[i][2] = evaluation

            if colour == 0:
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            else:
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

        SelectedBestMoves.sort(key=lambda x: x[2], reverse=colour == 1)

        return (SelectedBestMoves[0][0], SelectedBestMoves[0][1]), SelectedBestMoves[0][2]

    def play(self, depth, positions):
        checkmate = False
        middleGame = True
        colour = 1
        p.init()
        screen = p.display.set_mode((self.width, self.height))
        screen.fill("white")
        self.drawSquares(screen)
        clock = p.time.Clock()
        clicks = []

        p.display.set_caption('Chess Bot')
        p.display.set_icon(p.image.load('images\icon.png'))

        while True:
            if middleGame:
                if not self.isMiddleGame(self.Grid, self.PieceLocations):
                    self.optimalLocations[0].pop()
                    self.optimalLocations[1].pop()
                    self.optimalLocations[0].append(self.KingEndGame)
                    self.optimalLocations[1].append(self.KingEndGame)
                    middleGame = False

            for e in p.event.get():
                if e.type == p.QUIT:
                    break
                elif e.type == p.MOUSEBUTTONDOWN:
                    pos = p.mouse.get_pos()
                    coords = pos[1] // self.squareSize, pos[0] // self.squareSize
                    clicks.append(coords)
                    if len(clicks) == 2:
                        possibleMoves = self.allPossibleMoves(self.Grid, self.PieceLocations, colour)

                        if clicks[1] in possibleMoves[clicks[0]]:
                            self.PieceLocations, self.Grid = self.move(clicks[0], clicks[1], self.PieceLocations, self.Grid)

                            for colour in range(2):
                                if self.isCheckMate(self.Grid, self.PieceLocations, colour):
                                    checkmate = True

                            if checkmate:
                                if colour == 0:
                                    self.drawEndGameText(screen, "Black wins by checkmate")
                                else:
                                    self.drawEndGameText(screen, "White wins by checkmate")

                                p.display.update()
                                self.drawGrid(screen)
                                clock.tick(1)
                                p.display.flip()

                            self.drawGrid(screen)
                            p.display.flip()

                            colour = 1 - colour

                            selectedMove, evaluation = self.decideMove(colour, depth, positions, - float("inf"),
                                                                       float("inf"), self.Grid,
                                                                       self.PieceLocations)

                            self.PieceLocations, self.Grid = self.move(selectedMove[0], selectedMove[1],
                                                                       self.PieceLocations, self.Grid)

                            for col in range(2):
                                if self.isCheckMate(self.Grid, self.PieceLocations, col):
                                    checkmate = True

                            colour = 1 - colour

                            if checkmate:
                                if colour == 0:
                                    self.drawEndGameText(screen, "Black wins by checkmate")
                                else:
                                    self.drawEndGameText(screen, "White wins by checkmate")

                                p.display.update()
                                self.drawGrid(screen)
                                clock.tick(1)
                                p.display.flip()
                        clicks.clear()

            self.drawGrid(screen)
            clock.tick(10)
            p.display.flip()

    # end of core functions

b = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")  # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

b.play(4, 25)
