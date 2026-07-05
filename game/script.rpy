# ==========================================================================
# Game: Kelas 666
# script.rpy  —  VERSI ADAPTASI (naskah Andy + improvisasi integrasi)
# Lead Programmer: Zacky
#
# Basis alur & sistem variabel: Progres_Minggu_2/Naskah.md (Andy).
# Adaptasi casting agar semua aset terpakai & masuk akal:
#   - MC          : sprite murid (main_char/MC_normal). Muncul di PROLOG
#                   (menyusup + konfrontasi) & di-reveal lagi di True Ending.
#                   Saat sidang/interogasi tetap POV first-person (tanpa sprite).
#   - Mahasiswa B : KORBAN = sprite 'Siswa Curi Jawaban' (anak_nakal). Bandar
#                   contekan yang memeras MC; muncul di prolog lalu jadi mayat.
#   - Saksi Mata  : sprite saksi_mata/* (5 ekspresi). Dibingkai sebagai PETUGAS
#                   KEBERSIHAN MALAM kampus yang diam-diam mengincar kunci jawaban.
#   - Detektif, Pengacara: sesuai desain.
#
# Sistem variabel (Andy):
#   poin_curiga = 0          -> naik bila bantahan tidak logis
#   pengacara_percaya = 2    -> ANGKA; naik/turun per pilihan; Babak 3 auto -2
#   saksi_hancur = False     -> True bila Saksi berhasil dibongkar (Babak 2 pil. B)
#
# Aset audio Deva (Cue_Audio_Sheet) sudah terpasang penuh.
# CATATAN Ren'Py: literal "[" di teks HARUS ditulis "[[" (sintaks variabel).
# ==========================================================================


# ==========================================================================
# 0. CHANNEL AUDIO TAMBAHAN (ambience loop terpisah dari SFX one-shot)
# ==========================================================================
init python:
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)


# ==========================================================================
# 1. KARAKTER
# ==========================================================================
define det  = Character("Detektif", color="#e06666", who_outlines=[(3, "#3a0d0d", 0, 0)])
define law  = Character("Pengacara", color="#6fa8dc", who_outlines=[(3, "#0d2033", 0, 0)])
define wit  = Character("Saksi", color="#d9c15a", who_outlines=[(3, "#33290d", 0, 0)])
define vic  = Character("Mahasiswa B", color="#c98f8f", who_outlines=[(3, "#331616", 0, 0)])  # korban (prolog)
define hak  = Character("Hakim", color="#c9a86a", who_outlines=[(3, "#332810", 0, 0)])         # V.O. — tanpa sprite
define mc   = Character("Aku", color="#e8e8e8", who_outlines=[(3, "#222222", 0, 0)])           # MC bicara langsung
define mcb  = Character("Aku", color="#b9b9d6", what_italic=True, who_suffix=" (batin)")       # MC batin
define narr = Character(None, what_italic=True)                                                # narasi / SFX cue


# ==========================================================================
# 2. DEFINISI GAMBAR (background + sprite)
# ==========================================================================
# --- Background (native 2752x1536 -> zoom 0.703 = 1935x1080, pas layar) ---
image bg redup   = Transform("images/background/bg_kelas666_redup.png", zoom=0.703)
image bg terang  = Transform("images/background/bg_kelas666_terang.png", zoom=0.703)
image trauma     = Transform("images/background/bg_kelas666_siluet_hitam.png", zoom=0.703)

# --- Detektif ---
image detektif normal     = "images/detektif/detektif_normal.png"
image detektif intimidasi = "images/detektif/detektif_intimidasi.png"
image detektif tegang     = "images/detektif/detektif_tegang.png"
image detektif terkejut   = "images/detektif/detektif_terkejut.png"
image detektif terdiam    = "images/detektif/detektif_terdiam.png"

# --- Pengacara ---
image pengacara pd     = "images/pengacara/pengacara_pd.png"
image pengacara ragu   = "images/pengacara/pengacara_ragu.png"
image pengacara marah  = "images/pengacara/pengacara_marah.png"
image pengacara curiga = "images/pengacara/pengacara_curiga.png"
image pengacara lega   = "images/pengacara/pengacara_lega.png"
image pengacara diam   = "images/pengacara/pengacara_diam.png"
image pengacara dingin = "images/pengacara/pengacara_dingin.png"

