# ==========================================================================
# Game: Kelas 666
# script.rpy  —  VERSI ADAPTASI (naskah Andy + improvisasi integrasi)
# Lead Programmer: Zacky
#
# Basis alur & sistem variabel: Progres_Minggu_2/Naskah.md (Andy).
# Casting adaptasi (semua aset terpakai):
#   MC (Jokiwi) = main_char/MC_normal  (tampil di PROLOG & reveal True Ending)
#   Rendra      = anak_nakal/...       (KORBAN: bandar contekan yang memeras Jokiwi)
#   Saksi Mata  = saksi_mata/* (5 eksp) (petugas kebersihan malam pengincar kunci jawaban)
#   Detektif, Pengacara                (sesuai desain)
#
# Sistem variabel (Andy):
#   poin_curiga=0 ; pengacara_percaya=2 (ANGKA; Babak 3 auto -2) ; saksi_hancur=False
#
# --- NORMALISASI UKURAN SPRITE --------------------------------------------
# Tiap ekspresi digambar dengan skala berbeda di kanvas 1024x1536-nya, jadi
# SETIAP gambar dinormalkan sendiri (crop dari atas kepala + zoom) supaya tampil
# sebagai bust dengan tinggi layar SAMA (720px) & kepala sejajar. Angka dihitung
# dari alpha (threshold >200): zoom = 1150/tinggi-solid, crop mulai kepala-25px.
#
# --- SIAPA BICARA (voice) --------------------------------------------------
#   det/law/wit/vic/hak = tokoh (kotak nama).  mc = MC bicara lantang ("Aku").
#   mcb = MC batin ("Aku (batin)").  narr = narasi objektif (tanpa nama, italic).
#   -> Semua kalimat orang-pertama pakai mcb; narr hanya untuk aksi/suara objektif.
#
# CATATAN Ren'Py: literal "[" di teks HARUS ditulis "[[" (sintaks variabel).
# ==========================================================================


# ==========================================================================
# 0. CHANNEL AUDIO TAMBAHAN
# ==========================================================================
init python:
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)


# ==========================================================================
# 1. KARAKTER
# ==========================================================================
define det  = Character("Detektif", color="#e06666", who_outlines=[(2, "#3a0d0d", 0, 0)])
define law  = Character("Pengacara", color="#6fa8dc", who_outlines=[(2, "#0d2033", 0, 0)])
define wit  = Character("Saksi", color="#d9c15a", who_outlines=[(2, "#33290d", 0, 0)])
define vic  = Character("Rendra", color="#c98f8f", who_outlines=[(2, "#331616", 0, 0)])
define hak  = Character("Hakim", color="#c9a86a", who_outlines=[(2, "#332810", 0, 0)])
define mc   = Character("Jokiwi", color="#e8e8e8", who_outlines=[(2, "#222222", 0, 0)])
define mcb  = Character("Jokiwi", color="#b9b9d6", what_italic=True, who_suffix=" (batin)")
define narr = Character(None, what_italic=True)


# ==========================================================================
# 2. DEFINISI GAMBAR  (sprite sudah dinormalkan: bust 720px, kepala sejajar)
# ==========================================================================
image bg redup   = Transform("images/background/bg_kelas666_redup.png", zoom=0.703)
image bg terang  = Transform("images/background/bg_kelas666_terang.png", zoom=0.703)
image trauma     = Transform("images/background/bg_kelas666_siluet_hitam.png", zoom=0.703)

# Sprite hasil NORMALISASI FISIK (images/norm/): tiap ekspresi diskalakan agar
# ukuran kepala sama & kepala sejajar di kanvas seragam 1000x1300, halo dipangkas.
# Ditampilkan dengan zoom seragam 0.72.
# --- Detektif ---
image detektif normal     = Transform("images/norm/detektif_normal.png", zoom=0.72)
image detektif intimidasi = Transform("images/norm/detektif_intimidasi.png", zoom=0.72)
image detektif tegang     = Transform("images/norm/detektif_tegang.png", zoom=0.72)
image detektif terkejut   = Transform("images/norm/detektif_terkejut.png", zoom=0.72)
image detektif terdiam    = Transform("images/norm/detektif_terdiam.png", zoom=0.72)

