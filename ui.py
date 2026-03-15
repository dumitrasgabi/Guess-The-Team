import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from game import Game
import pygame
import random

pygame.mixer.init()

CUSTOM_COLORS = {
    "burgundy": "#800020",
    "maroon": "#800000",
    "navy": "#000080",
    "gold": "#FFD700",
    "silver": "#C0C0C0",
    "sky blue": "#87CEEB",
    "beige": "#F5F5DC",
    "lime": "#32CD32",
    "amber": "#FFBF00"
}

def get_color(color_name):
    return CUSTOM_COLORS.get(color_name.lower(), color_name)


class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {
            "defeat": pygame.mixer.Sound("assets/sounds/defeat.mp3"),
            "victory": pygame.mixer.Sound("assets/sounds/victory.mp3"),
            "click": pygame.mixer.Sound("assets/sounds/click.mp3"),
            "hover": pygame.mixer.Sound("assets/sounds/hover.mp3")
        }

    def play(self, sound_name):
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()

    def play_menu_music(self):
        pygame.mixer.music.load("assets/sounds/menu_music.mp3")
        pygame.mixer.music.play(-1)  # loop forever
        pygame.mixer.music.set_volume(0.5)  # 0.0 - 1.0

    def play_level_music(self):
        pygame.mixer.music.load("assets/sounds/Pufino_Syndicate.mp3")
        pygame.mixer.music.play(-1)  # loop forever
        pygame.mixer.music.set_volume(0.5)  # 0.0 - 1.0

    def stop_music(self):
        pygame.mixer.music.stop()