# --- Saksi Mata = petugas kebersihan malam (5 ekspresi) ---
image saksi normal   = "images/saksi_mata/saksi_mata_normal.png"
image saksi arogan   = "images/saksi_mata/saksi_arogan.png"
image saksi gugup    = "images/saksi_mata/saksi_gugup.png"
image saksi panik    = "images/saksi_mata/saksi_panik.png"
image saksi menangis = "images/saksi_mata/saksi_menangis.png"

# --- MC (prolog + reveal True Ending) & Korban/Mahasiswa B (prolog) ---
image mc normal = "images/main_char/MC_normal.png"
image korban    = "images/anak_nakal/Karakter_Siswa_Curi_Jawaban.png"


# ==========================================================================
# 3. TRANSFORM ANIMASI & POSISI (bust / setengah badan)
#    Pemakaian: show X at [mirror,] pos_<slot>, <anim>
#    - mirror   : flip horizontal (dipakai bila sprite perlu menghadap ke tengah)
#    - pos_*    : crop kepala-dada + posisi + animasi masuk (geser/naik)
#    - anim     : breathing / tremble / tremble_distress
# ==========================================================================
transform mirror:
    xzoom -1.0

# --- Idle breathing (loop halus) ------------------------------------------
transform breathing:
    subpixel True
    block:
        ease 2.4 yoffset -8
        ease 2.4 yoffset 0
        repeat

# --- Gemetar halus (gugup) -------------------------------------------------
transform tremble:
    subpixel True
    block:
        ease 0.045 xoffset 6
        ease 0.045 xoffset -6
        repeat

# --- Gemetar + warna wajah memudar (panik / menangis) ----------------------
transform tremble_distress:
    subpixel True
    matrixcolor SaturationMatrix(0.5) * BrightnessMatrix(-0.05)
    block:
        ease 0.04 xoffset 8
        ease 0.04 xoffset -8
        repeat

# --- Slot KIRI (bust) — masuk geser dari kiri ------------------------------
transform pos_left:
    subpixel True
    crop (0, 0, 1024, 980)
    zoom 0.82 xanchor 0.5 yanchor 0.0 xpos 0.22 ypos 0.05
    on show:
        alpha 0.0 xoffset -300
        easein 0.45 alpha 1.0 xoffset 0
    on replace:
        alpha 1.0 xoffset 0
    on hide:
        easeout 0.4 alpha 0.0 xoffset -260

# --- Slot KANAN (bust) — masuk geser dari kanan ----------------------------
transform pos_right:
    subpixel True
    crop (0, 0, 1024, 980)
    zoom 0.82 xanchor 0.5 yanchor 0.0 xpos 0.78 ypos 0.05
    on show:
        alpha 0.0 xoffset 300
        easein 0.45 alpha 1.0 xoffset 0
    on replace:
        alpha 1.0 xoffset 0
    on hide:
        easeout 0.4 alpha 0.0 xoffset 260

# --- Slot TENGAH (bust) — masuk naik dari bawah ----------------------------
transform pos_center:
    subpixel True
    crop (0, 0, 1024, 980)
    zoom 0.86 xanchor 0.5 yanchor 0.0 xpos 0.5 ypos 0.04
    on show:
        alpha 0.0 yoffset 60
        easein 0.45 alpha 1.0 yoffset 0
    on replace:
        alpha 1.0 yoffset 0
    on hide:
        easeout 0.4 alpha 0.0 yoffset 45

# --- Transisi khusus efek ---------------------------------------------------
define flash_red = Fade(0.06, 0.0, 0.5, color="#5a0000")
define slam      = Fade(0.02, 0.0, 0.25, color="#000000")


# ==========================================================================
# 4. VARIABEL SISTEM (penentu 3 ending) — sesuai Naskah.md Andy
# ==========================================================================
default poin_curiga = 0            # naik bila bantahan MC tidak logis
default pengacara_percaya = 2      # ANGKA (bukan boolean). Awal = 2
default saksi_hancur = False       # True setelah Babak 2 pilihan B

define CURIGA_THRESHOLD = 3