# --- Pengacara ---
image pengacara pd     = Transform("images/norm/pengacara_pd.png", zoom=0.72)
image pengacara ragu   = Transform("images/norm/pengacara_ragu.png", zoom=0.72)
image pengacara marah  = Transform("images/norm/pengacara_marah.png", zoom=0.72)
image pengacara curiga = Transform("images/norm/pengacara_curiga.png", zoom=0.72)
image pengacara lega   = Transform("images/norm/pengacara_lega.png", zoom=0.72)
image pengacara diam   = Transform("images/norm/pengacara_diam.png", zoom=0.72)
image pengacara dingin = Transform("images/norm/pengacara_dingin.png", zoom=0.72)

# --- Saksi (petugas kebersihan malam) ---
image saksi normal   = Transform("images/norm/saksi_normal.png", zoom=0.72)
image saksi arogan   = Transform("images/norm/saksi_arogan.png", zoom=0.72)
image saksi gugup    = Transform("images/norm/saksi_gugup.png", zoom=0.72)
image saksi panik    = Transform("images/norm/saksi_panik.png", zoom=0.72)
image saksi menangis = Transform("images/norm/saksi_menangis.png", zoom=0.72)

# --- MC (Jokiwi) & Korban (Rendra) ---
image mc normal = Transform("images/norm/mc_normal.png", zoom=0.72)
image korban    = Transform("images/norm/korban.png", zoom=0.72)


# ==========================================================================
# 3. TRANSFORM: flip (arah hadap), posisi slot, & animasi
#    Pemakaian: show X at [flip,] place_<slot>, <anim>
#    - flip   : mirror horizontal (detektif & pengacara menghadap keluar -> dibalik)
#    - place_*: posisi x + animasi masuk (kepala rata di atas, sama untuk semua)
#    - anim   : breathing / tremble / tremble_distress
# ==========================================================================
transform flip:
    xzoom -1.0

transform place_left:
    subpixel True
    xanchor 0.5 yanchor 0.0 xpos 0.19 ypos 0.12
    on show:
        alpha 0.0 xoffset -260
        easein 0.45 alpha 1.0 xoffset 0
    on replace:
        alpha 1.0 xoffset 0
    on hide:
        easeout 0.4 alpha 0.0 xoffset -220

transform place_right:
    subpixel True
    xanchor 0.5 yanchor 0.0 xpos 0.81 ypos 0.12
    on show:
        alpha 0.0 xoffset 260
        easein 0.45 alpha 1.0 xoffset 0
    on replace:
        alpha 1.0 xoffset 0
    on hide:
        easeout 0.4 alpha 0.0 xoffset 220

transform place_center:
    subpixel True
    xanchor 0.5 yanchor 0.0 xpos 0.5 ypos 0.12
    on show:
        alpha 0.0 yoffset 50
        easein 0.45 alpha 1.0 yoffset 0
    on replace:
        alpha 1.0 yoffset 0
    on hide:
        easeout 0.4 alpha 0.0 yoffset 40

transform breathing:
    subpixel True
    block:
        ease 2.4 yoffset -7
        ease 2.4 yoffset 0
        repeat

transform tremble:
    subpixel True
    block:
        ease 0.045 xoffset 6
        ease 0.045 xoffset -6
        repeat

transform tremble_distress:
    subpixel True
    matrixcolor SaturationMatrix(0.5) * BrightnessMatrix(-0.05)
    block:
        ease 0.04 xoffset 8
        ease 0.04 xoffset -8
        repeat

define flash_red = Fade(0.06, 0.0, 0.5, color="#5a0000")
define slam      = Fade(0.02, 0.0, 0.25, color="#000000")