class GuessTheTeam:
    # ---------------- INIT ----------------
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.root.title("Guess The Team")
        self.sound = SoundPlayer()
        self.timer_running = False
        self._just_selected = False

        self.selected_continents = []
        self.selected_countries = []
        
        # COLORS AND FONTS
        self.fg_color = "#ffffff"
        self.highlight_color = "#001e4f"
        self.font_family = "Minecraft"
        
        self.minecraft_font = tkfont.Font(
            family="Minecraft",
            size=11
        )
        
        style = ttk.Style(self.root)
        style.theme_use("default")
        
        style.configure(
            "Minecraft.TCombobox",
            font=("Minecraft", 11),
            foreground="white",
            background="#1a1a1a",
            borderwidth=1,
            relief="solid"
        )
        
        style.map(
            "Minecraft.TCombobox",
            fieldbackground=[("readonly", "#1a1a1a"), ("!readonly", "#1a1a1a")],
            foreground=[("readonly", "white"), ("!readonly", "white")],
            selectbackground=[("!disabled", "#3a86ff")],
            selectforeground=[("!disabled", "white")]
        )
        
        style.configure(
            "Minecraft.TCombobox.Listbox",
            font=("Minecraft", 11),
            background="#1a1a1a",
            foreground="white",
            selectbackground="#3a86ff",
            selectforeground="white",
            borderwidth=1,
            relief="solid"
        )
        
        style.configure(
            "Minecraft.TCombobox.arrow",
            background="#1a1a1a",
            bordercolor="#1a1a1a"
        )
        
        # LOAD IMAGES
        self.spr_bck_menu = ImageTk.PhotoImage(Image.open("assets/images/menu.png").resize((1920, 1080)))
        self.spr_bck_2 = ImageTk.PhotoImage(Image.open("assets/images/bck2.jpg").resize((1920, 1080)))
        self.spr_bck_level = ImageTk.PhotoImage(Image.open("assets/images/bck_chat.png").resize((1920, 1080)))
        self.spr_bck_result = ImageTk.PhotoImage(Image.open("assets/images/bck_result.png").resize((1920, 1080)))
        self.spr_robot = ImageTk.PhotoImage(Image.open("assets/images/robot.png").resize((440, 440)))
        self.spr_clock = ImageTk.PhotoImage(Image.open("assets/images/clock.png").resize((250, 250)))
        self.spr_history_bubble = ImageTk.PhotoImage(Image.open("assets/images/history.png").resize((720, 540)))
        self.spr_entry = ImageTk.PhotoImage(Image.open("assets/images/question_entry.png").resize((620, 100)))

        self.difficulty = tk.StringVar(value="Penalty Merchant (60\")")
        self.difficulty_times = {
            "Haram Baller (240\")": 240,
            "Tap-In Merchant (120\")": 120,
            "Penalty Merchant (60\")": 60,
            "GOAT (30\")": 30
        }

        self.root.geometry("1920x1080")
        self.show_menu()

    # ---------------- CLEAR SCREEN ----------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- SHOW MENU ----------------
    def show_menu(self):
        sp = SoundPlayer()
        if not pygame.mixer.music.get_busy():
            sp.play_menu_music()

        self.clear_screen()

        # BACKGROUND
        canvas = tk.Canvas(
            self.root,
            width=1920,
            height=1080,
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=self.spr_bck_menu, anchor="nw")

        # TITLE
        canvas.create_text(
            960, 140,
            text="Guess The Team",
            fill="white",
            font=(self.font_family, 50, "bold")
        )

        # DIFFICULTY
        canvas.create_text(
            960, 350,
            text="Difficulty",
            fill="#cccccc",
            font=(self.font_family, 20, "bold")
        )

        difficulty_box = ttk.Combobox(
            self.root,
            textvariable=self.difficulty,
            values=list(self.difficulty_times.keys()),
            state="readonly",
            width=21,
            font=("Minecraft", 15),
            style="Minecraft.TCombobox"
        )
        
        self.root.update_idletasks()
        try:
            popdown = difficulty_box.tk.eval('ttk::combobox::PopdownWindow %s' % difficulty_box)
            if popdown:
                listbox = f"{popdown}.f.l"
                self.root.tk.call(listbox, "configure", "-font", ("Minecraft", 12))
                self.root.tk.call(listbox, "configure", "-background", "#1a1a1a")
                self.root.tk.call(listbox, "configure", "-foreground", "white")
                self.root.tk.call(listbox, "configure", "-selectbackground", "#3a86ff")
                self.root.tk.call(listbox, "configure", "-selectforeground", "white")
        except:
            pass
        
        difficulty_box.current(2)

        canvas.create_window(
            960, 395,
            window=difficulty_box,
            anchor="center"
        )

        # PLAY BUTTON
        play_button = tk.Button(
            self.root,
            text="Play",
            width=20,
            font=(self.font_family, 15),
            command=self.start_game
        )
        self.add_sound_to_button(play_button)

        canvas.create_window(
            960, 450,
            window=play_button
        )

        # FILTER BUTTON
        filter_button = tk.Button(
            self.root,
            text="Filter",
            width=20,
            font=(self.font_family, 15),
            command=self.select_filter
        )
        self.add_sound_to_button(filter_button)

        canvas.create_window(
            960, 500,
            window=filter_button
        )

        # HELP BUTTON
        help_button = tk.Button(
            self.root,
            text="Help",
            width=20,
            font=(self.font_family, 15),
            command=self.show_how_to_play
        )
        self.add_sound_to_button(help_button)

        canvas.create_window(
            960, 550,
            window=help_button
        )

        # CREDITS BUTTON
        credits_button = tk.Button(
            self.root,
            text="Credits",
            width=20,
            font=(self.font_family, 15),
            command=self.show_credits
        )
        self.add_sound_to_button(credits_button)

        canvas.create_window(
            960, 600,
            window=credits_button
        )

        # EXIT BUTTON
        exit_button = tk.Button(
            self.root,
            text="Exit",
            width=20,
            font=(self.font_family, 15),
            command=self.root.quit
        )
        self.add_sound_to_button(exit_button)

        canvas.create_window(
            960, 650,
            window=exit_button
        )

    # ---------------- SHOW HOW TO PLAY ----------------
    def show_how_to_play(self):
        self.clear_screen()

        # BACKGROUND
        canvas = tk.Canvas(
            self.root,
            width=1920,
            height=1080,
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.spr_bck_2, anchor="nw")

        # TITLE
        canvas.create_text(
            960, 100,
            text="How To Play",
            fill="white",
            font=(self.font_family, 36, "bold")
        )

        # TEXT
        how_to = (
            "OBJECTIVE: Ask the bot Yes/No questions to identify the mystery team. "
            "Keep your questions concise to save time—for example, type \"ucl\" instead of "
            "\"Has this team ever won a Champions League?\". If the bot does not recognize "
            "your input, it will respond with question marks.\n\n"
            
            "RECOGNIZED CATEGORIES:\n\n"
            
            "• CONTINENTS & ASSOCIATIONS: Europe (UEFA), Asia (AFC), Africa (CAF), "
            "North America (CONCACAF), South America (CONMEBOL), and Oceania (OFC).\n"
            "(Note: Associations follow competitive conventions. For example, Israel, Turkey, "
            "and Armenia are categorized under Europe/UEFA despite geographic locations.)\n\n"
            
            "• ZONES: Balkan(s), Iberia/Iberian Peninsula, Catalonia, Mediterranean, Baltic, "
            "West, East, North, South, Central, Scandinavia, Saxon, Roman/Latin, Island, "
            "Slavic, Arab, British, Middle East.\n\n"
            
            "• COUNTRIES: You may type specific country names for the bot to verify.\n\n"
            
            "• POPULAR LEAGUES: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, "
            "Eredivisie, Jupiler Pro League, Premiership, Super Lig, MLS, Liga MX.\n"
            "(Note: Data may not reflect real-time promotions/relegations; a team may be "
            "listed in a league based on recent historical data.)\n\n"
            
            "• COLORS: Refers to both Kit and Crest colors. If a team wears a specific color "
            "that isn't on the crest, it is still included (e.g. Valencia wears white). Supported: Black, White, Red, Blue, Green, "
            "Yellow, Orange, Amber, Pink, Cyan, Maroon, Claret, Burgundy, Gray, Brown, "
            "Purple, Gold, Silver, Navy, Lime, Beige.\n\n"
            
            "• LOGO FEATURES: Animal, wolf, dog, fox, lion, tiger, bear, eagle, falcon, hawk, "
            "dragon, horse, bull, bird, fish, dolphin, mythology, liver bird, seagull, "
            "crocodile, panther, rhino, star, moon, sun, stripes, checkers, wings, ball, "
            "ship, anchor, crown, royal, monogram, coat of arms, cross, shield, text, flag, "
            "circle, oval, diamond, human, Eiffel Tower, lily, cannon, devil, tree, power plant, "
            "hammer, letter(s), bee, squirrel, hand, castle, tower, halo, arrow, bat, sword, "
            "gryphon, pine, pinecone, church, flower, wheat, olive, sheep, train, fountain, "
            "clover, plant, corn, ribbon, harp, torch.\n\n"
            
            "• TROPHIES: UEFA Champions League (UCL), UEFA Europa League (UEL), UEFA Conference "
            "League (Conference/UECL), Intertoto, Title (Domestic League), Cup (Domestic Cup), "
            "UEFA Super Cup, Club World Cup, Cup Winners Cup, Copa Libertadores, "
            "Copa Sudamericana, Recopa, CONCACAF Champions Cup, CONCACAF Caribbean Cup, "
            "Central American Cup, Leagues Cup, CAF CL, CAF Confederation Cup, CAF Super Cup, "
            "AFC Champions League/Elite, ACL 2, ACGL/Challenge League, OFC Champions League."
        )

        text_box = tk.Text(
            self.root,
            width=60,
            height=15,
            wrap=tk.WORD,
            font=(self.font_family, 15),
            fg="white",
            bg="#1a1a1a",
            relief="flat",
            highlightthickness=0
        )
        text_box.insert(tk.END, how_to)
        text_box.config(state=tk.DISABLED)

        canvas.create_window(
            960, 500,
            window=text_box
        )

        # BACK BUTTON
        back_button = tk.Button(
            self.root,
            text="Back To Menu",
            width=22,
            font=(self.font_family, 15, "bold"),
            command=self.show_menu
        )
        self.add_sound_to_button(back_button)

        canvas.create_window(
            960, 900,
            window=back_button
        )

    # ---------------- SHOW CREDITS ----------------
    def show_credits(self):
        self.clear_screen()

        # BACKGROUND
        canvas = tk.Canvas(
            self.root,
            width=1920,
            height=1080,
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.spr_bck_2, anchor="nw")

        # TITLE
        canvas.create_text(
            960, 100,
            text="Credits",
            fill="white",
            font=(self.font_family, 36, "bold")
        )

        # TEXT
        how_to = (
            "DEVELOPMENT:\n"
            "• Created & Programmed by GABRIEL DUMITRAS\n"
            "• Built with Python | Libraries: Tkinter, Pygame\n"
            "• Environment: Visual Studio Code on Zorin OS 18\n\n"
            
            "VISUALS & AUDIO:\n"
            "• Sprites: Open-source assets sourced via Web\n"
            "• Sound Effects: Royalty-free assets sourced via Web\n\n"
            
            "MUSIC LICENSING:\n\n"
            
            "Main Menu:\n"
            "\"Champion\" by Alex-Productions (https://onsound.eu/)\n"
            "Promoted by Chosic (https://www.chosic.com/free-music/all/)\n"
            "Licensed under Creative Commons (CC BY 3.0)\n\n"
            
            "Level Soundtrack:\n"
            "\"Syndicate\" by Pufino\n"
            "Source: https://freetouse.com/music\n"
            "Vlog Music for Video (Free Download)\n\n"
            
            "THANK YOU FOR PLAYING!"
        )

        text_box = tk.Text(
            self.root,
            width=60,
            height=15,
            wrap=tk.WORD,
            font=(self.font_family, 15),
            fg="white",
            bg="#1a1a1a",
            relief="flat",
            highlightthickness=0
        )
        text_box.insert(tk.END, how_to)
        text_box.config(state=tk.DISABLED)

        canvas.create_window(
            960, 500,
            window=text_box
        )

        # BACK BUTTON
        back_button = tk.Button(
            self.root,
            text="Back To Menu",
            width=18,
            font=(self.font_family, 15, "bold"),
            command=self.show_menu
        )
        self.add_sound_to_button(back_button)

        canvas.create_window(
            960, 900,
            window=back_button
        )

    # ---------------- SELECT FILTER ----------------
    def select_filter(self):
        self.updating_filters = False
        self.clear_screen()

        # LOAD UNIQUE CONTINENTS & COUNTRIES
        continents = sorted({t["continent"] for t in self.game.teams})
        countries = sorted({t["country"] for t in self.game.teams})

        # BACKGROUND CANVAS
        canvas = tk.Canvas(
            self.root,
            width=1920,
            height=1080,
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.spr_bck_2, anchor="nw")

        # TITLE
        canvas.create_text(
            960, 100,
            text="Select Filters",
            fill="white",
            font=(self.font_family, 36, "bold")
        )

        # STORE VARIABLES
        self.selected_continents = []
        self.selected_countries = []
        
        self.continent_vars = {}
        self.country_vars = {}
        self.continent_checkboxes = {}
        self.country_checkboxes = {}

        # SCROLLABLE FRAME FOR CONTINENTS
        canvas.create_text(
            270, 300,
            text="Continents:",
            fill="white",
            font=(self.font_family, 20, "bold"),
            anchor="w"
        )
        
        continent_container = tk.Frame(self.root, bg="#1a1a1a")
        canvas.create_window(350, 600, window=continent_container, anchor="center", width=300, height=500)

        continent_canvas = tk.Canvas(continent_container, bg="#1a1a1a", highlightthickness=0)
        scrollbar_cont = tk.Scrollbar(continent_container, orient="vertical", command=continent_canvas.yview)
        scrollable_cont_frame = tk.Frame(continent_canvas, bg="#1a1a1a")
        
        def configure_scroll_region(event):
            continent_canvas.configure(scrollregion=continent_canvas.bbox("all"))
        
        scrollable_cont_frame.bind("<Configure>", configure_scroll_region)
        
        continent_canvas.create_window((0, 0), window=scrollable_cont_frame, anchor="nw")
        continent_canvas.configure(yscrollcommand=scrollbar_cont.set)
        
        continent_canvas.pack(side="left", fill="both", expand=True)
        scrollbar_cont.pack(side="right", fill="y")
        
        for i, continent in enumerate(continents):
            var = tk.BooleanVar(value=False)
            self.continent_vars[continent] = var
            
            cb = tk.Checkbutton(
                scrollable_cont_frame,
                text=continent,
                variable=var,
                font=(self.font_family, 15),
                fg="white",
                bg="#1a1a1a",
                selectcolor="#3a86ff",
                activebackground="#1a1a1a",
                activeforeground="white",
                borderwidth=0,
                highlightthickness=0,
                relief="flat"
            )
            cb.pack(anchor="w", padx=10, pady=3)
            self.continent_checkboxes[continent] = cb

        # SCROLLABLE FRAME FOR COUNTRIES
        canvas.create_text(
            1420, 300,
            text="Countries:",
            fill="white",
            font=(self.font_family, 20, "bold"),
            anchor="w"
        )
        
        country_container = tk.Frame(self.root, bg="#1a1a1a")
        canvas.create_window(1500, 600, window=country_container, anchor="center", width=300, height=500)
        
        country_canvas = tk.Canvas(country_container, bg="#1a1a1a", highlightthickness=0)
        scrollbar_country = tk.Scrollbar(country_container, orient="vertical", command=country_canvas.yview)
        scrollable_country_frame = tk.Frame(country_canvas, bg="#1a1a1a")
        
        def configure_country_scroll_region(event):
            country_canvas.configure(scrollregion=country_canvas.bbox("all"))
        
        scrollable_country_frame.bind("<Configure>", configure_country_scroll_region)
        
        country_canvas.create_window((0, 0), window=scrollable_country_frame, anchor="nw")
        country_canvas.configure(yscrollcommand=scrollbar_country.set)
        
        country_canvas.pack(side="left", fill="both", expand=True)
        scrollbar_country.pack(side="right", fill="y")
        
        for i, country in enumerate(countries):
            var = tk.BooleanVar(value=False)
            self.country_vars[country] = var
            
            cb = tk.Checkbutton(
                scrollable_country_frame,
                text=country,
                variable=var,
                font=(self.font_family, 15),
                fg="white",
                bg="#1a1a1a",
                selectcolor="#3a86ff",
                activebackground="#1a1a1a",
                activeforeground="white",
                borderwidth=0,
                highlightthickness=0,
                relief="flat"
            )
            cb.pack(anchor="w", padx=10, pady=3)
            self.country_checkboxes[country] = cb

        # MUTUAL EXCLUSION LOGIC
        def update_checkbox_states():
            if self.updating_filters:
                return

            self.updating_filters = True

            any_continent_selected = any(var.get() for var in self.continent_vars.values())
            any_country_selected = any(var.get() for var in self.country_vars.values())
            
            if any_continent_selected:
                for country, var in self.country_vars.items():
                    if var.get(): var.set(False)
                    self.country_checkboxes[country].config(state="disabled")
                for continent in continents:
                    self.continent_checkboxes[continent].config(state="normal")
            
            elif any_country_selected:
                for continent, var in self.continent_vars.items():
                    if var.get(): var.set(False)
                    self.continent_checkboxes[continent].config(state="disabled")
                for country in countries:
                    self.country_checkboxes[country].config(state="normal")
            
            else:
                for cb in self.continent_checkboxes.values(): cb.config(state="normal")
                for cb in self.country_checkboxes.values(): cb.config(state="normal")

            self.updating_filters = False
                
        def on_continent_change(continent):
            def callback(*args):
                update_checkbox_states()
            return callback
        
        def on_country_change(country):
            def callback(*args):
                update_checkbox_states()
            return callback
        
        for continent, var in self.continent_vars.items():
            var.trace_add("write", on_continent_change(continent))
        
        for country, var in self.country_vars.items():
            var.trace_add("write", on_country_change(country))

        # CLEAR ALL BUTTONS
        def clear_all_continents():
            self.updating_filters = True
            for var in self.continent_vars.values():
                var.set(False)
            self.updating_filters = False
            update_checkbox_states()
        
        def clear_all_countries():
            self.updating_filters = True
            for var in self.country_vars.values():
                var.set(False)
            self.updating_filters = False
            update_checkbox_states()
        
        clear_cont_button = tk.Button(
            self.root,
            text="Clear All Continents",
            width=22,
            font=(self.font_family, 15),
            command=clear_all_continents
        )
        self.add_sound_to_button(clear_cont_button)
        canvas.create_window(350, 900, window=clear_cont_button)
        
        clear_country_button = tk.Button(
            self.root,
            text="Clear All Countries",
            width=22,
            font=(self.font_family, 15),
            command=clear_all_countries
        )
        self.add_sound_to_button(clear_country_button)
        canvas.create_window(1500, 900, window=clear_country_button)

        # SAVE BUTTON
        save_button = tk.Button(
            self.root,
            text="Save & Close",
            width=22,
            font=(self.font_family, 15, "bold"),
            command=self.save_filters_and_close
        )
        self.add_sound_to_button(save_button)

        canvas.create_window(
            960, 900,
            window=save_button
        )

        self.setup_scroll_context(continent_container, continent_canvas)
        self.setup_scroll_context(country_container, country_canvas)

    # ---------------- SETUP SCROLL CONTEXT ---------------
    def setup_scroll_context(self, container, canvas):
            def _on_mousewheel(event):
                # Windows/macOS
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def _on_linux_scroll_up(event):
                canvas.yview_scroll(-1, "units")

            def _on_linux_scroll_down(event):
                canvas.yview_scroll(1, "units")

            def attach_scroll(event):
                self.root.bind_all("<MouseWheel>", _on_mousewheel)
                self.root.bind_all("<Button-4>", _on_linux_scroll_up)
                self.root.bind_all("<Button-5>", _on_linux_scroll_down)

            def detach_scroll(event):
                self.root.unbind_all("<MouseWheel>")
                self.root.unbind_all("<Button-4>")
                self.root.unbind_all("<Button-5>")

            container.bind("<Enter>", attach_scroll)
            container.bind("<Leave>", detach_scroll)

    # ---------------- SAVE FILTERS AND CLOSE ---------------
    def save_filters_and_close(self):
        try:
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
        except:
            pass
        
        self.selected_continents = [
            continent for continent, var in self.continent_vars.items() 
            if var.get()
        ]
        
        self.selected_countries = [
            country for country, var in self.country_vars.items() 
            if var.get()
        ]
        
        self.show_menu()

    # ---------------- PICK RANDOM TEAM ---------------
    def pick_random_team(self):
        valid_teams = []

        for t in self.game.teams:
            if self.selected_continents:
                if t["continent"] not in self.selected_continents:
                    continue
            
            if self.selected_countries:
                if t["country"] not in self.selected_countries:
                    continue

            valid_teams.append(t)

        if not valid_teams:
            return None

        return random.choice(valid_teams)

    # ---------------- START GAME ----------------
    def start_game(self):
        sp = SoundPlayer()
        sp.stop_music()
        sp.play_level_music()

        selected_difficulty = self.difficulty.get()

        # PICK TEAM
        team = self.pick_random_team()
        self.game.correct_team = team
        if team is None:
            return

        # CREATE GAME WITH TEAM
        self.game = Game(team)
        self.time_left = self.difficulty_times[selected_difficulty]
        self.clear_screen()
        self.build_game_ui()
        self.timer_running = True
        self.update_timer()

    # ---------------- BUILD GAME UI ----------------
    def build_game_ui(self):
        # BACKGROUND
        self.game_canvas = tk.Canvas(self.root, width=1920, height=1080, highlightthickness=0)
        self.game_canvas.pack(fill="both", expand=True)
        self.game_canvas.create_image(0, 0, image=self.spr_bck_level, anchor="nw")

        # CLOCK
        self.game_canvas.create_image(1120, 80, image=self.spr_clock, anchor="e")

        # ROBOT
        self.game_canvas.create_image(1600, 600, image=self.spr_robot, anchor="center")

        # ROBOT SPEECH
        self.robot_speech = self.game_canvas.create_text(
            1535, 435,
            text="Ask me...",
            fill="black",
            font=(self.font_family, 20),
            width=180,
            justify="center"
        )

        # TIMER
        self.timer_label = self.game_canvas.create_text(
            1000, 90,
            text=self.format_time(self.time_left),
            fill="red",
            font=(self.font_family, 25),
            anchor="center"
        )

        self.game_canvas.tag_raise(self.timer_label)

        # QUESTION ENTRY
        entry_x, entry_y = 400, 285
        self.game_canvas.create_image(
            entry_x, entry_y,
            image=self.spr_entry,
            anchor="center"
        )

        self.entry = tk.Entry(
            self.root,
            width=45,
            font=(self.font_family, 15),
            bg="white",
            fg="black",
            highlightthickness=0,
            bd=0,
            relief="flat"
        )
        self.entry.bind("<Return>", self.ask_question)
        self.game_canvas.create_window(entry_x, entry_y, window=self.entry)
        self.entry.focus_set()

        # GET TEAMS' NAMES FOR SUGGESTIONS
        all_names = []
        for t in self.game.teams:
            all_names.append(t["full_name"])
        self.suggestion_list = sorted(list(set(all_names)))
        self.in_suggestion_nav = False

        # GUESS ENTRY + BUTTON
        guess_x, guess_y = 1100, 285
        self.game_canvas.create_image(
            guess_x, guess_y,
            image=self.spr_entry,
            anchor="center"
        )
        
        guess_container = tk.Frame(self.root)
        
        self.guess_entry = tk.Entry(
            guess_container,
            width=45,
            font=(self.font_family, 15),
            bg="white",
            fg="grey",
            highlightthickness=0,
            bd=0,
            relief="flat"
        )
        self.guess_entry.insert(0, "Final answer here (press RIGHT ARROW) ...")
        
        def clear_placeholder(event):
            if self.guess_entry.get() == "Final answer here (press RIGHT ARROW) ...":
                self.guess_entry.delete(0, tk.END)
                self.guess_entry.config(fg="black")
        
        def restore_placeholder(event):
            if not self.guess_entry.get():
                self.guess_entry.insert(0, "Final answer here (press RIGHT ARROW) ...")
                self.guess_entry.config(fg="grey")
        
        self.guess_entry.bind("<FocusIn>", clear_placeholder)
        self.guess_entry.bind("<FocusOut>", restore_placeholder)
        self.guess_entry.bind("<Return>", self.on_entry_return)
        self.guess_entry.bind("<KeyRelease>", self.update_suggestions)
        self.guess_entry.pack(side=tk.LEFT, padx=0)
        
        # ---------------- PRESS DOWN WHEN ON ENTRY ----------------
        def on_entry_down(event):
            if self.suggestions_frame.winfo_ismapped():
                self.suggestion_listbox.focus_set()
                self.suggestion_listbox.selection_clear(0, tk.END)
                self.suggestion_listbox.selection_set(0)
                return "break"
        
        self.guess_entry.bind("<Up>", lambda e: "break")
        self.guess_entry.bind("<Down>", on_entry_down)
        self.guess_entry.pack(side=tk.LEFT, padx=0)
        
        self.game_canvas.create_window(guess_x, guess_y, window=guess_container)

        # AUTOCOMPLETE SETUP
        self.suggestions_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.suggestions_frame.place(x=805, y=335)

        self.suggestion_listbox = tk.Listbox(
            self.suggestions_frame,
            width=59,
            height=25,
            bg="#1a1a1a",
            fg="white",
            selectbackground="#3a86ff",
            selectforeground="white",
            font=("Minecraft", 12),
            activestyle="none",
            highlightthickness=0
        )
        self.suggestion_listbox.pack()

        self.suggestions_frame.place_forget()
        
        def on_listbox_up(event):
            sel = self.suggestion_listbox.curselection()
            if not sel or sel[0] == 0:
                return "break"
            idx = sel[0]
            self.suggestion_listbox.selection_clear(0, tk.END)
            self.suggestion_listbox.selection_set(idx - 1)
            return "break"
        
        def on_listbox_down(event):
            sel = self.suggestion_listbox.curselection()
            size = self.suggestion_listbox.size()
            if not sel or sel[0] >= size - 1:
                return "break"
            idx = sel[0]
            self.suggestion_listbox.selection_clear(0, tk.END)
            self.suggestion_listbox.selection_set(idx + 1)
            return "break"
        
        self.suggestion_listbox.bind("<Up>", on_listbox_up)
        self.suggestion_listbox.bind("<Down>", on_listbox_down)
        self.suggestion_listbox.bind("<ButtonRelease-1>", self.accept_selection)
        self.suggestion_listbox.bind("<Return>", lambda e: (self.accept_selection(), "break"))
        
        def close_suggestions(event):
            self.suggestion_frame.place_forget()
            self.in_suggestion_nav = False
            self.guess_entry.focus_set()
            return "break"
        
        self.suggestion_listbox.bind("<Escape>", close_suggestions)
        
        # GUESS BUTTON
        button_x, button_y = 400, 920
        
        self.guess_button = tk.Button(
            self.root,
            text="Final Answer",
            command=self.make_guess,
            bg=self.highlight_color,
            fg="white",
            font=(self.font_family, 18),
            padx=20,
            pady=8
        )
        self.add_sound_to_button(self.guess_button)
        
        self.game_canvas.create_window(button_x, button_y, window=self.guess_button)

        # CHAT HISTORY
        chat_x, chat_y = 400, 610
        
        self.game_canvas.create_image(
            chat_x, chat_y,
            image=self.spr_history_bubble,
            anchor="center"
        )
        
        self.response_box = tk.Text(
            self.root,
            height=10,
            width=45,
            bg="white",
            fg="black",
            font=(self.font_family, 10),
            relief="flat",
            highlightthickness=0,
            wrap=tk.WORD
        )
        self.response_box.config(state=tk.DISABLED)

        # TAGS
        self.response_box.tag_config("yes", foreground="green", font=(self.font_family, 18, "bold"))
        self.response_box.tag_config("no", foreground="red", font=(self.font_family, 18, "bold"))
        self.response_box.tag_config("neutral", foreground="blue", font=(self.font_family, 18))
        self.response_box.tag_config("normal", foreground="black", font=(self.font_family, 18))

        self.game_canvas.create_window(chat_x, chat_y, window=self.response_box)

        # GLOBAL ARROW BIND
        self.root.bind_all("<Right>", self.switch_to_guess) 
        self.root.bind_all("<Left>", self.switch_to_entry)

    # ---------------- SWITCH TO GUESS TEXTBOX ----------------
    def switch_to_guess(self, event=None):
        self.guess_entry.focus_set()
        if self.guess_entry.get() == "Final answer here (press RIGHT ARROW) ...":
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.config(fg="black")
        return "break"

    # ---------------- SWITCH TO QUESTION TEXTBOX ----------------
    def switch_to_entry(self, event=None):
        self.entry.focus_set()
        self.entry.delete(0, tk.END)
        return "break"

    # ---------------- PRESS ENTER ----------------
    def on_entry_return(self, event):
        # SELECT SUGGESTION
        if self.suggestions_frame.winfo_ismapped():
            try:
                sel = self.suggestion_listbox.curselection()
                if not sel:
                    self.suggestion_listbox.selection_set(0)
                self.accept_selection()
                self.suggestions_frame.place_forget()
                return "break"
            except:
                pass
            
        # ELSE, MAKE GUESS
        self.make_guess()
        return "break"

    # ---------------- UPDATE SUGGESTION ----------------
    def update_suggestions(self, event=None):
        text = self.guess_entry.get().strip().lower()

        if any(text == t["full_name"].lower() for t in self.game.teams):
            self.suggestions_frame.place_forget()
            return

        if not text:
            self.suggestions_frame.place_forget()
            return

        matches = [
            t["full_name"]
            for t in self.game.teams
            if text in t["full_name"].lower()
        ]

        if not matches:
            self.suggestions_frame.place_forget()
            return

        self.suggestion_listbox.delete(0, tk.END)
        for m in matches:
            self.suggestion_listbox.insert(tk.END, m)

        self.suggestions_frame.place(x=805, y=335)

    # ---------------- ON SUGGESTION SELECT ----------------
    def on_suggestion_select(self, event=None):
        if self.in_suggestion_nav:
            return
        pass

    # ---------------- ACCEPT SUGGESTION ----------------
    def accept_selection(self, event=None):
        try:
            index = self.suggestion_listbox.curselection()[0]
            value = self.suggestion_listbox.get(index)
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.insert(0, value.strip())
        except:
            return
        
        self.suggestions_frame.place_forget()
        self.guess_entry.focus()
    
    # ---------------- FORMAT TIME AS MM:SS ----------------
    def format_time(self, seconds):
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02d}:{remaining_seconds:02d}"

    # ---------------- MAKE GUESS ----------------
    def make_guess(self, event=None):
        guess = self.guess_entry.get().strip()

        if guess != "Final answer here (press RIGHT ARROW) ...":
            correct = self.game.check_guess(guess)
            self.show_result(correct)
        else:
            self.guess_entry.focus_set()

    # ---------------- ASK QUESTION ----------------
    def ask_question(self, event=None):
        question = self.entry.get().strip()
        if question:
            answer, tag = self.game.answer_question(question)
            self.entry.delete(0, tk.END)
            self.append_response(question, answer, tag)
            self.game_canvas.itemconfig(self.robot_speech, text=answer)

    # ---------------- APPEND RESPONSE ----------------
    def append_response(self, question, answer, tag):
        self.response_box.config(state=tk.NORMAL)
        self.response_box.insert(tk.END, f"> {question}\n", "normal")
        if answer == "???":
            self.response_box.insert(tk.END, f"{answer}\n", "neutral")
        else:
            self.response_box.insert(tk.END, f"{answer}\n", tag)
        self.response_box.config(state=tk.DISABLED)
        self.response_box.see(tk.END) 

    # ---------------- SHOW RESULT ----------------
    def show_result(self, correct):
        sp = SoundPlayer()
        sp.stop_music()

        self.timer_running = False
        self.clear_screen()
        
        canvas = tk.Canvas(self.root, width=1920, height=1080, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        canvas.create_image(0, 0, image=self.spr_bck_result, anchor="nw")
        
        overlay = canvas.create_rectangle(0, 0, 1920, 1080, 
                                        fill="black", stipple="gray50", width=0)
        canvas.itemconfig(overlay, state=tk.HIDDEN)
        
        team = self.game.correct_team
        colors = team.get("kit_colors", ["#333333", "white"])
        
        accent_color = colors[1] if len(colors) > 1 else "white"
        text_color = "white" 

        result_card = tk.Frame(
            canvas,
            bg="#1c1a1a",
            highlightbackground=accent_color,
            highlightthickness=5
        )

        canvas.create_window(960, 540, window=result_card, width=800, height=600, anchor="center")

        content = tk.Frame(result_card, bg="#1c1a1a", padx=40, pady=40)
        content.pack(fill="both", expand=True)

        if correct:
            self.sound.play("victory")
            result_text = "CORRECT!"
            status_color = "green"
        else:
            self.sound.play("defeat")
            result_text = "WRONG GUESS!"
            status_color = "red"

        tk.Label(
            content,
            text=result_text,
            font=(self.font_family, 35, "bold"),
            fg=status_color,
            bg="#1c1a1a"
        ).pack(pady=10)

        tk.Label(
            content,
            text=f"The team was: {team['full_name']}",
            font=(self.font_family, 25, "italic"),
            fg=text_color,
            bg="#1c1a1a"
        ).pack(pady=5)

        kit_frame = tk.Frame(content, bg="#1c1a1a")
        kit_frame.pack(pady=10)
        
        for c in colors:
            safe_color = get_color(c)
            tk.Frame(kit_frame, width=50, height=50, bg=safe_color, 
                    highlightbackground=text_color, highlightthickness=1
            ).pack(side="left", padx=2)

        tk.Button(
            content, 
            text="Back to Menu", 
            command=self.show_menu,
            font=(self.font_family, 15),
            bg="white",
            fg="black",
            activebackground="#d9d9d9",
            relief="flat",
            padx=20
        ).pack(side=tk.BOTTOM, pady=20)

    # ---------------- UPDATE TIMER ----------------
    def update_timer(self):
        if not self.timer_running:
            return

        if hasattr(self, 'game') and self.time_left > 0:
            self.time_left -= 1
            self.game_canvas.itemconfig(
                self.timer_label,
                text=self.format_time(self.time_left)
            )
            self.root.after(1000, self.update_timer)
        elif hasattr(self, 'time_left') and self.time_left <= 0:
            self.timer_running = False
            self.show_result(correct=False)

    # ---------------- ADD SOUND TO BUTTON ----------------
    def add_sound_to_button(self, button):
        button.bind("<Button-1>", lambda e: self.sound.play("click"))
        button.bind("<Enter>", lambda e: self.sound.play("hover"))
