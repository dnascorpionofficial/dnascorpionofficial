USER = "dnascorpionofficial"
NAME = "ScorpioN"
ACCENT = "#e63946"

# header (assets/header.svg)
TAGLINES = [ # cycle every 3s under the name
    "> bots & automation",
    "> Python | Shell | C | Rust",
    "> Android tools & SU modules",
    "> HTML | JAVASCRIPT | CSS",
    "> Beginner | Kotlin | Java",
]

# terminal card (assets/terminal.svg)
# cmd = "$ <text>" typed in white, out = grey output line, ok = green status line
TERMINAL_TITLE = f"scorpion@{USER}: ~"
TERMINAL = [
    ("cmd", "whoami"),
    ("out", "ScorpioN | bots, automation, Android"),
    ("cmd", "ls focus/"),
    ("out", "telegram-bots  android  kernelsu  scripts"),
    ("cmd", "cat work.txt"),
    ("out", "private + client work. quality > showcase"),
    ("cmd", "status"),
    ("ok", "\u25cf open for freelance work"),
]

# "What I build" cards (assets/build.svg)
BUILD_TITLE = "What I build"
BUILD = [ # (icon, title, line 1, line 2)
    ("bot", "Telegram bots", "Auto-posting, commands, AI features,", "admin panels and databases"),
    ("phone", "Android tools", "Apps, keyboards, KernelSU modules", "and WebUIs"),
    ("gear", "Scripts & automation", "Python, shell, C and Rust tooling", "built to run on their own"),
]

# skills (assets/skills.svg)
SKILLS_TITLE = "Languages & skill level"
SKILLS_NOTE = "Currently leveling up: C and Rust"
LEVELS = { # name: (ring fill 0-1, colour, legend x)
    "Pro": (1.00, ACCENT, 150),
    "Intermediate": (0.66, "#f4a261", 250),
    "Beginner": (0.33, "#58a6ff", 410),
}
SKILLS = [ # (badge, name, level) - 3 per row
    ("Py", "Python", "Pro"),
    ("Sh", "Shell / Bash", "Pro"),
    ("JS", "JavaScript", "Pro"),
    ("</>", "HTML", "Pro"),
    ("CSS", "CSS", "Pro"),
    ("C", "C", "Intermediate"),
    ("Rs", "Rust", "Intermediate"),
    ("Kt", "Kotlin", "Beginner"),
    ("Jv", "Java", "Beginner"),
]

# small pieces
SNAKE_TITLE = "Contribution graph" # snake.yml (Platane/snk)
CONTACT_TITLE = "Contact"

# private-work note (assets/private.svg), shown under the contribution graph
PRIVATE_TITLE = "Why no public repos?"
PRIVATE_LINES = [ # keep each line under ~40 characters
    "I do paid client work, so almost every",
    "project I build is kept private.",
    "Graph above / scroll down - contribution count.",
]
TELEGRAM_TEXT = "Ping Me in groups only"
