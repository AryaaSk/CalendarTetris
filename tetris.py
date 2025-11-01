import random
import time
import threading
import sys
import os
from calendar_api import update_grid

event_ids = ['6ltdnn1013acdj3oftogk7vmks', 'np0q0imtuij6bj6iaj3n1u81ho', 'g5h6k13mod5kap9g04a2jmnmo8', '59q9dirngeevf1li0tsn5sn8m8', 'g9lk1g34449bonmgipds55lk1g', 'pcu7ahteta9isg1evb77kinvoo', 'kjq0str03iqarppnf067vgndd0', '6jobrnch65m5m9h74haqvj15vk', 'jcjv8g3qm0hag51t96hq571bok', 'l3iqlia2q3hanjvejbkj49c284', '4jc864mlbgfb5oec3fm7sda2m0', 'sdgbmu1st7fcs688vfiedj37g4', 'upirk7k8tr8fr3uc0026vcr0f0', '4fu4crqadkh3eagnu18ovgrpec', 'grr535dhkg6nba5j063k0u1pq8', '6la3ki3pfh5jk34ms42a3k9p2c', '6eqbob5f9pdjlomrfdh1cd820g', '3ud212dfgc6rc2ubokv22g7ag8', 'hj0sttb0h7m8mkt5oni8a2rpqs', '4rrmtkhpsfojlo2ji5d6vqglog', '0unifn3d4s2skh6rtqs4anuhto', '67vfkcnhf3gtialkqq0holg3cg', 'r2l77o5fqjuqitjlcnvrpcs9sc', 'p1gdtd0jg17c6dqlk9o03rbrc0', '6hm30u6lhmgkk0v38ekd2kj1nc', '9gcm0rvu3ueus0s8gl56p8sono', 'm8olqrt62lasthm8anj1fb0lmo', 'gfu0nolscf8n9b87c652pfe560', 'e1lahe8982eqitac28l1a33mbc', '4n5es9bunqdi58b14h06j32n4o', 'nckb3cjf73ct9js4t47l2lcjvg', 'u8r24vc6lse4dvj9umqlcgjln4', 'ot3s2ci0ol0l2s92fihie3u56s', 'd1nhskrabsu5nddam27kbrl1ps', 'tue6hgquemhuirav2g4a4r093k', 'l9qfglhkqcivbjo4qospju54dg', 'b65ntqfeldqogqjf15qua22ng4', 'fp912c13i3f83k6ttuit40b604', 'am2flps2hopj5tb99fshepmcfs', '7ocu4jcma38khdf55m0th1rq74', 'bh2if012p15kn895f3vgqrdils', '1dak83vt70tbs7o0qcp0qr6tc8', 'itja81bs07k1j74f84e5uc28co', '7bc046fgemm04l56898bmdj33c', '53nv58hc2dl5tile3594ujgr8k', 'tum8bi0jee6d8dnd93oknuqgs0', 'a9ng5q1oqhq3e2m5a80e9a53r4', 'ehjplats1m5alaciij4rkaa84c', 'goj31lgvnt27ccj7is22egraic', 'vohv2b6cujjk8tqjj3pf4kp57s', 'blivpgcta3g020pb5eoc8minno', '2vpctoa2sqsmqimjtitm4s74l4', '2vokcsr3be1ok5e0qadk019ivc', '3khbmv6v17akqcjse0tjekt3u8', '636u8teecuqohopfp7hsu2i5fk', '8a3omepc8c7n350mq4k8b55mak', 'gqmi1anvguju1k7006jatts2cc', 'ok0h7m208f1dktdoq82iec0qdc', 've05m9bbn8uq1oj9rr0cmkdvbc', '2goiei85trvjle4s4pne1jmmn4', 'csvm45qpq9e8rcfi2uf41s6brg', 'e8g93q8rg386ds2dd5ibapdvq0', 'nfrpeo3u8rts8okbkht78svjf8', '19r0dkld31n5313lsm2h3s4lak', 'uivp0k1ln7m0mrvofane65koac', '8g45563vifqot8r7rmlaqju0ls', 'i0qrdhmtcro3949m7agi9292v4', '06ne0cbib39h8v2bo6b545pj9k', 'm2d56cljqd11rjglvbupa01l3c', 'j7k7439aa79hf7pcnpapb886t4', 'meugtdevu7svr1ks89u953car8', 'sl99mf3uq0hueb416e90paoc4o', 'kv5lj7p4le3egfsn85sj81o9vk', '453dbgjern4e2jcad27hq9ujsc', 'r8alsivfn5ehov6729hbeljsr4', 'keair2uas190njl5fruoehus24', 'a93l2m2jc2p1t3ch3esui6638o', '0ocrjvciv6a6ang2ui67ntgs24', '922ko4q9u37jfk98cfkia3231o', '72709sgreu7fvscud029vul0ps', '8utpbbh12csfg1934hhe19ahqo', 'i4kq6tn1k9f39lbnmmmo8s0k7k', 'bj04tqiqateb0v0hdv79ghqk10', 'jkqe13lrhk5dinjc5m0jh85vf8', '5tiqc0j9ogfvqrrkb1l2dmat48', 'o0dntth8j8ibd4pmi0vqfka0s0', '9205b7lgmrbise1hllk5equ6j4', 'j7m9leno3dhhhmr0hqduo3ds4k', '002d51k6qgekh3m8ahfmbasdt4', 'q81128s0ooknctrs3epndqf100', 'ue6ihfnpa68bqcs6fjm3ljsha4', 'f57b0lvl4ar1rfik9mtbarhcls', 'utg67k1bsfq1vkhfoqe44gin54', 'nemurpdk1p9osioom5r5nlsv78', 'vcu1hgddkmasrl0h9lfe0tnseo', 'e7v6dv8po43vpr8anisvhe44fk', 'l3gicoted3gs04gkg0u4345t3o', 'm52677bdvc7tvi85jtnv2cjet4', 'qhkq9nj987g0qipim1i8gkn92k', 'lv7rroltd8cq1hl09oi25efo40', '6vjl2335pcfhh3poaii27c503s', '5rn4jus605l0ev3t76t9pqq8pg', 'g1ps80ki4h5vo6gfihevec804s', 'h50pjhiqdruld556elbv5mhgkg', 'ie26o6k2c93fek2fcdd35macm4', 'gihrflar07cmkurmtcb4j1o0rc', '63rdr83068ud6u14qobr5687ig', '5t1b1ml9djht8smus0aeb8bfjs', 'gdddngi87eri75ntqa1u9ef068', 'uec36g7r4n87at2ejcimvocm7s', 'ppd6rrjrt6b5osqkitj08qj87g', '7hc4siecib3kcj5jsoruo04s2k', 'jb65bdlefrnf2hmr7jc1loj3eg', 'nfvf6snsvnbjv2cesbjfe04ees', 'hfj94ap20e3f48h3p1v4fduopc', 's4uf04mljemccck5b9gnv78evc', '59mh0oal62htmn665djcvhu9mg', 'moont4e6tbd4sjpf7afo8s3oq4', 'et5fclburuudnq7g20nq4v7ld8', '27vfa9d24tp9stuk2r80qicuog', '77qj870795qv4j7qmo7ffg6ib0', 'gg4j2lsbg5ilkqrtpb5q9cmb68', 'hjd868dhfr86h6plcnprtdp8ic', 'glt232ki6c0li7jfn23nrvi35s', '3d3gqqbvemiq9fdndbsirlhrv0', '3r3pe34pnr0tglghg7h5l994ug', 'dferk10c9mova6me5ouh50c3a0', 'r95ken9cd2lhmmtt71tflc63qk', 'gg41a5gtvi0nqh49o4ha81ekmk', 'p4hltprehjj4fbkgsrm2elfvug', 'p2qetgndh32u56cj85i5h2orl0', 'pa08o9cnkkv5f4j5p5ntkjsu9c', '9v1j0g704osv0h3m4h6duv2duo', 'q5u9ttc2nhfk9pchjet1n71dlo', 'h888pn3qjv8chjoucuajag6bho', 'v8iaquecqnm79105rpiqtkg6b4', 'upcf7t61pd9vilc2e29kvll5ig', '7jts1ujgt18ugoto9b6i6nrt9k', '04mpfo1uk62pabi7tdb3uuov9o', 'coma39lcbqu69s56lokaet0s0c', 'j6ekvgqqtbivifi9m8ruru8e04', '841g7lm3g7sn0e76tjvaos50ps', 'jj75il2a784ba5jpntlj5uj8tk', 'h5eu08g3i4bpsdrblke2ftjqvg', 'llumd7j1l3736ffekk33986flo', 'hlc15931a04beqemf730edv06g', 'ekpp5v7e51mmakla1v8qfb811k', 'edrican5133bsruuvp0l6o0ork', '541cehvs38gaereqg1ghao365o', 'russb78rj3gjaai5g35bdcnev8', '8k83mkasi53fufsjikejbc6evs', '2k64kgqf0a9c8n2b8qgd2pci7c', 'pc1ljid764q75fhsthe3ogu71k', '9hkbhqgm1dt9p9ttdsc8hvvo30', 'r1itlnc9jl23i220doupjqf62o', 'hckjj0s4ora495off1ftar7ktg', 'ceclejuvtjefsnktu86gcc4fd4', 'hf30bu724ioi4kqr1j0tvds4us', '1gjlb2lh6eq33q230ooh333rug', 'q8kpqlacspg21lrlrk3r7eb4jo', 'jj6ddb65mnncoruab6cg10setk', 'ua5kfshkbn884o5idsbtkd30dc', '3sbamc5gav1f8vik6afv8ncfmo', '3lu9q8naqu8mb4q6ph274a59u0', 'idbcu78u0j9fku4vdoq8rr09ec', 'dji0vqgosc1srqq2d1q8h6574k', 'a0lnqf0rt7ikp2nq47i2kam7o8', '7fnq905dg91kuqt5rj2l21l6d0', 'euvut6egig6nurnkklppp16lqk', '1223fbtrg3injh1hlff6rbdot0', 'n96190ni76elhqvk8sm454drc8', 'ps9p27a72kpa44bg75q3qksndg', 'maarr089qtnheflgk2js1hcn4g', 'o4av2tlqpoloolhi40g6i8p8po', 'dgb451cft8011dva43df5oq7g8', 'ggmfjijqhd5f7g39rmrkj55vt8', 'u1ikc5ofhs2u9odp4029j8ssro', '52ferbampfbsk676hs3l3gi5e4', 'vu87tduo71n86mkj86d3ufmtvo', 'fvetrhpi6dvcegn5ktdoi544ng', 'teifk1218ce114fpj582c0ql6o', '1ndbpto4rjk1qpt30g9sf5lbu4', 'tlotnb8vcfkpq69i06r5mdnjuk', 'mfts1lflvjrfp3a39cn58qbsgc', '61gp2ppt5cp5gr6k0f4tc5m4n0', 'd6r4s7l78o0uki50u0b0a9v6vo', 'l2v9r94c85rkalt0htubq9an4o', 'l09rctocpiqpqffo77j8pa4jvc', '5or5jevgpvgbphjkn2pe5u2248', 'lmgikkq0unogcvqa0a2av5d4k4', '6hkbiejcplncnl1m9ofcvdh830', '4cs978c56ntv4udv3vj599vlr8', 'tumue8n16ibecabu5qv9p5gjlg', 'rfdcjo5qnpcqi4s9dcsh3jf8n4', 'n2qtincia2cs8a934d6iidrlc0', 'lebkq61mh38o5016os4mija770', 'avreq57stgld20tfe35od1j7c4', 'aq6f34v6p37sghg476jnakfu58', 'ib6e2vlf0vh2l7g6huqt6kcmug', '79l3fji0772nl77h8mduo91ivs', '9g1ngaq64vpsponam3jcbhk4mc', 'uhlrcmud7ukf87fcbhsg6dtddg', 'a17271nhfntqss0gths8moucl4', 'j2u5ob1kuj0oolnp6p0tjocb6o', 'tabnp2cgrkb9ggjf8uv2n72tks', '6l9hp6dop6n5g13s4tol9l55k0', 'ijsu0jt7bq67lobuta29pladhs', 's5vah2ne9agf1n7qc5p7tc9104', 'jsad17bqhaou5n9unharsq8bo0', '6btrvmablkkes9c1dr0nfsv5k0', 'lup8bh1er0shgs1pe3iu50kpro', 'nbq0vb2nsl1l02ingpj9f7r28c', '5okp0ruqso9pdcct19q4p94mio', 'i566l4eda67rl4s6hv50fu7j7g', 'dvue3hstseu839ilq1n12ss4d0', '369ij3hrqpp8o2lujl2190pps0', '1b2ke38ru41qgcbrj89ci2prqs', 'qe3ikeomp7hpig31ssll6v9ctg', '7b44gtkj4kk91jq1t41337sj3s', 'enn2b8718uupr09fouuu53ligk', '4gr7udfsvq10har58souv00h8s', 'o1r6pc71mgfb7av672voh0jtc0', 'rttkrbgblreltb56a3e9a4m3uo', 'bms9liujvut5j2eovjs4tf6g1g', 'nijk6gbmss0kp171m46ucg1av8', 'vrbm5kli3l14jcf305c96lacos', 'ljj49j34dvlcfcudtetmtifa9s', 's87nj0952g35eb0tf027u12n7o', 'b1amvaj484vhvul0an0kicq1kg', 'm2qmu7rik08738a55ccd22m9tk', 'rhug5ueftrr0afb3aehjo87r8g', 'j020it0fj76pos3khtjbmnb1ug', 'g4qnnhqejrq2un8vj10karkvco', 'p3gk23ml1oqnh9ho0d4r131qvc', 'ots8cjbuna8er82jaa40lnnjbs', 'l5gtpi4dda8e46hr6llt7f7m4c', 's01ig76cgn0qp3c3rdtjnri4c8', 'hqli3vomkc4q1525rqaaq2s3n4', 'apov091hsvvaea149f3phk933g', 'ms64v5ml0ansr00nf1rl70saao']