# ==========================================================================
# 5. PROLOG — MALAM ITU  (Kelas 666, jam 2 pagi)  [MC tampil]
# ==========================================================================
label start:

    scene black
    with Pause(0.3)

    play music "audio/bgm/bgm_prolog_malam.mp3" fadein 2.0 volume 0.8
    play ambient "audio/sfx/sfx_jam_dinding.mp3" fadein 1.0 volume 0.55
    narr "Kelas 666. Jam dua pagi. Gelap dan sunyi. Hanya detak jam dinding yang mengisi lorong sekolah yang kosong."
    mcb "Aku tahu ini salah. Tapi kalau soal ujian besok bocor sekarang, semua kerja kerasku selama ini tidak akan berarti apa-apa."

    play sound "audio/sfx/sfx_langkah_pelan.mp3"
    scene bg redup with Dissolve(0.8)
    show mc normal at mirror, pos_left, breathing
    with Dissolve(0.5)
    mcb "Aku menyelinap lewat jendela yang lupa dikunci. Brankas soal ada di depan mata."

    play sound "audio/sfx/sfx_brankas_decit.mp3"
    mcb "...Brankasnya sudah terbuka? Siapa yang ke sini sebelum aku?"

    play sound "audio/sfx/sfx_heartbeat.mp3"
    show korban at pos_right, breathing
    with Dissolve(0.5)
    vic "Wah, wah. Si anak teladan malah nekat juga malam ini."
    mcb "Dia. Bandar kunci jawaban yang selama ini memerasku dengan rekaman itu."
    vic "Tenang. Selama kamu terus bayar, rahasiamu aman. Tapi kalau berani macam-macam..."

    show korban at pos_right, tremble
    vic "Aku bisa hancurkan masa depanmu malam ini juga."
    menu:
        "Dia mencengkeram kerahmu. Apa yang kau lakukan?"

        "Mendorongnya menjauh sekuat tenaga.":
            mc "Lepaskan aku!"
        "Berusaha merebut rekaman di tangannya.":
            mc "Berikan itu padaku!"

    # Pergumulan tidak diperlihatkan penuh — layar menggelap
    stop ambient fadeout 1.0
    play sound "audio/sfx/sfx_dorongan_benturan.mp3"
    scene black with slam
    with vpunch
    narr "Suara dorongan. Sebuah benda jatuh menghantam sudut meja. Langkah kaki panik."
    mcb "Aku tidak ingat persis apa yang terjadi setelah itu. Yang aku ingat cuma suara benturan keras, lalu semuanya diam."

    play sound "audio/sfx/sfx_sirene_polisi.mp3"
    narr "Dari kejauhan, sirene polisi. Semakin lama semakin dekat."
    mcb "Tanganku gemetar. Ada sesuatu yang basah di ujung kemejaku. Aku tidak sempat berpikir sebelum lampu senter menyorot wajahku."

    stop music fadeout 1.5

    call babak_1
    call babak_2
    call babak_3

    return