# ==========================================================================
# 4. VARIABEL SISTEM
# ==========================================================================
default poin_curiga = 0
default pengacara_percaya = 2
default saksi_hancur = False

define CURIGA_THRESHOLD = 3


# ==========================================================================
# 5. PROLOG — MALAM ITU  (Kelas 666, jam 2 pagi)
# ==========================================================================
label start:

    scene black
    with Pause(0.3)

    play music "audio/bgm/bgm_prolog_malam.mp3" fadein 2.0 volume 0.8
    play ambient "audio/sfx/sfx_jam_dinding.mp3" fadein 1.0 volume 0.55

    centered "{size=50}KELAS 666{/size}\n\n{size=28}Prolog — Malam Itu{/size}"

    mcb "Namaku Jokiwi. Siswa teladan, nilai sempurna, kebanggaan sekolah. Tak seorang pun tahu ada satu kesalahan di masa laluku."
    mcb "Kesalahan yang dipakai seseorang untuk memerasku selama berbulan-bulan."
    mcb "Malam ini aku mengakhirinya. Kalau soal ujian besok kucuri lebih dulu, dia tak punya apa-apa lagi untuk ditagihkan padaku."

    play sound "audio/sfx/sfx_langkah_pelan.mp3"
    scene bg redup with Dissolve(0.8)
    show mc normal at place_left, breathing
    with Dissolve(0.5)
    mcb "Kelas 666. Jam dua pagi. Aku menyelinap lewat jendela yang lupa dikunci."

    play sound "audio/sfx/sfx_brankas_decit.mp3"
    mcb "...Brankas soalnya sudah terbuka? Siapa yang ke sini sebelum aku?"

    play sound "audio/sfx/sfx_heartbeat.mp3"
    show korban at place_right, breathing
    with Dissolve(0.5)
    vic "Wah, wah. Si anak teladan malah nekat juga malam ini."
    mcb "Dia. Bandar kunci jawaban — orang yang selama ini memerasku."
    vic "Tenang. Selama kamu terus bayar, rahasiamu aman. Tapi kalau berani macam-macam malam ini..."

    show korban at place_right, tremble
    vic "...aku bisa hancurkan masa depanmu detik ini juga."
    menu:
        "Dia mencengkeram kerahmu. Apa yang kau lakukan?"

        "Mendorongnya menjauh sekuat tenaga.":
            mc "Lepaskan aku!"
        "Berusaha merebut rekaman di tangannya.":
            mc "Berikan itu padaku!"

    stop ambient fadeout 1.0
    play sound "audio/sfx/sfx_dorongan_benturan.mp3"
    scene black with slam
    with vpunch
    narr "Suara dorongan. Sebuah benda jatuh menghantam sudut meja. Lalu — hening."
    mcb "Aku tidak ingat persis apa yang terjadi. Yang kuingat cuma suara benturan keras, lalu tubuhnya tak bergerak lagi."

    play sound "audio/sfx/sfx_sirene_polisi.mp3"
    narr "Dari kejauhan, sirene polisi. Semakin lama semakin dekat."
    mcb "Tanganku gemetar. Ada yang basah di ujung kemejaku. Lampu senter menyorot wajahku sebelum aku sempat berpikir."

    stop music fadeout 1.5

    call babak_1
    call babak_2
    call babak_3

    return