previous_grid = []

class Tetromino:
    """Represents a tetris piece with its different rotations"""
    
    # All tetromino shapes and their rotations (each letter represents a different color)
    SHAPES = {
        'I': [
            [[1, 1, 1, 1]],
            [[1], [1], [1], [1]]
        ],
        'O': [
            [[1, 1], [1, 1]]
        ],
        'T': [
            [[0, 1, 0], [1, 1, 1]],
            [[1, 0], [1, 1], [1, 0]],
            [[1, 1, 1], [0, 1, 0]],
            [[0, 1], [1, 1], [0, 1]]
        ],
        'S': [
            [[0, 1, 1], [1, 1, 0]],
            [[1, 0], [1, 1], [0, 1]]
        ],
        'Z': [
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1], [1, 1], [1, 0]]
        ],
        'J': [
            [[1, 0, 0], [1, 1, 1]],
            [[1, 1], [1, 0], [1, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[0, 1], [0, 1], [1, 1]]
        ],
        'L': [
            [[0, 0, 1], [1, 1, 1]],
            [[1, 0], [1, 0], [1, 1]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1], [0, 1], [0, 1]]
        ]
    }
    
    # Color mapping for each piece type
    COLORS = {
        'I': 'C',  # Cyan
        'O': 'Y',  # Yellow
        'T': 'M',  # Magenta
        'S': 'G',  # Green
        'Z': 'R',  # Red
        'J': 'B',  # Blue
        'L': 'O'   # Orange
    }
    
    def __init__(self, piece_type):
        self.Type = piece_type
        self.rotationIndex = 0
        self.Shape = self.SHAPES[piece_type]
        self.Color = self.COLORS[piece_type]
    
    def GetCurrentShape(self):
        """Returns the current rotation of the piece"""
        return self.Shape[self.rotationIndex]
    
    def Rotate(self):
        """Rotates the piece to the next rotation"""
        self.rotationIndex = (self.rotationIndex + 1) % len(self.Shape)
    
    def GetWidth(self):
        """Returns the width of the current rotation"""
        return len(self.GetCurrentShape()[0])
    
    def GetHeight(self):
        """Returns the height of the current rotation"""
        return len(self.GetCurrentShape())