# ==========================================================================
# BABAK 1 — TEKANAN  (mengumpulkan poin_curiga & pengacara_percaya)
# ==========================================================================
label babak_1:

    # SFX: Gebrakan meja — layar bergetar
    play sound "audio/sfx/sfx_desk_slam.mp3"
    scene black with slam
    with vpunch
    play music "audio/bgm/bgm_interrogation.mp3" fadein 1.2 volume 0.85

    scene bg redup with Dissolve(0.6)
    show detektif intimidasi at mirror, pos_right, breathing
    with Dissolve(0.3)
    det "Kamu tertangkap basah di Kelas 666 bersama mayat dan brankas soal ujian yang terbuka. Jangan mengelak lagi."

    show pengacara pd at mirror, pos_left, breathing
    with Dissolve(0.4)
    law "Tenang, jangan jawab terburu-buru. Katakan yang sejujurnya — apa yang kamu lakukan di sana jam dua pagi?"

    mcb "Tanganku masih gemetar. Noda kemerahan di ujung kemejaku untungnya tidak terlihat dalam cahaya redup ini. Aku harus merangkai alasan yang masuk akal."

    menu:
        "Bagaimana kau menjawab?"

        "\"Saya hanya kebetulan lewat dan melihat pintu terbuka.\"":
            $ poin_curiga += 1
            show detektif intimidasi at mirror, pos_right, breathing
            mc "Saya... hanya kebetulan lewat. Pintunya terbuka, jadi saya masuk."
            det "Kebetulan? Jendela dibuka paksa dan brankas dibongkar. 'Kebetulan lewat' tidak menjelaskan itu."
            show pengacara ragu at mirror, pos_left, breathing
            law "(Alasan itu terlalu tipis...)"

        "\"Saya memang berniat mencuri soal ujian, tapi saya tidak membunuh siapa pun!\"":
            $ pengacara_percaya += 1
            mc "Saya jujur saja. Saya ke sana untuk mengambil soal ujian — itu salah, saya akui. Tapi saya tidak membunuh siapa pun."
            show detektif terdiam at mirror, pos_right, breathing
            det "...Setidaknya kau punya nyali untuk mengakui satu dosa."
            show pengacara pd at mirror, pos_left, breathing
            law "(Bagus. Kejujuran parsial membuatmu terlihat manusiawi, bukan monster.)"

        "\"Itu bukan urusan Anda! Saya minta pulang!\"":
            $ poin_curiga += 2
            $ pengacara_percaya -= 1
            play sound "audio/sfx/sfx_desk_slam.mp3"
            with hpunch
            mc "Itu bukan urusan Anda! Saya minta pulang sekarang juga!"
            show detektif intimidasi at mirror, pos_right, breathing
            det "Menuntut pulang? Orang tak berdosa tidak berteriak seperti hewan yang terpojok."
            show pengacara curiga at mirror, pos_left, breathing
            law "(Tenanglah... kau menggali kuburmu sendiri.)"

    show detektif normal at mirror, pos_right, breathing
    det "Kita simpan jawabanmu. Sebentar lagi kau akan bertemu seseorang yang katanya melihat semuanya."
    return


# ==========================================================================
# BABAK 2 — KONTRADIKSI  (menentukan saksi_hancur)
# ==========================================================================
label babak_2:

    show detektif normal at mirror, pos_right, breathing
    det "Ada petugas kebersihan malam yang sedang piket. Dia melihatmu dengan jelas — bersembunyi di balik meja saat kamu memukul korban."

    play sound "audio/sfx/sfx_langkah_pelan.mp3"
    show saksi arogan at pos_center, breathing
    with Dissolve(0.5)
    wit "I-iya... Saya lihat semuanya! Ruangannya memang gelap, tapi saya lihat dia memukul korban pakai kursi kayu!"

    mcb "Dia berbohong. Korban jatuh membentur ujung meja, bukan dipukul kursi. Tapi aku tidak boleh mengatakan itu."

    show pengacara curiga at mirror, pos_left, breathing
    law "Ada yang janggal dari kesaksian ini. Coba perhatikan lagi detailnya."

    # SFX: ketegangan batin MC menyusun bantahan
    play sound "audio/sfx/sfx_heartbeat.mp3"

    menu:
        "Serang kesaksian Saksi:"

        "\"Kursi kayu terlalu berat untuk saya angkat!\"":
            $ poin_curiga += 1
            mc "Kursi kayu itu berat! Mana mungkin saya mengangkatnya sendirian!"
            show saksi arogan at pos_center, breathing
            wit "Berat? Adrenalin bisa membuat orang mengangkat apa saja. Argumen lemah."
            show pengacara ragu at mirror, pos_left, breathing
            law "(Sayang sekali. Kau menyerang hal yang salah, dan justru terdengar defensif.)"
            show detektif intimidasi at mirror, pos_right, breathing
            det "Kesaksian tetap berdiri. Kau tak menggoyahkan apa pun."

        "\"Jika ruangan gelap total, bagaimana kamu bisa tahu pasti senjata yang digunakan?\"":
            $ poin_curiga -= 1
            $ pengacara_percaya += 1
            $ saksi_hancur = True
            mc "Tunggu. Kau bilang ruangannya {b}gelap total{/b}."
            mc "Lalu bagaimana kau bisa tahu {i}persis{/i} senjatanya kursi kayu? Bagaimana kau melihatnya sejelas itu dalam gelap gulita?"
            show saksi gugup at pos_center, tremble
            with hpunch
            wit "I-itu... s-saya... saya kan cuma..."
            show pengacara pd at mirror, pos_left, breathing
            law "Jawab pertanyaannya. Kalau ruangan gelap total, apa yang sebenarnya bisa kau lihat?"

            stop music fadeout 1.0
            show detektif terkejut at mirror, pos_right, breathing
            with hpunch
            det "...Ruangan gelap?"

            play music "audio/bgm/bgm_panic.mp3" fadein 0.8 volume 0.85
            show saksi panik at pos_center, tremble_distress
            play sound "audio/sfx/sfx_heartbeat.mp3"
            wit "Baik! BAIK! Saya mengaku!"
            show saksi menangis at pos_center, tremble_distress
            wit "Saya tidak melihat pembunuhannya! Saya datang ke sana {i}setelah{/i} kejadian — saya cuma mau menyalin kunci jawaban buat saya jual!"
            wit "Waktu saya masuk, mayatnya sudah tergeletak. Saya panik, takut dituduh, jadi saya karang cerita itu!"

            show pengacara lega at mirror, pos_left, breathing
            law "Kesaksian dibatalkan. Satu-satunya 'saksi mata' baru saja mengaku berbohong."
            mcb "Aku... aku menang? Ini sudah selesai?"

    hide saksi with Dissolve(0.5)
    return


