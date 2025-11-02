import random
import time
from calendar_api import init_joystick, update_grid, check_joystick

event_ids = ['75uog6gf6b5mn9vap4m9oeu344', '4a31fpf0cbi22h237or8681soo', 's8vgs0gpm0em51q094davfej3c', 'alahoc8ehu7ol9o6fair5c9sj8', '6r43cu624qvl00879lanplpk5o', '02kaabkfeat9e20lvf445nv1og', 'a17259hf3t8cmui0d5d9lc2jd0', '0ik548ad7gkuma9uuk90s7757c', 'lhmoo211nhpubf242d3htgqdp0', '4406bbdco2365qu75cd00natlc', 'n2n0ora2r07ke97sc7jvhonbjk', 'd03os3dkc359tfjs40olht583s', 'mn0a314sgkc2r5tnfo3fltrgbg', '2123i5s6o24vjoueonq26j1e6k', 'cgg05i1krvdsji38o28a43mjn8', 'i4bmtsrl7net8mahj6pjgaidk0', 'dd9ilgtm4bc48l80k8jrebdqa8', '2r82d497dhfebqfpf7mcdlcfag', 'lj4rg6e38sra8dl3q8ope1t7kg', 'qn5pfbsnh1igh1bjh388mr5l28', '9dtnboko0k1at487s574aoga0c', 'qjj1972vgbqm7plvavd4du1egk', '2l7b9te96nhjdfg47cl2p225is', '2a0tbfat2i6m1ddnvie5qdd2e8', 'er4nuf9au78sn3rptc61baov30', 'junic5kgpdm7g2d8ppfmrd2934', '1cnjgd5pk2789jd3ktj4iuvg28', '96p3oh41jcp165klfuhaaak93k', 'ns37ia900mcbghm4l49osbt4rs', '7q6p19hu579t0gb5n6ou6l6t1k', 'ef1d4oofri3a6v6anqjtk87omk', '17t8lla9frhj14hihnjn89mk40', 'dsq0dhg6dp89p3h8chgeo4ida0', 'fufpeflh6d9vq6pe1aj5shbk90', '16hckutu6q0ct226c636qpfja8', 'nqsj1ffkcg04dhr79o47ha4ecs', 'nhsm3m1mocnno5gqujrqedsfi8', 'p7guc13ke3huu3qq3o3a33g4ik', 'oh2ovuabj5d6ohdodu4u2kk2so', 'uq5qn0pit59gfq33ddhgvsp2ck', 'll283k34tk9siiiomknrvtqa74', 'cjk3rnjlrf29bcc5qadhgg0ju4', '30jafcper7ig6e6m8if6rb05i0', 'qan0ecf62288or795br7b44pjc', 'ipfkpo74gqe13veu4kg3agoink', 'nk0o861peddkasdhcompcbi7go', 'ujh9fqvigf7ijmc3sv426q816k', 'n5r6qolfhnnv8kfo8cq449nb3c', 'r5cdbkqbhlr2uh6nmhettjo4v0', 'eu2r7v8pcsd0ub2463njqurn3c', 'hqhlnulspji61u3dahl7ki6720', 'pv1q3eu349du9njgmnhn5td8tc', 'svnbsecr1tcpc9cs0bkql7i7dk', 'v35067nu3na3ucuk82uf18ins4', '6jhf193m93143jmiaqp2oc2404', 'vtel9278ofo21t5n8iuk4fesa8', 'vu5cj0for11njs3krl25oeupno', 'nh9bdrgn7ecdlloq8m3a21g06c', '43mruk6o0uffh91u3879e8hl7o', 'nhm631otqadre4dr2qm94oj4uk', 'uabojm8sqd9qo2vvq72h2uvfd4', 'i3otdj7la55rfh8cmk73gduur4', 'qguio83u24lfg0tj0bcg08ivrk', 'quhqhecm2pk0n4sl2dukb9o9ls', 'ch5i80h84gi0d0ja1ssm26b9cg', 'cge3qta3mt0id9cve012dtgc24', 'uhm1cm7jip67udg8bplo4cdf5k', 'rie7j5phc77ije8gvv3vklbu6k', 'j79si7c619atkib428h6or03u8', 'b62jap1ve80nttr64eusqrppc8', 'r1jglqdcmre8b0p23aeer2irkg', 'ulhcm5aiem4u83pvc8nvg3lhag', '4gfc1l8let6fd6d34tt0g2vcc0', 'iam4sb1tk6fq0a63b45ada9au0', 'l0d6i39shbj0a71gb3a6qg2ogg', '794s3ucm7jkncucbg73n7hd834', 'jugn8nliv3cmch5u60g8593604', 'vtm9kri34t6okclcba0q44srnk', '92dfajouec6r6devfbt09vdovk', '76707qjavpj1n22k9634i8tlts', 'h9teg661u6rd1eu229uf2ek9qs', '5lfcjk47kevfpqqrc1nat958ds', 'l90o8lnfg04fgldv5g7df7mm2c', 'qcamt3jfolehjsi8gfgkqstpsc', 'udpgvbv35sgm8i7h5s42v4d0j8', 'fa8rs7kqd49b2qgvv8n2ih2iqk', 'vkjul93l9si5arj5q49418tajk', 'csgc87dj3fk9mr8ebdeil2kn6o', 'lb197e1bqmg030h93nrb975avg', 'aeqqqsdc4kuqr63ircepkiphog', 'bseilfokdt3pkarhssngupccio', '02gq4vaao1ehen8b94ld27j4t0', 'gu83n8a26dn962100jp1atvfsc', '5u54nt75ganhh1hi6ioc8gmvv0', '35hvef1hemmj20ot025ful7i6c', 'u0gi50q5tt4ccuttpat9gamaes', '1ajaha53bjgcomah556at6h0ks', 'g5o71al50fcbtn066ki9r9le68', 'lgnhlu6t2m4dckbjji54c4b1ko', 'umuncnuorvkc9qrvoboj94frc8', 'h64bhnknejccjl1jcqk09isdtg', 'qlbfpamc6unijbms5j88k0omv8', 'hm4s0p671hh4u4uo6kbqciufpc', 'q5jva4q8f5ii2fkku7fs6407pc', '9erg19g7v8gflq5vuu99ab65fs', '9r77joummd2pb3gmv3shdlmqkc', 'mntiobleir9mg6260qin9sitgo', 'kkgcmegp3sa7vb773ej9c1degk', 'o1hn5ifqtt5u1ga35k0kkt6ras', 'et70moli4chjekgnae5t0vi1e8', 'tssnockkg023t8fs7ljvev7ji0', 'avd55uf55qrce2ve4thu9hpkbg', 'h9lk6s4al3mblm9sne7shqhidg', 'et9jejs9tl0ab7jo31v5gcpvm0', 'mbree4sfakr0b00ddbjtgol2qk', 'rnug613c1fdruv4odeqllladmo', '1udau7qg5582lta6ks6c4ddf70', '733touhdvsighgns15mfpfutak', '8np1ktkjd48rb0a0dvcs7bnogk', 'mn8if867sm8ll8cd07ugsmv2vc', 'lt612bmavmihrnloe0dtjagf5s', 'mb1rphbdnlbtfisabv04m49o68', '345lm8m0cohvst5nrsb6sc64nk', 'bhovhouhephfp7ht32c2j570g4', '8ne3n7uh08orfq4gpc427hhmvs', 'bn1hcnp7i2f9i1saqctl60e3lo', '637lqqdaubc45knv50l8s00klg', 'smsb0qqkic3pn8hv06dbbb44fo', 'r77phchnaq5kl9v1q2avibubf8', '8lh1h8ka5ptc9chlo2vuovirhg', '5ap23o4dv3ju3vpatkkiqe2sm0', 'bva348e6v8fuhkd2b7gl0getvk', 'vnqmrkgpfn00acqorcl41i3kb4', 'stmh0nt3u5i3esphhdq800tngo', '1vg77a5bk132b52fsf0m5rq96c', '7q4teeogs850nfliqukvcrk11c', '64toatgoqahuad6gs4v99igdtk', '0it8hlh4pkdl88111m6lkmjhu8', 'okgeurn2hljehpd8qoj94t3j8o', 'tl5dci76b4komtt30v8fs19m94', '6mi0grvf90udbkhafvg5vtt1ic', '0ae926dvc4ovddue3i6gtolki4', 'msra1lfc50it368m7lepugg81g', 'tdagvsp4thqgkauktqnucfbjgg', 'apdho71nq7agt8n9dt9vthg1v4', 'l49thak4mj31dkvgi38i40go94', 'l2ui4548riufa1e3655elv2i1s', 'fgn7a5ptf9i5bk3is2d9i6qroo', '98gdprqaurrgvjc58erbv88ens', 'cs6adnpusqkdj9ptb31cirm6b0', 'p1889g8d2ucbdf09fdid96fbk0', 'p5nefnurp0fubhgbltv3gpi8bs', '57080cfoh1mqoqiabke1uujk3g', 't7uaslch3t9hlagfnlju0s3o78', 'enfvmfgk2hbgvduju8b26ve62s', '5921o9pk8mn48g5fd6kd95lrpo', '6iof977turlb043pjl4uslarhk', 'q1ugp3q33jj5eldql00r17namk', 'ckd448l8cvk54ijeojkovblbos', 'l8e3h3i26j1b1cpjb9kitvad3c', '7ibnb06p96a227ldqgno7e71p8', '2st022ue2e7lh32hp5m9ln0j5s', '78fji0e7dti2itplmbkdtmq1v4', 'uc0cjjdn4l9l4i2t3ol27dcl48', 'a16s5fjsfoml4tetohnurucukk', 'pqn3u2445vdht83n5qg0abq7vc', '4c31j2ijn5i6v62fpk9qii3ud0', '5ldujlrvgbtv3jcqfopvcg99rs', 'gpjsekjh3o47f8ioi0p31gegf8', 'qt5i7c5bjrsb9tm3impugpspfg', '5n5pcl1olh4qe74ti89jc7st4o', 'odo6pdap9j6uqj6t8uek6trbvo', 'v6mcq1kfu28n1ur7ko0t7cn3ug', 'si1g379vua3525nbo4vieiprgk', 'ng3gkl2682ss3tshkdetdhf63c', '073d859pj2s6o9qcl1jpnm5kpc', 'f3ov26hgv934jf5gd4up2snn4g', 'urc8947ckg536ipt57n1uk8nsg', 'bqlqcubcjqiubas1bduha8qabs', 'ug3b3r48ef2pgf5prfr6kpi3fg', 'pcjua6oklbbqhje54nnpjdffcg', 'tenbjr5dm553agecr862oubjgc', 'tiiflgk70356m2ckc19o3amcqo', '9kftr5hnjj51h3ap35fvhvd6ms', 's9f11911b00v463qkq748tvvag', '8jrtqtj184v96gevguc4cd2tc8', '1gcp7a2ncc2ltj6qio13v6n2n8', 'd9qch66ods1gkrigtk8e283c7g', 'rh5qtaie47icpjcpp9svjrc0rk', '7bdcrr58b9hecst71b06utlnm4', 'tqbgejgi29khgmp2c2o4f65pb4', 'm2ft00dtb61ohvqr9t4tjp5m60', '6bp5s6dmon1da4bllt9ptlgpak', 'vpihekdtng1anbvka8nvj2dgc8', 'pgpcvn7vshnifkkbn2m85up954', 'tf1il50rvlbvn7ebcvbmvnbfa8', 'pfkbc6do0mrv0s0ivr0bj5lis4', 'rb5vrrpnlga8d6q5v0uvt41irg', 'u4tofrm1n7nu4e5rjjb8uluq68', 'ceqs6nqf3idqf2nlerspk2sp8g', '7cdbs24uffn5asleus8f9iuiv4', 'c9s7e3b83pnep1aq2dp196qjvg', 'lte287abta55eq3ehvtd55rj0o', 'g3fma2oo18i15d31c9l0gfmtq0', 'heqab28gbtslgb6hhet348a5p8', 'mub71mlhsm9buoudodc5rjfu40', 'gsb7o93i8ahm197p6ca7mpi990', '4p5f1027lb2cjath4k2dace99k', 'vck3hq4hn5ip92k08ocq6cual8', 'v4mod527t0o624eq09j5t32na0', 'ohice6pa9gi2gka2juhesnh0ho', 'lm0icofbt1fmh356iepovm3mr8', '7ggsrta8ikog2o7soock3o7i38', '14q5n5le38flffrgp91gb4cm5s', '3nf5q7qql822d3lrhusirsadtg', 'r0anfgb25p5ci12uohs792i0ck', '0lu4nvvbd026jhbi49dlas93hk', '52vbl7q58v3kd64lh7qik9mq04', 'p8t33jrdsmerqg9jo7mdc842gg', 'ue0dga3gt7fohm7h7peagc07uc', 'buru7keb98idija6cdv4madme8', '3qjv7o1hjvhed1prg975icgrvg', 'kqfd4aqvadoidmoevrqq1mgf10', 'vfu60m76l5rvk4ho3h93fcf3c4', 'hijqhd7n4scjg52iqa9ip2rmao', '485e137gjjl24el8l5nm4lla2c', 'sq5ssp2moa6rbvm9i2so2dkc54', '5b68jqlu3tt9ce149377791h8s', 'mj7uec5bs3jg81lqmijl5f9t30', 'vsgurbjjguqnsiuujcf0420jgk', 'svnbup99t7atjh23rgc0opnvjg', 'aec3ciuhmus3qeaufk64bokj00', 'a9prkks18t9bnmdob8nqqs765g', '876pb7chlhi8o8dpe2jllqfdn4', 'iii73j9erpdjaurfajjandgrg8', 'ubn6fn2n1nfg567bnqja2u2bmg', 'b2aeld27alej7un3or3r2bn6cs', 'hdmmm6uv45ppf96cgo5dqr6ilo', '6q16fhjrpf3fdsustllcfku24k', 'p5lrh80p65dkmje3bhdi4r4l7o']

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
            # Check joystick input
            joystick_input = check_joystick()
            if joystick_input != 0:
                init_joystick()
            if joystick_input == 1:  # Left
                self.TryMove(-1, 0)
            elif joystick_input == 2:  # Right
                self.TryMove(1, 0)
            elif joystick_input == 3:  # Up
                self.TryRotate()
            elif joystick_input == 4:  # Down
                self.TryMove(0, 1)
            
            self.Tick()
            self.Render()



def main():
    """Main game loop"""
    game = Tetris()
    
    # Just run the tick loop directly - it now handles joystick input
    game.tick_loop()


if __name__ == "__main__":
    main()