# ==========================================================================
# BABAK 1 — TEKANAN
# ==========================================================================
label babak_1:

    scene black with Dissolve(0.6)
    centered "{size=40}Babak 1 — Ruang Interogasi{/size}\n\n{size=26}Beberapa jam kemudian.{/size}"

    play sound "audio/sfx/sfx_desk_slam.mp3"
    scene black with slam
    with vpunch
    play music "audio/bgm/bgm_interrogation.mp3" fadein 1.2 volume 0.85

    scene bg redup with Dissolve(0.6)
    show detektif intimidasi at flip, place_right, breathing
    with Dissolve(0.3)
    det "Aku Detektif yang menangani kasusmu. Kamu tertangkap basah di Kelas 666 bersama mayat dan brankas soal yang terbuka. Jangan mengelak lagi."

    show pengacara pd at flip, place_left, breathing
    with Dissolve(0.4)
    law "Dan aku pengacara yang ditunjuk mendampingimu. Jangan jawab terburu-buru — katakan yang sejujurnya, apa yang kamu lakukan di sana jam dua pagi?"

    mcb "Pengacara ini satu-satunya perisaiku. Kalau dia berhenti percaya, aku habis. Tapi noda di kemejaku tak boleh terbongkar."

    menu:
        "Bagaimana kau menjawab?"

        "\"Saya hanya kebetulan lewat dan melihat pintu terbuka.\"":
            $ poin_curiga += 1
            show detektif intimidasi at flip, place_right, breathing
            mc "Saya... hanya kebetulan lewat. Pintunya terbuka, jadi saya masuk."
            det "Kebetulan? Jendela dibuka paksa, brankas dibongkar. 'Kebetulan lewat' tidak menjelaskan itu."
            show pengacara ragu at flip, place_left, breathing
            law "(Alasan itu terlalu tipis...)"

        "\"Saya memang berniat mencuri soal ujian, tapi saya tidak membunuh siapa pun!\"":
            $ pengacara_percaya += 1
            mc "Saya jujur saja. Saya ke sana untuk mengambil soal ujian — itu salah, saya akui. Tapi saya tidak membunuh siapa pun."
            show detektif terdiam at flip, place_right, breathing
            det "...Setidaknya kau punya nyali untuk mengakui satu dosa."
            show pengacara pd at flip, place_left, breathing
            law "(Bagus. Kejujuran parsial membuatmu terlihat manusiawi, bukan monster.)"

        "\"Itu bukan urusan Anda! Saya minta pulang!\"":
            $ poin_curiga += 2
            $ pengacara_percaya -= 1
            play sound "audio/sfx/sfx_desk_slam.mp3"
            with hpunch
            mc "Itu bukan urusan Anda! Saya minta pulang sekarang juga!"
            show detektif intimidasi at flip, place_right, breathing
            det "Menuntut pulang? Orang tak berdosa tidak berteriak seperti hewan terpojok."
            show pengacara curiga at flip, place_left, breathing
            law "(Tenanglah... kau menggali kuburmu sendiri.)"

    show detektif normal at flip, place_right, breathing
    det "Kita simpan jawabanmu. Sebentar lagi kau akan bertemu seseorang yang katanya melihat semuanya."
    return