# ==========================================================================
# BABAK 3 — BUKTI ABSOLUT & PENENTUAN NASIB
# ==========================================================================
label babak_3:

    show detektif tegang at mirror, pos_right, breathing
    with Dissolve(0.3)
    if saksi_hancur:
        det "Bagus. Saksi kita coret dari daftar pembunuh."
    else:
        det "Kesaksian tadi masih berdiri. Tapi itu bahkan bukan kartu terkuatku."

    # SFX: Detektif mengeluarkan barang bukti
    play sound "audio/sfx/sfx_paper_rustle.mp3"
    show detektif intimidasi at mirror, pos_right, breathing
    det "Kami menemukan ponsel korban dengan draf pesan ancaman yang ditujukan padamu."
    det "Dan yang paling fatal — ada serpihan kain kemejamu di bawah kuku korban."

    # Stinger dramatis + transisi tegang
    play sound "audio/sfx/sfx_dramatic_hit.mp3" volume 0.7
    play music "audio/bgm/bgm_panic.mp3" fadein 1.0 volume 0.85
    show pengacara marah at mirror, pos_left, breathing
    with vpunch
    law "Kamu..."
    law "Kamu... membohongiku?"

    # [Sistem] Otomatis di semua jalur: kepercayaan pengacara jatuh drastis
    $ pengacara_percaya -= 2

    mcb "Wajah pengacaraku berubah. Aku bisa melihat keraguan menjalar di matanya. Apapun yang aku katakan setelah ini harus cukup kuat untuk meyakinkannya kembali."

    # ---------------- KONDISI A : poin_curiga >= 3 ----------------
    if poin_curiga >= CURIGA_THRESHOLD:
        show detektif normal at mirror, pos_right, breathing
        det "Kamu sudah cukup membuktikan diri sendiri, hanya lewat caramu menjawab. Semua bukti ini tinggal formalitas."
        show pengacara diam at mirror, pos_left, breathing
        with Dissolve(0.4)
        narr "Pengacara menunduk, diam, tidak lagi membela."
        mcb "Aku kehabisan cara. Semua jalan sudah tertutup jauh sebelum bukti ini muncul."
        jump ending_bad

    # ---------------- KONDISI B : saksi_hancur ? ----------------
    if saksi_hancur:
        # ----- KONDISI C1 : pengacara_percaya >= 1 ? -----
        if pengacara_percaya >= 1:
            show pengacara curiga at mirror, pos_left, breathing
            law "Saksi itu sudah kehilangan kredibilitasnya di depan hakim. Tapi bukti ini terlalu kuat untuk kita abaikan."
            law "Ceritakan yang sebenarnya terjadi. Aku akan cari cara membelamu."
            menu:
                "Keputusan terakhirmu:"
                "\"Saksi itu yang masuk untuk mencuri kunci jawaban! Dia panik lalu mengarang cerita untuk menutupi jejaknya sendiri!\"":
                    jump ending_normal
                "\"Saya... tidak bermaksud membunuhnya. Kami bergumul, dia terjatuh membentur meja. Saya panik dan mencoba kabur.\"":
                    jump ending_true
        else:
            show pengacara dingin at mirror, pos_left, breathing
            law "Aku sudah tidak yakin dengan semua ucapanmu. Satu-satunya cara aku bisa membantu adalah kalau kamu menunjuk arah lain. Titik."
            menu:
                "Hanya ada satu jalan tersisa:"
                "\"Saksi itu yang sebenarnya masuk untuk mencuri kunci jawaban! Dia yang harus bertanggung jawab!\"":
                    jump ending_normal

    else:
        # ----- KONDISI C2 : pengacara_percaya >= 1 ? -----
        if pengacara_percaya >= 1:
            show pengacara curiga at mirror, pos_left, breathing
            law "Kesaksian itu masih berdiri kuat di mata hakim, kita tidak bisa menyerangnya lagi. Tapi aku masih percaya kamu bukan pembunuh berencana."
            law "Katakan yang sebenarnya. Akan aku bangun pembelaan dari situ."
            menu:
                "Hanya ada satu jalan tersisa:"
                "\"Saya... tidak bermaksud membunuhnya. Itu kecelakaan saat kami bergumul. Saya panik dan mencoba kabur.\"":
                    jump ending_true
        else:
            show pengacara dingin at mirror, pos_left, breathing
            law "Aku sudah tidak bisa berbuat apa-apa lagi. Kesaksian itu masih berlaku, dan kamu bahkan tidak jujur padaku sejak awal."
            narr "Pengacara menutup map di tangannya."
            mcb "Tidak ada jalan keluar lagi. Kebohonganku terlalu jauh mengakar untuk bisa dibongkar sekarang."
            jump ending_bad


