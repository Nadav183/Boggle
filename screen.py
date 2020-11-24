from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox


class Screen:
    '''Game Vars'''
    # These variables are the basis of the game, and will not be changed by
    # settings

    # Screen proportions
    MAIN_SPLIT = 0.15  # split between Top and Bottom frames
    BOTTOM_SPLIT = 0.75  # Split between Game_Window and Player_HUD

    # Dictionary to locate adjacent keys for an item
    ADJACENT_KEYS = {
        'up': lambda location: (location[0] - 1, location[1]),
        'down': lambda location: (location[0] + 1, location[1]),
        'left': lambda location: (location[0], location[1] - 1),
        'right': lambda location: (location[0], location[1] + 1),
        'diag_ul': lambda location: (location[0] - 1, location[1] - 1),
        'diag_ur': lambda location: (location[0] - 1, location[1] + 1),
        'diag_dl': lambda location: (location[0] + 1, location[1] - 1),
        'diag_dr': lambda location: (location[0] + 1, location[1] + 1)
    }

    '''Messages'''
    # Text to be displayed on the starting screen
    INITIAL_TEXT = 'Welcome to our boggle game, press start to display board'
    RETRY_LABEL = 'Press Start to start again'

    # Displays at the end of the countdown
    COUNT_MESSAGE = 'Good Luck!'

    # Text to be displayed on the ending screen
    END_TITLE = 'You managed to find {} words!'
    # Display the player's score
    END_SCORE = 'Your total score is: {}'

    # These are the Messagebox messages for all outcomes of the game
    TIMEUP_TITLE = 'Time\'s Up!'
    TIMEUP_TEXT = 'The clock has run out!\nLet\'s see how you did'
    EARLY_TITLE = 'QUITTER ALERT!'
    EARLY_TEXT = 'The clock did not run out!\nYOU ARE FREAKING WEAK!!!'
    AFTER_TITLE = 'Going so fast?'
    AFTER_TEXT = 'Don\'t you want to play again?'
    DEFAULT_PIC = 'default'

    # A dictionary to determine which message to show on exit
    ENDERS = {
        'TIMEUP': (TIMEUP_TITLE, TIMEUP_TEXT),
        'EARLY': (EARLY_TITLE, EARLY_TEXT),
        'AFTER': (AFTER_TITLE, AFTER_TEXT)
    }

    SETTING_ERR = ('Game is running!', 'You can\'t change settings midgame!')

    '''Visual Default Settings'''
    # These are the default visual settings for the game, the player has an
    # Option to change some of these from within the game

    # Default font for all text in the game
    FONT = 'Helvetica'
    # Font sizes dictionary
    SIZES = {
        'small': (FONT, 10),  # Used for buttons
        'medium': (FONT, 15),  # Used for non-title text
        'large': (FONT, 20),  # Used for titles
        'gigantic': (FONT, 70)  # Used for special text
    }
    # Holds sequences of 9 colors that represent a theme
    THEME = {
        'DEFAULT': ('#FBCE3A', '#E0D0B8', '#E0D0B8',
                    '#372F2F', '#FBCE3A', '#372F2F',
                    '#FBCE3A', '#372F2F', '#FBCE3A')
    }
    # holds path for specific reactions for words
    PICS = {
        'wrong': "pics/wrong_word.png",
        'random': "pics/random_word.png",
        'unknown': 'pics/unknown_word.png',
        'impressive': 'pics/impressive.png',
        'basic': 'pics/basic.png',
        'default': 'pics/good_luck.png',
        'recycle': 'pics/recycling.png'

    }
    RANDOM_WORDS = ['AA', 'AAH', 'AAL', 'AAS', 'AB', 'ABA', 'AX']
    # The the theme chosen by the player (can be altered in settings)
    CHOSEN_THEME = 'DEFAULT'
    TOP_BAR_COLOR = THEME[CHOSEN_THEME][0]  # Background for top frame
    GAME_WINDOW_COLOR = THEME[CHOSEN_THEME][1]  # Background for game window
    PLAYER_HUD_COLOR = THEME[CHOSEN_THEME][2]  # Background for player HUD
    BUTTONS_BG = THEME[CHOSEN_THEME][3]  # Background for buttons
    BUTTONS_FG = THEME[CHOSEN_THEME][4]  # Text color for buttons
    TILE_BG = THEME[CHOSEN_THEME][5]  # Background for board tiles
    TILE_FG = THEME[CHOSEN_THEME][6]  # Text color for board tiles
    BOX_BG = THEME[CHOSEN_THEME][7]  # Background for leaders\found words
    BOX_FG = THEME[CHOSEN_THEME][8]  # Text color for leaders\found words

    # The base padding for all items on screen - Not alterable
    PAD = 5

    '''Default Game Settings'''
    # The length of the game - can be changed in settings
    GAME_TIME = 180
    COUNTDOWN = 3

    def __init__(self):
        self.__init_vars()
        self.__init_screen()  # Creates all the screen components

    def __init_vars(self):
        self.__score = 0  # Player's score
        self.__bank = []  # Words found by the player
        self.__curr_word = ''  # The word the player is currently forming
        self.clock_running = False  # The state of the clock
        self.__player = ''  # The players name
        self.__game_status = False  # determines whether a game should end
        self.press_bank = []  # Letters the player clicked on
        self.stopclock = False  # Should the clock be stopped

        self.score_bank = {}

    def __init_screen(self):
        '''
        This function creates the main game screen and base variables
        associated with it
        '''
        self.__root = Tk()  # The base screen
        # Get's the user's screen size so the game screen size will be
        # relative
        self.screen_width = self.__root.winfo_screenwidth() // 2
        self.screen_height = self.__root.winfo_screenheight() // 2

        # sets a minimum size for the game screen
        self.__root.minsize(width=self.screen_width + 180,
                            height=self.screen_height + 120)

        # Initiates the topleven menu
        self.toplevel_menu()
        # Adds the top frame
        self.top_frame()
        # Adds the bottom frame
        self.bottom_frame()

    '''Base Methods'''

    def set_title(self, title):
        self.__root.title(title)

    def set_dict(self, dict):
        # Should be in boggle.py
        self.__dict = dict

    def set_board(self, board):
        # Should be in boggle.py
        self.__board = board

    def start_screen(self):
        self.__root.mainloop()

    def set_game_status(self, status):
        self.__game_status = status

    '''Toplevel Menu Methods'''

    def toplevel_menu(self):
        menubar = Menu(self.__root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Options", command=self.options)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.forcexit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.__root.config(menu=menubar)

    def forcexit(self):
        if self.clock_running:  # user ends early
            self.stopclock = True
            self.end(type='EARLY')
        else:  # game is over
            self.__game_status = 'exit'

    '''Options window methods'''

    def options(self):
        if self.clock_running:
            tkinter.messagebox.showinfo(self.SETTING_ERR[0],
                                        self.SETTING_ERR[1])
            return
        # Creating the toplevel window
        self.menu = Toplevel()
        self.menu.title('Options')
        # Adding the save button
        self.save_button = ttk.Button(self.menu, text="Save Settings",
                                      command=self.options_save)
        self.save_button.pack(side=BOTTOM, padx=self.PAD, pady=self.PAD)
        # Creating the containing notebook for the setting tabs
        self.menu_note = ttk.Notebook(self.menu, height=200,
                                      width=250, padding=self.PAD)
        self.menu_note.pack(side=TOP, fill='both', expand=True)
        self.game_settings_window()  # Creates the Game_Settings Tab
        # self.visual_settings_window()  # Creates the Visual Settings Tab

    def options_save(self):
        # Setting the game time
        self.GAME_TIME = (self.time_min.get()) * 60 + self.time_sec.get()
        self.COUNTDOWN = self.countdown_duration.get()
        self.update_text()

        # Closing the Options menu after saving the changed settings
        self.menu.destroy()

    '''Game Settings Methods'''

    def game_settings_window(self):
        # Making the notebook Tab for game settings
        self.game_settings = ttk.Frame(self.menu_note)
        self.menu_note.add(self.game_settings, text='Game Settings')
        self.gametime()  # adding the game duration setting option
        self.countdown_timer()

    def gametime(self):
        # Container Frame for the Game Duration setting
        self.gametime_frame = ttk.Frame(self.game_settings)
        self.gametime_frame.pack(side=TOP)

        # The label for the duration setting
        self.gametime_title = ttk.Label(self.gametime_frame,
                                        text="Game Duration:")
        self.gametime_title.pack(side=LEFT)

        # Making two IntVar objects that will hold the minutes and the seconds
        # Chosen by the player in the settings menu
        self.time_min = IntVar(self.gametime_frame)
        self.time_sec = IntVar(self.gametime_frame)
        # Making the options menus for the minutes and seconds
        self.option_minutes = ttk.OptionMenu(self.gametime_frame,
                                             self.time_min,
                                             0, *range(11))

        # Setting a default value for minutes
        self.time_min.set(self.GAME_TIME // 60)
        self.option_minutes.pack(side=LEFT)
        self.option_seconds = ttk.OptionMenu(self.gametime_frame,
                                             self.time_sec,
                                             0, *range(0, 60, 5))
        # Setting a default value for minutes
        self.time_sec.set(self.GAME_TIME % 60)
        self.option_seconds.pack(side=LEFT)

    def countdown_timer(self):
        # Container Frame for the countdown timer setting
        self.countdown_timer_frame = ttk.Frame(self.game_settings)
        self.countdown_timer_frame.pack(side=TOP)

        # The label for the countdown timer setting
        self.countdown_timer_title = ttk.Label(self.countdown_timer_frame,
                                               text="Timer Duration:")
        self.countdown_timer_title.pack(side=LEFT)

        # Making an IntVar object that will hold the duration length
        self.countdown_duration = IntVar(self.countdown_timer_frame)
        # Making the options menus for the minutes and seconds
        self.countdown_options = ttk.OptionMenu(self.countdown_timer_frame,
                                                self.countdown_duration,
                                                0, *range(6))
        self.countdown_duration.set(self.COUNTDOWN)
        self.countdown_options.pack(side=LEFT)

    '''Visual Settings Methods'''

    def visual_settings_window(self):
        # Making the notebook Tab for visual settings
        self.visual_settings = ttk.Frame(self.menu_note)
        self.menu_note.add(self.visual_settings, text='Visual Settings')

    ''' Top Frame Methods'''

    def top_frame(self):
        # Creates the containing frame
        self.top = Frame(self.__root, bg=self.TOP_BAR_COLOR)
        self.top.place(rely=0, relheight=self.MAIN_SPLIT, relwidth=1.0)

        self.start_button()  # Creates the Start\Check button
        self.forming_word()  # Creates the forming word box
        self.clock()  # Creates the clock

    def start_button(self):  # creates start button
        self.main_button = Button(self.top,
                                  text='Start', font=self.SIZES['small'],
                                  command=self.start, fg=self.BUTTONS_FG,
                                  bg=self.BUTTONS_BG, width=10)
        self.main_button.pack(side=LEFT, padx=self.PAD)

    def forming_word(self):
        # Creates the forming word container box
        self.forming_word_container = Frame(self.top, bg=self.TOP_BAR_COLOR)
        self.forming_word_container.pack(side=LEFT, padx=self.PAD)
        # Creates the forming word static title
        self.forming_word_title = Label(self.forming_word_container,
                                        text=f'Forming Word:',
                                        font=self.SIZES['small'],
                                        bg=self.TOP_BAR_COLOR)
        self.forming_word_title.pack(side=LEFT, padx=self.PAD)
        # Creates the forming word dynamic label
        self.forming_word = Label(self.forming_word_container,
                                  text=f'{self.__curr_word}',
                                  font=self.SIZES['large'],
                                  bg=self.TOP_BAR_COLOR)
        self.forming_word.pack(side=LEFT, padx=self.PAD)

    def clock(self):
        t = divmod(self.GAME_TIME, 60)
        self.clock_label = Label(self.top, font=self.SIZES['large'],
                                 bg=self.TOP_BAR_COLOR,
                                 text=f'{t[0]:0>2}:{t[1]:0>2}',
                                 bd=1, relief=SUNKEN)
        self.clock_label.pack(side=RIGHT, padx=self.PAD)

    ''' Bottom Frame Methods'''

    def bottom_frame(self):
        # Main Frame
        self.bottom = Frame(self.__root)
        self.bottom.place(rely=self.MAIN_SPLIT,
                          relheight=(1.0 - self.MAIN_SPLIT),
                          relwidth=1.0)
        self.game_window()
        self.player_hud()

    def game_window(self):
        self.game_window = Frame(self.bottom, bg=self.GAME_WINDOW_COLOR)
        self.game_window.place(relx=0, relheight=1.0,
                               relwidth=self.BOTTOM_SPLIT)
        self.initial_label = Label(self.game_window,
                                   bg=self.GAME_WINDOW_COLOR,
                                   text=self.INITIAL_TEXT,
                                   font=self.SIZES['large'],
                                   wraplength=self.screen_width // 2,
                                   justify=CENTER)
        self.initial_label.pack(expand=True)

    def player_hud(self):
        # Right Subframe - Player HUD
        self.player_hud = Frame(self.bottom, bg=self.PLAYER_HUD_COLOR)
        self.player_hud.place(relx=self.BOTTOM_SPLIT,
                              relheight=1.0,
                              relwidth=1.0 - self.BOTTOM_SPLIT)
        self.score_section()

        # Holds the found words and leaderboards frames for enduser size
        # control
        self.pane = PanedWindow(self.player_hud, orient=VERTICAL)
        self.pane.pack(side=TOP, fill='both', expand=True, pady=self.PAD,
                       padx=self.PAD)
        self.found_words_section()
        self.imageframe = Frame(self.player_hud,
                                bg=self.PLAYER_HUD_COLOR,
                                height=50,
                                relief=SUNKEN,
                                bd=3)
        self.imageframe.pack(side=BOTTOM, fill='both', expand=True,
                             padx=self.PAD, pady=self.PAD)
        self.put_picture(self.DEFAULT_PIC)  # adds default picture

    def score_section(self):
        # Score display
        self.score_container = Frame(self.player_hud, bg=self.BOX_BG)
        self.score_container.pack(side=TOP, pady=self.PAD, padx=self.PAD,
                                  fill=X)
        self.score_title = Label(self.score_container,
                                 text='Score:',
                                 bg=self.BOX_BG,
                                 fg=self.BOX_FG,
                                 font=self.SIZES['small'])
        self.score_title.pack(side=TOP, fill=X)

        self.score_label = Label(self.score_container,
                                 text=f'{self.__score}',
                                 bg=self.BOX_BG,
                                 fg=self.BOX_FG,
                                 font=self.SIZES['small'])
        self.score_label.pack(side=TOP, fill=X)

    def found_words_section(self):
        # Found Words
        self.bank_container = Listbox(self.pane,
                                      bg=self.BOX_BG,
                                      fg=self.BOX_FG,
                                      font=self.SIZES['small'])
        self.pane.add(self.bank_container)
        self.bank_container.insert(END, 'Found Words:', '')
        self.scrollbar = ttk.Scrollbar(self.bank_container, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.bank_container.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.bank_container.yview)

    '''General gameplay - Most should move to boggle.py'''

    def end(self, type='TIMEUP'):
        self.end_frame = Frame(self.game_window, bg=self.GAME_WINDOW_COLOR)
        self.end_frame.pack(expand=True)
        self.main_button.config(state=DISABLED)
        tkinter.messagebox.showinfo(self.ENDERS[type][0],
                                    self.ENDERS[type][1])
        self.board_frame.pack_forget()
        self.end_title = Label(self.end_frame,
                               text=self.END_TITLE.format(len(self.__bank)),
                               bg=self.GAME_WINDOW_COLOR,
                               font=self.SIZES['large'])
        self.end_title.pack(side=TOP, fill=X, expand=True)

        self.end_score = Label(self.end_frame,
                               text=self.END_SCORE.format(self.__score),
                               bg=self.GAME_WINDOW_COLOR,
                               font=self.SIZES['large'])
        self.end_score.pack(side=TOP, fill=X, expand=True)
        self.buttonframe = Frame(self.end_frame, bg=self.GAME_WINDOW_COLOR)
        self.buttonframe.pack(side=TOP, padx=self.PAD, pady=self.PAD)

        self.exitbtn = ttk.Button(self.buttonframe,
                                  text='Exit',
                                  command=lambda: self.set_game_status(
                                      'exit'))
        self.exitbtn.pack(side=LEFT)
        self.retrybtn = ttk.Button(self.buttonframe,
                                   text='Retry',
                                   command=lambda: self.set_game_status(
                                       'retry'))
        self.retrybtn.pack(side=LEFT)

    def tick_clock(self, time):
        if not self.clock_running:
            self.clock_running = True
        t = divmod(time, 60)
        now = f'{t[0]:0>2}:{t[1]:0>2}'
        self.clock_label.config(text=now)
        if self.stopclock:
            self.clock_running = False
            return
        elif time == 0:
            self.clock_running = False
            self.end()
        else:
            time -= 1
            self.__root.after(1000, self.tick_clock, time)

    def get_game_status(self):
        return self.__game_status

    def get_root(self):
        return self.__root

    def countdown(self, counting):
        if counting == 'start':
            counting = self.COUNTDOWN
            self.initial_label.pack_forget()
            if counting == 0:
                self.display_board()
                self.tick_clock(self.GAME_TIME)
                self.main_button.config(text='Check')
                return
            self.countdown_frame = Frame(self.game_window)
            self.countdown_frame.pack(expand=True)
            self.countdown_label = Label(self.countdown_frame,
                                         text=counting,
                                         font=self.SIZES['gigantic'],
                                         bg=self.GAME_WINDOW_COLOR,
                                         justify=CENTER)
            self.countdown_label.pack(expand=True)
            self.__root.after(1000, self.countdown, counting)
        elif counting > 1:
            counting -= 1
            self.countdown_label.config(text=counting)
            self.__root.after(1000, self.countdown, counting)
        elif counting == 1:
            self.countdown_label.config(text=self.COUNT_MESSAGE)
            counting -= 1
            self.__root.after(1500, self.countdown, counting)
        else:
            self.countdown_frame.pack_forget()
            self.display_board()
            self.tick_clock(self.GAME_TIME)
            self.main_button.config(text='Check')

    def update_bank(self):
        self.__bank.append(self.__curr_word)
        self.bank_container.insert(END, self.__curr_word)

    def check_word(self, undo=False):
        key = self.picture_key(self.__curr_word)
        if not undo:  # makes sure not to affect image if just unclicking
            if self.image:  # forgets if image is there
                self.image.pack_forget()
            Screen.put_picture(self, key)
        if (self.__curr_word in self.__dict) and (self.__curr_word not in self.__bank):
            self.__score += len(self.__curr_word) ** 2
            self.score_label.config(text=f'{self.__score}')
            self.update_bank()

    def clear_word(self, undo=False):
        self.check_word(undo)
        self.__curr_word = ''
        self.press_bank = []
        self.forming_word.config(text=f'{self.__curr_word}')
        for loc in self.__board:
            self.buttons[loc].config(state=NORMAL)
            if self.__board[loc].get_status():
                self.__board[loc].press()

    def add_letter(self, letter):
        self.__curr_word += letter.get_data().upper()
        self.forming_word.config(text=f'{self.__curr_word}')

    def press(self, location, re=False):
        if self.__board[location].get_status():
            if len(self.press_bank) == 1:
                return self.clear_word(True)
            else:
                self.__board[self.press_bank.pop()].press()
                self.__board[self.press_bank[-1]].press()
                return self.press(self.press_bank.pop(), re=True)
        self.press_bank.append(location)
        items = [self.ADJACENT_KEYS[key](location)
                 for key in self.ADJACENT_KEYS]
        # objects = [self.board[item] if item in self.board for item in items]
        self.__board[location].press()
        # self.buttons[location].config(state=DISABLED)
        for i, j in self.buttons:
            if (i, j) == location:
                self.buttons[(i, j)].config(state=NORMAL)
                continue
            if (i, j) in items:
                if self.__board[(i, j)].get_status():
                    self.buttons[(i, j)].config(state=DISABLED)
                else:
                    self.buttons[(i, j)].config(state=NORMAL)
            else:
                self.buttons[(i, j)].config(state=DISABLED)
        if re:
            self.__curr_word = self.__curr_word[:-1]
            self.forming_word.config(text=f'{self.__curr_word}')
            return
        return self.add_letter(self.__board[location])

    def display_board(self):
        # makes a frame for the game tiles
        self.board_frame = Frame(self.game_window,
                                 bg=self.GAME_WINDOW_COLOR)
        self.board_frame.pack(expand=True)

        self.buttons = {}  # dictionary that will hold the buttons
        # makes the buttons based on the game board
        for i, j in self.__board:
            self.buttons[(i, j)] = (
                Button(self.board_frame,
                       text=str(self.__board[(i, j)]),
                       command=lambda item=(i, j): self.press(
                           item),
                       font=self.SIZES['large'],
                       width=5,
                       height=2,
                       fg=self.TILE_FG,
                       bg=self.TILE_BG))
            # places each tile in a grid
            self.buttons[(i, j)].grid(row=i, column=j,
                                      padx=self.PAD, pady=self.PAD)

    def picture_key(self, word):
        """
        returns appropriate key for picture
        """
        if word not in self.__dict:
            return 'wrong'
        if word in self.__bank:
            return 'recycle'
        if word in Screen.RANDOM_WORDS:
            return 'random'
        if len(word) <= 3:
            return 'basic'
        if len(word) <= 8:
            return 'impressive'
        return 'unknown'

    def put_picture(self, dic_key):
        """
        adds picture to the screen
        """
        path = Screen.PICS[dic_key]
        photo = PhotoImage(file=path)
        photo = photo.subsample(1, 1)
        self.image = Label(self.imageframe, image=photo, borderwidth=0,
                           highlightthickness=0, bg=self.PLAYER_HUD_COLOR)
        self.image.image = photo
        self.image.pack(side=BOTTOM, padx=self.PAD,
                        pady=self.PAD, expand=True, fill='both')

    def start(self):
        if self.clock_running:
            self.clear_word()
        else:
            self.countdown('start')

    def update_text(self):
        t = divmod(self.GAME_TIME, 60)
        self.clock_label.config(text=f'{t[0]:0>2}:{t[1]:0>2}')
        self.forming_word.config(text=f'{self.__curr_word}')
        self.score_label.config(text=f'{self.__score}')
        self.bank_container.delete(2, END)
        self.image.pack_forget()
        self.put_picture(self.DEFAULT_PIC)

    def reset_screen(self):
        self.end_frame.pack_forget()
        self.initial_label.config(text=self.RETRY_LABEL)
        self.initial_label.pack(expand=True)
        self.__init_vars()
        self.update_text()
        self.main_button.config(text='Start', state=NORMAL)
