# ==========================================================================
# options.rpy  —  Konfigurasi dasar & pengaturan build
# Game: Kelas 666
# ==========================================================================

define config.name = _("Kelas 666")

define gui.show_name = True

define config.version = "0.1.0"

define gui.about = _p("""
Visual novel interogasi/misteri.
Prototipe Minggu 1 — Lead Programmer: Zacky.
""")

# Nama dasar berkas yang dihasilkan saat build distribusi.
define build.name = "Kelas666"

# --- Suara -----------------------------------------------------------------
define config.has_sound = True
define config.has_music = True
define config.has_voice = False

# Musik di main menu (diaktifkan Minggu 3 setelah aset diimpor).
# define config.main_menu_music = "audio/bgm_interrogation.mp3"

# --- Transisi default ------------------------------------------------------
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

# --- Window -----------------------------------------------------------------
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

# --- Save directory ---------------------------------------------------------
define config.save_directory = "Kelas666-1727"


# ==========================================================================
# Pengaturan Build Distribusi  (.app / .dmg / .exe di Minggu 4)
# ==========================================================================
init python:

    # Klasifikasi berkas dokumentasi agar tidak ikut ke dalam arsip game.
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)

    # Dokumentasi: dimasukkan ke arsip tapi tidak ke dalam game.
    build.documentation("*.html")
    build.documentation("*.txt")