# ==========================================================================
# ENDINGS  (SETTING: Ruang Sidang, beberapa minggu kemudian)
# Catatan produksi: Jaksa dihapus -> peran diambil Detektif. Hakim = V.O.
# ==========================================================================

label ending_bad:
    scene black with Dissolve(1.0)
    pause 0.4
    play music "audio/bgm/bgm_ruang_sidang.mp3" fadein 1.2 volume 0.8
    play ambient "audio/sfx/sfx_gumama_sidang.mp3" fadein 1.0 volume 0.45
    narr "Ruang Sidang. Beberapa minggu kemudian. Gumaman pengunjung memenuhi ruangan."

    scene bg redup with Dissolve(0.8)
    show detektif normal at mirror, pos_right, breathing       # Detektif merangkap penuntut
    with Dissolve(0.4)
    det "Yang Mulia, seluruh bukti sudah jelas menunjukkan niat dan tindakan terdakwa. Poin kecurigaan yang terus meningkat sejak awal penyelidikan membuktikan bahwa terdakwa tidak pernah berniat jujur sejak hari pertama."

    show pengacara diam at mirror, pos_left, breathing
    with Dissolve(0.4)
    narr "Pengacara menunduk, tidak mengangkat argumen apa pun."

    stop ambient fadeout 1.5
    hak "Berdasarkan seluruh bukti dan kesaksian yang telah dipaparkan, pengadilan memutuskan terdakwa bersalah atas pembunuhan berencana."

    play sound "audio/sfx/sfx_palu_tegas.mp3"
    with vpunch
    mcb "Aku menunggu rasa itu datang — penyesalan, atau ketakutan. Tapi yang datang justru kekosongan. Aku sudah kehilangan kesempatan membela diri jauh sebelum sidang ini dimulai."

    scene black with Dissolve(1.5)
    mcb "Pintu besi itu tertutup di belakangku. Dan untuk pertama kalinya, aku benar-benar sendirian dengan kebohongan yang aku buat sendiri."
    centered "{size=72}BAD ENDING{/size}\n\n{size=40}Penjara Maksimal{/size}"
    jump the_end


