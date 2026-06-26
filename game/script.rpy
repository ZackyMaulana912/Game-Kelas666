# ==========================================================================
# Game: Kelas 666
# script.rpy  —  DUMMY SCRIPT (Minggu 1: Logic Prototyping / PoC)
# Lead Programmer: Zacky
#
# Tujuan file ini: membuktikan alur Babak 1 -> 2 -> 3 dan percabangan ke
# 3 ending berjalan tanpa error. Teks masih placeholder; naskah penuh
# dimasukkan di Minggu 2 (lihat Alur_Cerita.md & Progres_Minggu_1/Naskah.md).
# ==========================================================================

# --- Definisi Karakter ----------------------------------------------------
define det = Character("Detektif", color="#d65a5a")
define law = Character("Pengacara", color="#5a9bd6")
define wit = Character("Saksi", color="#c7a85a")
define mc  = Character("Aku", color="#cccccc")          # MC: first-person, tanpa sprite

# --- Variabel Sistem (penentu 3 ending) -----------------------------------
default poin_curiga = 0           # naik bila bantahan MC tidak logis
default pengacara_percaya = True  # False bila poin_curiga lewat ambang -> percepat Bad Ending
default saksi_hancur = False      # harus True setelah Babak 2 agar lanjut Babak 3
default mc_mengaku = False         # pilihan final Babak 3: mengaku atau bertahan

# Ambang batas kecurigaan yang memicu kegagalan
define CURIGA_THRESHOLD = 3


# ==========================================================================
# START
# ==========================================================================
label start:

    "== Kelas 666 — PROTOTIPE LOGIKA (Minggu 1) =="
    mc "(Placeholder) Aku terbangun di Kelas 666. Ada mayat dan brankas soal yang terbuka..."

    call babak_1
    call babak_2
    call babak_3

    return


# ==========================================================================
# BABAK 1 — Tekanan & Manipulasi  (mengumpulkan poin_curiga)
# ==========================================================================
label babak_1:

    scene black with fade
    # TODO Minggu 3: scene kelas_redup + play music bgm_interrogation + vpunch saat gebrak meja
    det "Placeholder Detektif: Kamu tertangkap basah. Jangan mengelak."
    law "Placeholder Pengacara: Tenang, jawab dengan jujur."

    menu:
        "Pilihan Dialog 1 (placeholder):"

        "[A] Mengelak halus — 'Saya cuma kebetulan lewat.'":
            $ poin_curiga += 1
            mc "Dummy A: aku berbohong soal kebetulan lewat."

        "[B] Jujur sebagian — 'Saya berniat mencuri soal, tapi tidak membunuh.'":
            $ poin_curiga += 0
            mc "Dummy B: aku mengaku niat mencuri."

        "[C] Membentak — 'Bukan urusan Anda! Saya minta pulang!'":
            $ poin_curiga += 2
            mc "Dummy C: aku membentak dan terlihat panik."

    # Pengacara berhenti percaya bila MC terlalu mencurigakan sejak awal
    if poin_curiga >= CURIGA_THRESHOLD:
        $ pengacara_percaya = False
        law "Placeholder Pengacara: ...(diam, mulai meragukanmu)."

    "[DEBUG] Akhir Babak 1 -> poin_curiga=[poin_curiga], pengacara_percaya=[pengacara_percaya]"
    return


# ==========================================================================
# BABAK 2 — Kontradiksi Saksi Mata  (menentukan saksi_hancur)
# ==========================================================================
label babak_2:

    wit "Placeholder Saksi: Aku lihat dia memukul korban pakai kursi kayu!"
    law "Placeholder Pengacara: Ada yang janggal. Serang celah logikanya."

    menu:
        "Pilihan Dialog 2 (placeholder):"

        "[A] 'Kursi kayu terlalu berat untuk saya angkat!'":
            $ poin_curiga += 1
            mc "Dummy A: argumen lemah, tidak mematahkan saksi."

        "[B] 'Kalau gelap total, bagaimana kamu tahu pasti senjatanya?'":
            $ saksi_hancur = True
            wit "Placeholder Saksi: ...(panik, menangis) Aku cuma mau curi soal!"

    "[DEBUG] Akhir Babak 2 -> saksi_hancur=[saksi_hancur], poin_curiga=[poin_curiga]"
    return


# ==========================================================================
# BABAK 3 — Jebakan Terakhir & Eksekusi Ending
# ==========================================================================
label babak_3:

    det "Placeholder Detektif: Kesaksian dibatalkan... tapi ada serpihan kemejamu di kuku korban."
    law "Placeholder Pengacara: Kamu... membohongiku?"

    menu:
        "Pilihan Dialog 3 — penentuan akhir (placeholder):"

        "[A] Bertahan dengan kebohongan — salahkan Saksi sepenuhnya.":
            $ mc_mengaku = False

        "[B] Mengaku — 'Korban memerasku. Itu tidak sengaja.'":
            $ mc_mengaku = True

    # --- Kalkulasi Ending (if / elif / else) ------------------------------
    if mc_mengaku:
        jump ending_true
    elif (poin_curiga >= CURIGA_THRESHOLD) or (not pengacara_percaya):
        jump ending_bad
    else:
        jump ending_normal


# ==========================================================================
# ENDINGS
# ==========================================================================
label ending_bad:
    scene black with fade
    "== BAD ENDING — Penjara Maksimal =="
    "Kebohonganmu runtuh total. Pengacara mundur. Kamu dihukum berat."
    "[DEBUG] poin_curiga=[poin_curiga] pengacara_percaya=[pengacara_percaya] saksi_hancur=[saksi_hancur]"
    return

label ending_normal:
    scene black with fade
    "== NORMAL ENDING — Kambing Hitam =="
    "Saksi dipenjara, tapi kamu tetap di-DO. Selamat, tapi rasa bersalah membayangimu."
    "[DEBUG] poin_curiga=[poin_curiga] pengacara_percaya=[pengacara_percaya] saksi_hancur=[saksi_hancur]"
    return

label ending_true:
    scene black with fade
    "== TRUE ENDING — Manslaughter =="
    "Kamu mengaku. Skandal pemerasan terbongkar. Hukumanmu lebih ringan."
    "[DEBUG] poin_curiga=[poin_curiga] pengacara_percaya=[pengacara_percaya] saksi_hancur=[saksi_hancur]"
    return