# ==========================================================================
# BABAK 2 — KONTRADIKSI
# ==========================================================================
label babak_2:

    show detektif normal at flip, place_right, breathing
    det "Ada petugas kebersihan malam yang piket. Dia mengaku melihatmu — bersembunyi di balik meja saat kamu memukul korban."

    play sound "audio/sfx/sfx_langkah_pelan.mp3"
    show saksi arogan at place_center, breathing
    with Dissolve(0.5)
    wit "I-iya... Saya lihat semuanya! Ruangannya memang gelap, tapi saya lihat dia memukul korban pakai kursi kayu!"

    mcb "Dia berbohong. Korban jatuh membentur sudut meja, bukan dipukul kursi. Tapi kalau aku membetulkannya, aku justru mengaku ada di sana."

    show pengacara curiga at flip, place_left, breathing
    law "Ada yang janggal. Ruangan gelap, tapi ia tahu detail senjatanya. Perhatikan baik-baik."
    play sound "audio/sfx/sfx_heartbeat.mp3"

    menu:
        "Serang kesaksian Saksi:"

        "\"Kursi kayu terlalu berat untuk saya angkat!\"":
            $ poin_curiga += 1
            mc "Kursi kayu itu berat! Mana mungkin saya mengangkatnya sendirian!"
            show saksi arogan at place_center, breathing
            wit "Berat? Adrenalin bisa membuat orang mengangkat apa saja. Argumen lemah."
            show pengacara ragu at flip, place_left, breathing
            law "(Kau menyerang hal yang salah, dan malah terdengar defensif.)"
            show detektif intimidasi at flip, place_right, breathing
            det "Kesaksian tetap berdiri. Kau tak menggoyahkan apa pun."

        "\"Jika ruangan gelap total, bagaimana kamu bisa tahu pasti senjata yang digunakan?\"":
            $ poin_curiga -= 1
            $ pengacara_percaya += 1
            $ saksi_hancur = True
            mc "Tunggu. Kau bilang ruangannya {b}gelap total{/b}."
            mc "Lalu bagaimana kau tahu {i}persis{/i} senjatanya kursi kayu? Bagaimana kau melihatnya sejelas itu dalam gelap gulita?"
            show saksi gugup at place_center, tremble
            with hpunch
            wit "I-itu... s-saya... saya kan cuma..."
            show pengacara pd at flip, place_left, breathing
            law "Jawab. Kalau ruangan gelap total, apa yang sebenarnya bisa kau lihat?"

            stop music fadeout 1.0
            show detektif terkejut at flip, place_right, breathing
            with hpunch
            det "...Ruangan gelap?"

            play music "audio/bgm/bgm_panic.mp3" fadein 0.8 volume 0.85
            show saksi panik at place_center, tremble_distress
            play sound "audio/sfx/sfx_heartbeat.mp3"
            wit "Baik! BAIK! Saya mengaku!"
            show saksi menangis at place_center, tremble_distress
            wit "Saya tidak melihat pembunuhannya! Saya datang ke sana {i}setelah{/i} kejadian — cuma mau menyalin kunci jawaban untuk saya jual!"
            wit "Waktu saya masuk, mayatnya sudah tergeletak. Saya panik, takut dituduh, jadi saya karang cerita itu!"

            show pengacara lega at flip, place_left, breathing
            law "Kesaksian dibatalkan. Satu-satunya 'saksi mata' baru saja mengaku berbohong."
            mcb "Jadi dia pun pencuri yang berbohong demi menutupi dirinya sendiri. Aku... aku menang? Ini sudah selesai?"

    hide saksi with Dissolve(0.5)
    return