class Tetris:
    """Main Tetris game class"""
    
    def __init__(self, width=10, height=24):
        self.width = width
        self.height = height
        self.board = [['.' for _ in range(width)] for _ in range(height)]
        self.currentPiece = None
        self.pieceX = 0
        self.pieceY = 0
        self.score = 0
        self.linesCleared = 0
        self.gameOver = False
        self.SpawnNewPiece()
    
    def SpawnNewPiece(self):
        """Spawns a new random tetromino at the top center"""
        pieces = list(Tetromino.SHAPES.keys())
        piece_type = random.choice(pieces)
        self.currentPiece = Tetromino(piece_type)
        
        # Center the piece horizontally at the top
        self.pieceX = self.width // 2 - self.currentPiece.GetWidth() // 2
        self.pieceY = 0
        
        # Check if the game is over (no room to spawn)
        if self.CheckCollision(self.pieceX, self.pieceY):
            self.gameOver = True
    
    def CheckCollision(self, x, y, piece=None):
        """Checks if the piece at position (x, y) collides with anything"""
        if piece is None:
            piece = self.currentPiece.GetCurrentShape()
        
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    board_y = y + row_idx
                    board_x = x + col_idx
                    
                    # Check boundaries
                    if board_x < 0 or board_x >= self.width or board_y >= self.height:
                        return True
                    
                    # Check if there's already a piece there (but allow negative y for spawning)
                    if board_y >= 0 and self.board[board_y][board_x] != '.':
                        return True
        
        return False
    
    def PlacePiece(self):
        """Places the current piece on the board"""
        piece = self.currentPiece.GetCurrentShape()
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    board_y = self.pieceY + row_idx
                    board_x = self.pieceX + col_idx
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.currentPiece.Color
    
    def ClearLines(self):
        """Clears completed lines and updates score"""
        lines_cleared_this_frame = 0
        new_board = []
        
        for row in self.board:
            # If the row has no empty cells, it's a completed line
            if all(cell != '.' for cell in row):
                lines_cleared_this_frame += 1
            else:
                new_board.append(row)
        
        # Add empty rows at the top
        while len(new_board) < self.height:
            new_board.insert(0, ['.' for _ in range(self.width)])
        
        self.board = new_board
        self.linesCleared += lines_cleared_this_frame
        
        # Scoring: 100 points for 1 line, 300 for 2, 500 for 3, 800 for 4
        if lines_cleared_this_frame == 1:
            self.score += 100
        elif lines_cleared_this_frame == 2:
            self.score += 300
        elif lines_cleared_this_frame == 3:
            self.score += 500
        elif lines_cleared_this_frame == 4:
            self.score += 800
    
    def TryMove(self, dx, dy):
        """Attempts to move the current piece by (dx, dy)"""
        new_x = self.pieceX + dx
        new_y = self.pieceY + dy
        
        if not self.CheckCollision(new_x, new_y):
            self.pieceX = new_x
            self.pieceY = new_y
            return True
        return False
    
    def TryRotate(self):
        """Attempts to rotate the current piece"""
        self.currentPiece.Rotate()
        
        if self.CheckCollision(self.pieceX, self.pieceY):
            # If rotation causes collision, try wall kicks
            if self.TryMove(-1, 0):  # Try moving left
                return True
            elif self.TryMove(1, 0):  # Try moving right
                return True
            else:
                # Rotate back if wall kick failed
                self.currentPiece.Rotate()
                self.currentPiece.Rotate()
                self.currentPiece.Rotate()
                return False
        return True
    
    def Tick(self):
        """Main game tick - moves piece down"""
        if self.gameOver:
            return
        
        # Try to move down
        if not self.TryMove(0, 1):
            # If we can't move down, place the piece
            self.PlacePiece()
            self.ClearLines()
            
            # Spawn next piece
            self.SpawnNewPiece()


    def Render(self):
        global previous_grid
    
        """Renders the current game state"""
        # Create a copy of the board
        render_board = [row[:] for row in self.board]
        
        # Draw the current piece
        if self.currentPiece and not self.gameOver:
            piece = self.currentPiece.GetCurrentShape()
            for row_idx, row in enumerate(piece):
                for col_idx, cell in enumerate(row):
                    if cell:
                        board_y = self.pieceY + row_idx
                        board_x = self.pieceX + col_idx
                        if 0 <= board_y < self.height and 0 <= board_x < self.width:
                            render_board[board_y][board_x] = self.currentPiece.Color
        
        """
        # Print the board
        print("\n" + "=" * 50)
        print(f"Score: {self.score} | Lines: {self.linesCleared}")
        print("=" * 50)
        
        for row in render_board:
            print(' '.join(row))
        """
        print("rendering board")
        if (previous_grid != []):
            update_grid(previous_grid, event_ids, render_board)
        previous_grid = render_board
        
    def tick_loop(self):
        """Runs the game tick every second, independent of input"""
        while not self.gameOver:
            time.sleep(3)  # tick every 1 second
            self.Tick()
            self.Render()



def main():
    """Main game loop"""

    if os.name == 'nt':
        import msvcrt

        def GetChar():
            """Gets a single character from stdin without Enter (Windows)"""
            ch = msvcrt.getch()
            # Decode bytes to string if necessary (Python 3)
            if isinstance(ch, bytes):
                ch = ch.decode('utf-8', errors='ignore')
            return ch

    else:
        import termios
        import tty

        def GetChar():
            """Gets a single character from stdin without Enter (Unix)"""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    
    game = Tetris()

    tick_thread = threading.Thread(target= game.tick_loop, daemon=True)
    tick_thread.start()
    
    while not game.gameOver:
        print("\nNext move (a/d/s/w/q): ", end=' ', flush=True)
        move = GetChar().lower()
        print(move)  # Echo input

        if move == 'q':
            print("\nQuitting game...")
            break
        elif move == 'a':
            game.TryMove(-1, 0)
        elif move == 'd':
            game.TryMove(1, 0)
        elif move == 's':
            game.TryMove(0, 1)
        elif move == 'w':
            game.TryRotate()

    # Stop ticking thread
    tick_thread.join(timeout=1)


if __name__ == "__main__":
    main()