label ending_normal:
    scene black with Dissolve(1.0)
    pause 0.4
    play music "audio/bgm/bgm_ruang_sidang.mp3" fadein 1.2 volume 0.8
    play ambient "audio/sfx/sfx_gumama_sidang.mp3" fadein 1.0 volume 0.45
    narr "Ruang Sidang. Beberapa minggu kemudian."

    scene bg terang with Dissolve(0.8)
    show pengacara pd at mirror, pos_left, breathing
    with Dissolve(0.4)
    law "Yang Mulia, kesaksian yang tadinya dijadikan dasar tuduhan ternyata mengandung kontradiksi besar. Saksi sendiri telah mengakui berada di lokasi untuk tujuan yang berbeda dari yang ia sampaikan sebelumnya."

    play sound "audio/sfx/sfx_tangis_diseret.mp3"
    show saksi menangis at pos_center, tremble_distress
    with Dissolve(0.5)
    wit "Saya... saya cuma mau menyalin kunci jawaban juga! Saya nggak ada hubungannya sama kematian itu!"

    show detektif terkejut at mirror, pos_right, breathing
    with Dissolve(0.4)
    narr "Detektif terdiam, menatap berkas di tangannya."

    hide saksi with Dissolve(0.4)
    stop ambient fadeout 1.5
    hak "Mengingat kredibilitas kesaksian yang telah runtuh, dan tidak adanya bukti langsung yang mengaitkan terdakwa dengan tindak kekerasan, pengadilan memutuskan untuk membebaskan terdakwa dari seluruh tuduhan."

    scene black with Dissolve(1.2)
    mcb "Aku bebas. Tapi kebebasan ini terasa seperti utang yang belum aku bayar. Aku tahu persis apa yang sebenarnya terjadi malam itu — dan itu bukan Saksi."
    mcb "Mungkin suatu hari nanti, kebenaran ini akan mengejarku kembali. Tapi untuk sekarang, aku memilih berjalan terus."
    centered "{size=72}NORMAL ENDING{/size}\n\n{size=40}Kambing Hitam{/size}"
    jump the_end


label ending_true:
    scene black with Dissolve(1.0)
    pause 0.4
    play music "audio/bgm/bgm_ruang_sidang.mp3" fadein 1.2 volume 0.8
    play ambient "audio/sfx/sfx_gumama_sidang.mp3" fadein 1.0 volume 0.4
    narr "Ruang Sidang. Beberapa minggu kemudian."

    scene bg terang with Dissolve(0.8)
    show pengacara pd at mirror, pos_left, breathing
    with Dissolve(0.4)
    law "Yang Mulia, klien saya tidak pernah berniat mengakhiri nyawa siapa pun. Yang terjadi malam itu adalah kecelakaan dalam situasi penuh tekanan — bukan tindakan yang direncanakan."

    # Momen KUNCI: kamera lepas dari POV, wajah MC ditampilkan penuh
    show mc normal at pos_center, breathing
    with Dissolve(0.6)
    mc "Saya... saya panik. Saya cuma mau kabur waktu itu, bukan menyakiti siapa pun. Tapi saya terlalu takut mengatakan yang sebenarnya sejak awal."

    narr "Hakim menimbang lama, membolak-balik berkas."
    stop ambient fadeout 1.5
    hak "Pengadilan mempertimbangkan pengakuan jujur terdakwa serta tidak adanya unsur perencanaan dalam peristiwa ini."

    play sound "audio/sfx/sfx_palu_pelan.mp3"
    hak "Terdakwa dinyatakan bersalah atas kelalaian yang mengakibatkan kematian, dengan masa hukuman yang telah mempertimbangkan pengakuan dan kerja samanya selama persidangan."

    show pengacara lega at mirror, pos_left, breathing
    narr "Pengacara menepuk pundak MC."
    law "Ini bukan akhir yang sempurna. Tapi ini akhir yang jujur."

    scene black with Dissolve(1.2)
    mcb "Untuk pertama kalinya sejak malam itu, aku bisa bernapas lega. Bukan karena aku bebas — tapi karena aku akhirnya berhenti berbohong, bahkan pada diriku sendiri."
    centered "{size=72}TRUE ENDING{/size}\n\n{size=40}Manslaughter{/size}"
    jump the_end


label the_end:
    stop music fadeout 3.0
    stop ambient fadeout 2.0
    pause 1.0
    centered "{size=48}TAMAT{/size}\n\n{size=28}Kelas 666{/size}"
    return