# ==========================================================================
# BABAK 3 — BUKTI ABSOLUT & PENENTUAN NASIB
# ==========================================================================
label babak_3:

    show detektif tegang at flip, place_right, breathing
    with Dissolve(0.3)
    if saksi_hancur:
        det "Bagus. Saksi kita coret dari daftar pembunuh."
    else:
        det "Kesaksian tadi masih berdiri. Tapi itu bahkan bukan kartu terkuatku."

    play sound "audio/sfx/sfx_paper_rustle.mp3"
    show detektif intimidasi at flip, place_right, breathing
    det "Kami menemukan ponsel korban. Isinya draf pesan ancaman untukmu — bukti dia memerasmu."
    det "Dan yang paling fatal: ada serpihan kain kemejamu di bawah kuku korban."

    play sound "audio/sfx/sfx_dramatic_hit.mp3" volume 0.7
    play music "audio/bgm/bgm_panic.mp3" fadein 1.0 volume 0.85
    show pengacara marah at flip, place_left, breathing
    with vpunch
    law "Kamu..."
    law "Kamu... membohongiku?"

    $ pengacara_percaya -= 2

    mcb "Pesan ancaman itu membuktikan korban memerasku — motif yang kusembunyikan sejak awal. Apa pun yang kukatakan sekarang harus cukup untuk meyakinkan pengacaraku kembali."

    # ---------------- KONDISI A : poin_curiga >= 3 ----------------
    if poin_curiga >= CURIGA_THRESHOLD:
        show detektif normal at flip, place_right, breathing
        det "Kamu sudah membuktikan diri sendiri, hanya lewat caramu menjawab sejak awal. Bukti ini tinggal formalitas."
        show pengacara diam at flip, place_left, breathing
        with Dissolve(0.4)
        narr "Pengacara menunduk, tak lagi membela."
        mcb "Aku kehabisan cara. Semua jalan sudah tertutup jauh sebelum bukti ini muncul."
        jump ending_bad

    # ---------------- KONDISI B : saksi_hancur ? ----------------
    if saksi_hancur:
        if pengacara_percaya >= 1:
            show pengacara curiga at flip, place_left, breathing
            law "Saksi sudah kehilangan kredibilitas di depan hakim. Tapi bukti ini terlalu kuat untuk diabaikan. Ceritakan yang sebenarnya — aku akan cari cara membelamu."
            menu:
                "Keputusan terakhirmu:"
                "\"Saksi itu yang masuk untuk mencuri kunci jawaban! Dia mengarang cerita untuk menutupi jejaknya!\"":
                    jump ending_normal
                "\"Saya tidak bermaksud membunuhnya. Kami bergumul, dia terjatuh membentur meja. Saya panik dan kabur.\"":
                    jump ending_true
        else:
            show pengacara dingin at flip, place_left, breathing
            law "Aku sudah tidak yakin dengan ucapanmu. Satu-satunya cara aku bisa membantu adalah kalau kamu menunjuk arah lain. Titik."
            menu:
                "Hanya ada satu jalan tersisa:"
                "\"Saksi itu yang sebenarnya masuk untuk mencuri kunci jawaban! Dia yang harus bertanggung jawab!\"":
                    jump ending_normal

    else:
        if pengacara_percaya >= 1:
            show pengacara curiga at flip, place_left, breathing
            law "Kesaksian itu masih kuat di mata hakim, tak bisa kita serang lagi. Tapi aku masih percaya kamu bukan pembunuh berencana. Katakan yang sebenarnya."
            menu:
                "Hanya ada satu jalan tersisa:"
                "\"Saya tidak bermaksud membunuhnya. Itu kecelakaan saat kami bergumul. Saya panik dan kabur.\"":
                    jump ending_true
        else:
            show pengacara dingin at flip, place_left, breathing
            law "Aku sudah tidak bisa berbuat apa-apa lagi. Kesaksian itu masih berlaku, dan kamu bahkan tidak jujur padaku sejak awal."
            narr "Pengacara menutup map di tangannya."
            mcb "Tidak ada jalan keluar lagi. Kebohonganku terlalu dalam untuk dibongkar sekarang."
            jump ending_bad


# ==========================================================================
# ENDINGS  (Ruang Sidang, beberapa minggu kemudian)
# ==========================================================================

label ending_bad:
    scene black with Dissolve(1.0)
    pause 0.3
    centered "{size=40}Ruang Sidang{/size}\n\n{size=26}Beberapa minggu kemudian.{/size}"
    play music "audio/bgm/bgm_ruang_sidang.mp3" fadein 1.2 volume 0.8
    play ambient "audio/sfx/sfx_gumama_sidang.mp3" fadein 1.0 volume 0.45

    scene bg redup with Dissolve(0.8)
    show detektif normal at flip, place_right, breathing
    with Dissolve(0.4)
    det "Yang Mulia, seluruh bukti menunjukkan niat dan tindakan terdakwa. Poin kecurigaan yang terus meningkat sejak awal membuktikan ia tak pernah berniat jujur sejak hari pertama."

    show pengacara diam at flip, place_left, breathing
    with Dissolve(0.4)
    narr "Pengacara menunduk, tak mengangkat argumen apa pun."

    stop ambient fadeout 1.5
    hak "Berdasarkan seluruh bukti dan kesaksian yang dipaparkan, pengadilan memutuskan terdakwa bersalah atas pembunuhan berencana."

    play sound "audio/sfx/sfx_palu_tegas.mp3"
    with vpunch
    mcb "Aku menunggu penyesalan atau ketakutan datang. Yang datang justru kekosongan. Aku kehilangan kesempatan membela diri jauh sebelum sidang ini dimulai."

    scene black with Dissolve(1.5)
    mcb "Pintu besi tertutup di belakangku. Untuk pertama kalinya, aku benar-benar sendirian dengan kebohongan yang kubuat sendiri."
    centered "{size=72}BAD ENDING{/size}\n\n{size=40}Penjara Maksimal{/size}"
    jump the_end


