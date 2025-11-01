import random
import time
import threading
import sys
import os
from calendar_api import update_grid

event_ids = ['skqc0eq2v0l9mti9etoj2488lg', 'm4q04rps5elnq0qt8selas75so', 'l4sppg0pgbvt9sf7ikh9ls0icg', 'mnp62rmvh6naqhqe2fckg9crf0', 't4h4lrb7u8u8ijnen1kd9r0d0k', 'vdr1pqkvre5n7ej7lobkoo9ujs', 'lqv4uihumvlmj0fbt8rmb602cs', 't3j91lgudqdg34dtm5o0g3h01s', '69akt0d6h1sune0pqkpbafc9h0', 'qkghgiu9g24qp27tt7nlrbodh8', 'oi44hhf0h20hjq2oaa180janu0', 'rqf0bb8inbgpaaj91d7ecfidbc', '1vs3td53ojcshghfk2o4n5be2g', 'obbpvg23thqbhukjrj5ean2u8o', '0hn1mgg3651r87gcbdqcaiu6i8', 'aj80vif34gnitbbc665ldmmt68', '74ionk1fpvt03jqn21rimk8dq0', 'hct0g4dh1qbup1g19vjsmnk2rk', 'da9o6h46hc0rqleigsc3m4l6ss', '8cea77ua36j7t5lbrpsvj8jt2s', 'gg7lmd3futnghhs0l8btpm170k', '5eo6obodq1gja4l8pb3va1esjo', '2trpdvppd6vuke93f7a17bsp2k', '7v6aetgodq5pm18v46qd59kt68', 'dntuprnp9schv8bnkcneljm840', 'e6gcf0k1rof33vtmhlvhg5jvo8', '4octr3831ncghkn86u5l9g3a24', 'servd7sr277c3l8har50mc97as', 'pb3lneah61d6suopilf0glb5a0', 'd8u10vtv6dris0lmkrs4q9tcpc', 'pa4jqeishfqfig5cor8if9c840', '2fhblnjg4k9ngq1e617e1f64k8', '01vmk3tiocuh2ufg8sbt9amt98', 'q8ikbkl4jp6kr9dos4ifdie444', 'd1e5ujsafcm3lngvrc0fe67ris', '7niq7mqqk4cato696jl51r5g20', 'uiacmbv7gd41a3ocmuhahki45g', 'bg232gttlgcr1rgrng444tq64s', '50jrrl2bflkvthgccl9trjqet8', 'h4cmkk899rff5nohspvn543cgk', '494g6doeh77ojmvdc95k3lqvro', 'ttu0ecbb6p1kb9ncfqe5so6lmo', 's26089a57p7pkmov8468kbmo9g', '81iibi57dpo2lbf1e3r2lrq0l0', '7gpe5407eiuk78ke9jrfkkcp3k', '38u20k10uou5rgaqfppp78jgjc', 'rm1bn3moht36es4qpkgeb77cm0', '86kegbie1nepj822gk7cps91us', 'flrd6qm77enee44a0glnqtjusg', '8r251sir78ia02qnm5ekbak6p4', 'jo7dsvl1euurhl45guaqsktm64', 'kapj11gd0rfc01vmnj3jqf003g', 'laf5t1tpbsup9er3ulspo8507s', 'cbtm77ient5nd0fqn9d2t48ns8', '8v2q58tkp6slb72upbbtes1urc', '0lg0p4fbkgt4vm4nqr5nskkkfs', 'k6voqq8r6nnoc836nrc72aqt2g', 'kdbubph5ghruqifg9iet8j95t0', 'c28pn0gtgm0g6nkp1rgk2qvht0', '1f6kloq70crbl53bj0lr8p68lk', 'o0tv5l2d2hhhet0p0fkea0vnao', '506sle5vbtr9c0u959mql80iag', '1i4vknaef1hlshtaulsrbc9as4', '8gg1hj9roc8latdmudab7ftpjg', 'koq9mt0ie2b7569ljd6ka0bhn0', '5cq90no87k2mrfie34r18q50u0', 't89g7h9njd9p7ab1nmfi9k4a4g', 'dj7r9phgi2b8d5rghar92niaik', 'h1aiios13amrmt3d1oagiit6e4', 'tenf4jhf8m3lqotoomf87aju48', 'lv3nm0kgerjn2amaundhmme4tg', 't772e28nlrgkeu56fj2b2qg5s0', 'mdhig5gnju0tdd047071f16pps', '7p17qpntgd3coapukh2rpvjlbk', 'hu02a0037mi46qvf05oipeepgo', '9clnsavb985c374lloan6il7tg', '37btvpc4a1igdpo2ano6j61u2s', 'l53hs58v47ji4hfvqjf5vld5kk', '0u18cfhjtm14p95r46mpct1958', '04u3k9q5331uom38cei5c0ut3s', '50vleftnpj3n3hb0pj3ujlno7g', '1vs2rjmqdebd5filstdjhcrddg', '2i8fsnuaf9f1j6le0n4bh6srfo', 'oeh677fboaei3th4dp7r1amn6s', 'n2b2cvdni259btnl29hih777r0', 'so09q4j71gt3v5kb3t0g1ol8o0', 'icuug4ektoc7amga9laavu0vq8', '8dsncprsvu15f0prpqgddkeeb4', '2g753nob1r72ohllbn24dhv5l4', 'b3i7b8abo1kfasg752m8asd010', 'hsfppst2gq9s6h75luusvmnfdg', 'qad53m19tdt94jaslmqke4ir08', 'kd8rie4roa915toc9hiedc5p6o', '75pe055s59jf0egb1ae3q0kkss', 'vfmlr6gnusp0vt4ktospfmpdn8', 'b20e0t4d4h58el3pp1jmbvr44k', 'kdqi6nj2j4o6u2ioqnrq5ob1vg', 'i0d5vusmbsmv627urlg3nh1vb8', 'd5r2rnjq37nfvnnv675dgu51kk', 'o0i6r68043k7g5r2ba942omegg', 'onct4upiuv56sunak2vf93o5o0', '68boklds45t8rs294s11h1o65o', 'mmtvmuo0rvm0kis6ak1heh53k4', '3et0pcr0a48bq11gb3gcn3sd8c', '8e1o0qsndeqs0qjv4pje6dfv7c', 'bed1f0j24330rjvf5ku9oplg2k', 'qs1qsnmaesgpm8plopq6tme09k', 'nevf9ikq5dg14gevm8bfpl6lqk', '7jrfmittj3kihjnm83oetplm3o', 'a159b926a6682sormv6b9n3brk', 'll62gdm30fat7qhonl3hc30hks', '65h00n242el4fkmqf340sujah4', 'j7mle7eac8c2anm2bv1cj5uqmk', 'o3dla7t7h9tpkjir5b23tb4c00', 'o35k9t84la8195gl38le5m18ko', 'havrhvdo1u223nie6jen9mklqk', 'a39en31d97thnqh2ev0atvbkng', 'q7ol6tvvkdpljjgt7r4lckoscs', '6kqs26jed5oi5fmn67iiipotkg', 'lhcfc8hjko3glpkt21ovrb1b98', 'lpcv1prj5upcq518bo9p96quqo', '60d0mor5d1t5vfue6nq4bce838', 'at0kbedjokfiu4mfe08tr6s2cg', 'cslfu872mp1ni918ep1pjd70so', 'vd8n8ovmk6pe1n30nunefd746c', 'cjk50aq66de2sgerbgtb0f99kk', 'hli9h414id14ar62fa8jtrbmo4', 'anqdn1dqf15ecak40jatql6950', 'tdfbo78i94rprfhdoprnsebsrs', 'bkjo0fqdcd82oha4vmehlu70ek', 'r5urtkojth963mbcur4nf6se2k', '576v8p9fdr0gak0fjcbt0rd2r4', '3bbo8v63d2a467n09k5cfm9bfk', 'hdh02gelj6rppga9bnbi4fp3j4', '5eu487ocq2gpomfbrbam8e3vl4', 'n28omb17cva2913iafem3rg5m4', '9r75tka9dqrumss2hm6vivc770', '7sfc3n9kapqi4ia47d18enuaqs', '7ncc4mviqt765tq4tk29rton18', 'idt9ce7magb399cpip17l9atsg', 'lg0gle7ve7hsg1vahq5n48foq8', '887o9fric2ll256vdumul0ri1k', 'mhgtass1vnruh8tif5nvgcf6f4', 'qutj24am7810odul803ek4lipo', 'agvb4idinh0jc84nkn9te975ic', 'eil5hm8lpu463kj5i3j7tt0tls', '655cceh49k8t88bpath7hrbde4', 'm9k1vbglj6lprkh5m97j3fvt0o', 'vbhdprd799t38ajh0441qhsqd8', 'aikb2dba9u2feepb8chd0hugm4', 'kav4dtqc8b8d6bea11sqm971qs', 'i3tpsmd7gtjf9oqc7chnbp86h8', '31t79invs3edumqrdg37vml4no', '7212hes1lekd7hu6u0sn4ckco4', '71kd1de5aolpb43qej0grm88hg', 'ivoi963hh9c2rkm5q00kre372k', '00eodc5lijpu8hkh3hrjdumgdc', 'innduckmhl68tgerqi11bj4bmg', 'ts3vaj01r7vfklt22jekdifl7o', '8s9vj4e9stm0gj37a4jaocmdqk', 'rdcup438t38vpognhectthl0i0', '27fusl27165s9niekpm1n7vqk8', 'vm1gml5gm53upmf7o12l090l5c', '4v8sij242b58p1ickrss7i7c6c', 'uq9g09kof55js0qc7smfijn5jo', '3i1078jquhpir19t7emmj80g1o', 'kh163tef404bb9j89duafui52s', 'rce00vmkkbb1mhfm2klf4nm8fg', 'hed86veacbtdtv0ee07qq2jupk', '04nev31dn3igvr345gq0gqd25k', 'etsllmie4ummadu43e0i1uev5g', 'hrtmrglnpm7qjhhhtistp8o08o', 'h9p6qafo8mgbki1g7b0835p92s', 'j0dj5n0gbg6gp2ag1mnob1ude4', '7q5lt41i5873k2uhf444pcb4h0', 'qtt9qfa5t7ahrbohjddpi1bj44', 's639jfpcnlkb6tnptplj3u06to', 'jb4bklb3egi70il6r926gtklj8', '51svnqljegvehp4ff130uafrng', '34lc3bsnh4lqfmkf49gnave9mo', 'qg4it6notuj0f78b887qhh8cdk', 'u8ev1vfse02sgdo689j37c8ek4', '1f35gvgvo28nh9pufifl4hg2lc', 'k5nukkh78d6rclk2c7qs1413to', '37aocmk88dj90i537uc9dnsh10', 'oi814som00chrpkd3vvnchkiac', 'cfitqrsakg8hkkb14pnb8umh1o', 'c5ql4uvude8qh2603rcbn1hig4', 'qrotqqgb57caemrnk6ri3qsbig', 'n5kik6c0ssu7nrtm8jbu4f1q30', 'pa6dn1chs1qd1bknc04jp1orj0', 'dngelfuemf24btk2ntaj9imq5k', '3t2ajajb40j4sol33ikupdn968', '9eojj52s7jd8gcir88j6lesms8', 'kgoulijif3joqtaac20hha4pe0', 'vjnpv21705gu8vc5rcb40r6l9s', 'qlc3mcdpv93809fg4lgried89o', 'goedufccsi5t7ib9eq7o2pcqns', '7u6bd2klpkblkckjue8ab6h7v4', '957nlgiv3ofku9igu449h6d8uo', 'e18v9drchnlfsebqvhe31pjupc', 'bngpdp95pn3p0ijv3jaev5g7ss', 'qbefhq4rd3fjdjg0bnoiea2h6k', 'olgbe030029u12rujvpcn3btj0', 'tta956a66sf7m90h1u93ssn4ic', '0flut74a5je4ephu3tf277p9ho', 'jqt24b2psch1njtufqd9jlh7lk', 'o76ltrtvhuroiq7h9qr202rg70', 't619tkdj6j9hlqda92podvtmts', 'b1fk5of7cn4jerbe5q3qc10g9k', 'lnht7kmfe1v88dvongvb2efg5k', 'fgo41e1sff0lqb13qitdmc1gm0', '357u56356disl1et41u4h703vc', '0nmh1p2q55m0o0mctpm44n5nks', 'cnsa3k122an9ip26684h0c30dc', 'dvo20b5csh4tj2t7h53815s42k', 'r3e8ro7b180pt1ht8hsc1tiops', 'hhh34t3rq0jl2vi8mlet44hhsg', 'e58d8h7tn1cu6ks9u2efc1b648', 'n64s9mb56jd023rulfm3clpmtc', '8m774h5io5kh3his4nhecot5h0', '509dpv7vdkorej7cek3l5briqg', 'mffncc26ca7a0n86v38n1o0lds', 'ad04mjp0ubiviugfo6lrgcq5dg', 'km8cv3165e6tt0tkgj6s2gc4j4', 'aicqj3n3c4b066o49oq83qlgsc', 'a46o9ec3ab4pp6ad5319sj3v5k', 'v8evv34d2hssq1usi29en1lka0', 'jmhqdkdsul4vkhq578e6f6hlf0', '3apke90aarl78kgp3tgihjomrc', 'mm7akv3emp9vf68fdhoa7i4rok', 'a4hons15suocg8h4udsimij2g4', 'cuc96amrtqc3evuv8b50sfj478', 'nur72r4hnbf898hmrtavg3md2o', 'p2kq51b2rd9g6c0120ou3o0elc', 't7oakaf164bvic65vibrkn0ljk', 'bhem2m472prl9tk07l8fcooqns', 'q5pl92rhv8lembskn3g1d277r0', 'qqis3fcogvrim3jjjgf14rh040', '0psg2tfin109kfc10ibhp8joqk']

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
            time.sleep(1.5)  # tick every 1 second
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
            #reset the grid
            update_grid(previous_grid, event_ids, [['.'] * 10 for _ in range(24)])
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