label ending_normal:
    scene black with Dissolve(1.0)
    pause 0.3
    centered "{size=40}Ruang Sidang{/size}\n\n{size=26}Beberapa minggu kemudian.{/size}"
    play music "audio/bgm/bgm_ruang_sidang.mp3" fadein 1.2 volume 0.8
    play ambient "audio/sfx/sfx_gumama_sidang.mp3" fadein 1.0 volume 0.45

    scene bg terang with Dissolve(0.8)
    show pengacara pd at flip, place_left, breathing
    with Dissolve(0.4)
    law "Yang Mulia, kesaksian yang menjadi dasar tuduhan mengandung kontradiksi besar. Saksi sendiri mengakui berada di lokasi untuk tujuan berbeda dari yang ia sampaikan."

    play sound "<from 0 to 3.5>audio/sfx/sfx_tangis_diseret.mp3" fadeout 0.6 volume 0.35
    show saksi menangis at place_center, tremble_distress
    with Dissolve(0.5)
    wit "Saya... saya cuma mau menyalin kunci jawaban juga! Saya nggak ada hubungannya sama kematian itu!"

    show detektif terkejut at flip, place_right, breathing
    with Dissolve(0.4)
    narr "Detektif terdiam, menatap berkas di tangannya."

    hide saksi with Dissolve(0.4)
    stop ambient fadeout 1.5
    hak "Mengingat kredibilitas kesaksian yang runtuh, dan tidak adanya bukti langsung yang mengaitkan terdakwa dengan kekerasan, pengadilan membebaskan terdakwa dari seluruh tuduhan."

    scene black with Dissolve(1.2)
    mcb "Aku bebas. Tapi kebebasan ini seperti utang yang belum kubayar. Aku tahu persis apa yang terjadi malam itu — dan itu bukan Saksi."
    mcb "Mungkin suatu hari kebenaran ini akan mengejarku kembali. Tapi untuk sekarang, aku memilih berjalan terus."
    centered "{size=72}NORMAL ENDING{/size}\n\n{size=40}Kambing Hitam{/size}"
    jump the_end


label ending_true:
    scene black with Dissolve(1.0)
    pause 0.3
    centered "{size=40}Ruang Sidang{/size}\n\n{size=26}Beberapa minggu kemudian.{/size}"
    play music "audio/bgm/bgm_ruang_sidang.mp3" fadein 1.2 volume 0.8
    play ambient "audio/sfx/sfx_gumama_sidang.mp3" fadein 1.0 volume 0.4

    scene bg terang with Dissolve(0.8)
    show pengacara pd at flip, place_left, breathing
    with Dissolve(0.4)
    law "Yang Mulia, klien saya tidak pernah berniat mengakhiri nyawa siapa pun. Yang terjadi malam itu adalah kecelakaan dalam situasi penuh tekanan — bukan tindakan yang direncanakan."

    # Momen KUNCI: kamera lepas dari POV, wajah MC ditampilkan penuh
    show mc normal at place_center, breathing
    with Dissolve(0.6)
    mc "Saya panik. Saya cuma mau kabur, bukan menyakiti siapa pun. Tapi saya terlalu takut mengatakan yang sebenarnya sejak awal."

    narr "Hakim menimbang lama, membolak-balik berkas."
    stop ambient fadeout 1.5
    hak "Pengadilan mempertimbangkan pengakuan jujur terdakwa serta tidak adanya unsur perencanaan dalam peristiwa ini."

    play sound "audio/sfx/sfx_palu_pelan.mp3"
    hak "Terdakwa dinyatakan bersalah atas kelalaian yang mengakibatkan kematian, dengan hukuman yang telah mempertimbangkan pengakuan dan kerja samanya."

    show pengacara lega at flip, place_left, breathing
    narr "Pengacara menepuk pundakku."
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
