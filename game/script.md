# Naskah Game: Kelas 666 — Versi Lengkap (sesuai `script.rpy`)

> Dokumen ini adalah salinan **naskah final yang benar-benar berjalan di game** (`game/script.rpy`),
> ditulis ulang dalam bentuk markdown agar mudah dibaca tim naskah/QA.
> Berbeda dengan versi di folder `Progres_Minggu_*` karena naskah asli sudah melalui adaptasi & integrasi.
>
> - **Basis alur & sistem variabel:** `Progres_Minggu_2/Naskah.md` (Andy)
> - **Lead Programmer / adaptasi:** Zacky
> - **Resolusi:** 1920 × 1080 · **Engine:** Ren'Py 8.6.0
> - **POV:** First-person (layar = mata MC). MC hanya ditampilkan penuh di reveal True Ending.

---

## Casting Adaptasi

| Kode | Tokoh | Warna Nama | Peran |
|------|-------|------------|-------|
| `mc` | **Jokiwi (MC)** | Putih | MC. Siswa teladan yang diperas. Bicara lantang. Kotak nama menampilkan "Jokiwi (MC)". |
| `mcb` | **Jokiwi (batin)** | Ungu pudar, miring | Suara batin MC (orang pertama). |
| `det` | **Detektif** | Merah | Menekan MC. |
| `law` | **Pengacara** | Biru | Pendamping MC; kepercayaannya menentukan ending. |
| `wit` | **Saksi** | Kuning | Petugas kebersihan malam; pencuri kunci jawaban. |
| `vic` | **Rendra** | Merah muda | Korban — bandar contekan yang memeras Jokiwi. |
| `hak` | **Hakim** | Emas | Pembaca vonis di ruang sidang. |
| `narr` | *(narasi)* | — | Narasi objektif (aksi/suara), tanpa kotak nama, miring. |

---

## Sistem Variabel

```python
default poin_curiga        = 0      # Naik bila bantahan MC tidak logis
default pengacara_percaya  = 2      # ANGKA (awal 2). Babak 3 otomatis -2
default saksi_hancur       = False  # True bila kesaksian Saksi berhasil dipatahkan

define CURIGA_THRESHOLD = 3         # Ambang batas menuju Bad Ending
```

**Cara kerja percabangan (akhir Babak 3):**
1. Jika `poin_curiga >= 3` → **Bad Ending** (langsung, tak peduli variabel lain).
2. Selain itu, cek `saksi_hancur` dan `pengacara_percaya` untuk menentukan pilihan menu terakhir → Normal / True / Bad.

---

## PROLOG — Malam Itu
*Kelas 666, jam dua pagi.*

**BGM:** `bgm_prolog_malam.mp3` · **Ambient:** `sfx_jam_dinding.mp3`

> **KELAS 666**
> *Prolog — Malam Itu*

**Jokiwi (batin):** Namaku Jokiwi. Siswa teladan, nilai sempurna, kebanggaan sekolah. Tak seorang pun tahu ada satu kesalahan di masa laluku.

**Jokiwi (batin):** Kesalahan yang dipakai seseorang untuk memerasku selama berbulan-bulan.

**Jokiwi (batin):** Malam ini aku mengakhirinya. Kalau soal ujian besok kucuri lebih dulu, dia tak punya apa-apa lagi untuk ditagihkan padaku.

*(Langkah pelan → scene Kelas 666 redup. MC muncul dari kiri.)*

**Jokiwi (batin):** Kelas 666. Jam dua pagi. Aku menyelinap lewat jendela yang lupa dikunci.

*(Suara brankas berdecit.)*

**Jokiwi (batin):** ...Brankas soalnya sudah terbuka? Siapa yang ke sini sebelum aku?

*(Detak jantung. Rendra muncul dari kanan.)*

**Rendra:** Wah, wah. Si anak teladan malah nekat juga malam ini.

**Jokiwi (batin):** Dia. Bandar kunci jawaban, orang yang selama ini memerasku.

**Rendra:** Tenang. Selama kamu terus bayar, rahasiamu aman. Tapi kalau berani macam-macam malam ini...

*(Rendra bergetar / mengancam.)*

**Rendra:** ...aku bisa hancurkan masa depanmu detik ini juga.

### ▶ PILIHAN — "Rendra mencengkeram kerahku erat-erat. Apa yang harus kulakukan?"

| Pilihan | Dialog MC | Efek |
|---------|-----------|------|
| **Mendorongnya menjauh sekuat tenaga.** | "Lepaskan aku!" | — |
| **Berusaha merebut rekaman di tangannya.** | "Berikan itu padaku!" | — |

*(Kedua pilihan menuju hasil yang sama.)*

*(Ambient berhenti. Suara dorongan & benturan → layar hitam, `vpunch`.)*

**Narasi:** Suara dorongan. Sebuah benda jatuh menghantam sudut meja. Lalu, hening.

**Jokiwi (batin):** Aku tidak ingat persis apa yang terjadi. Yang kuingat cuma suara benturan keras, lalu tubuhnya tak bergerak lagi.

*(Sirene polisi mendekat.)*

**Narasi:** Dari kejauhan, sirene polisi. Semakin lama semakin dekat.

*(Sprite `mc gemetar` muncul di tengah — Jokiwi dengan kemeja bernoda & tangan gemetar.)*
**Jokiwi (batin):** Tanganku gemetar. Ada yang basah di ujung kemejaku. Lampu senter menyorot wajahku sebelum aku sempat berpikir.

---

## BABAK 1 — Tekanan
*Ruang Interogasi. Beberapa jam kemudian.*

**BGM:** `bgm_interrogation.mp3` · **SFX pembuka:** `sfx_desk_slam.mp3` + `vpunch`

**Detektif** *(intimidasi)*: Aku Detektif yang menangani kasusmu. Kamu tertangkap basah di Kelas 666 bersama mayat dan brankas soal yang terbuka. Jangan mengelak lagi.

**Pengacara** *(percaya diri)*: Dan aku pengacara yang ditunjuk mendampingimu. Jangan jawab terburu-buru, katakan yang sejujurnya, apa yang kamu lakukan di sana jam dua pagi?

**Jokiwi (batin):** Pengacara ini satu-satunya perisaiku. Kalau dia berhenti percaya, aku habis. Tapi noda di kemejaku tak boleh terbongkar.

### ▶ PILIHAN — "Bagaimana aku harus menjawab?"

#### A. "Saya hanya kebetulan lewat dan melihat pintu terbuka."
> **Efek:** `poin_curiga += 1`

**Jokiwi:** Saya... hanya kebetulan lewat. Pintunya terbuka, jadi saya masuk.
**Detektif:** Kebetulan? Jendela dibuka paksa, brankas dibongkar. 'Kebetulan lewat' tidak menjelaskan itu.
**Pengacara** *(ragu)*: (Alasan itu terlalu tipis...)

#### B. "Saya memang berniat mencuri soal ujian, tapi saya tidak membunuh siapa pun!"
> **Efek:** `pengacara_percaya += 1`

**Jokiwi:** Saya jujur saja. Saya ke sana untuk mengambil soal ujian, itu salah, saya akui. Tapi saya tidak membunuh siapa pun.
**Detektif** *(terdiam)*: ...Setidaknya kau punya nyali untuk mengakui satu dosa.
**Pengacara** *(pd)*: (Bagus. Kejujuran parsial membuatmu terlihat manusiawi, bukan monster.)

#### C. "Itu bukan urusan Anda! Saya minta pulang!"
> **Efek:** `poin_curiga += 2`, `pengacara_percaya -= 1` · SFX `sfx_desk_slam` + `hpunch`

**Jokiwi:** Itu bukan urusan Anda! Saya minta pulang sekarang juga!
**Detektif** *(intimidasi)*: Menuntut pulang? Orang tak berdosa tidak berteriak seperti hewan terpojok.
**Pengacara** *(curiga)*: (Tenanglah... kau menggali kuburmu sendiri.)

---

**Detektif** *(normal)*: Kita simpan jawabanmu. Sebentar lagi kau akan bertemu seseorang yang katanya melihat semuanya.

---

## BABAK 2 — Kontradiksi
*Ruang Interogasi berlanjut.*

**Detektif** *(normal)*: Ada petugas kebersihan malam yang piket. Katanya, ia sedang bersembunyi di balik meja saat kejadian, dan dari sana ia melihatmu memukul korban.

*(Langkah pelan. Saksi muncul dari tengah, arogan.)*

**Saksi** *(arogan)*: I-iya... Saya lihat semuanya! Ruangannya memang gelap, tapi saya lihat dia memukul korban pakai kursi kayu!

**Jokiwi (batin):** Dia berbohong. Korban jatuh membentur sudut meja, bukan dipukul kursi. Tapi kalau aku membetulkannya, aku justru mengaku ada di sana.

**Pengacara** *(curiga)*: Ada yang janggal. Ruangan gelap, tapi ia tahu detail senjatanya. Perhatikan baik-baik.

*(Detak jantung.)*

### ▶ PILIHAN — "Bagaimana aku harus membantah kesaksiannya?"

#### A. "Kursi kayu terlalu berat untuk saya angkat!" — *(salah sasaran)*
> **Efek:** `poin_curiga += 1`

**Jokiwi:** Kursi kayu itu berat! Mana mungkin saya mengangkatnya sendirian!
**Saksi** *(arogan)*: Berat? Adrenalin bisa membuat orang mengangkat apa saja. Argumen lemah.
**Pengacara** *(ragu)*: (Kau menyerang hal yang salah, dan malah terdengar defensif.)
**Detektif** *(intimidasi)*: Kesaksian tetap berdiri. Kau tak menggoyahkan apa pun.

*(→ `saksi_hancur` tetap `False`.)*

#### B. "Jika ruangan gelap total, bagaimana kamu bisa tahu pasti senjata yang digunakan?" — *(telak)*
> **Efek:** `poin_curiga -= 1`, `pengacara_percaya += 1`, `saksi_hancur = True`

**Jokiwi:** Tunggu. Kau bilang ruangannya **gelap total**.
**Jokiwi:** Lalu bagaimana kau tahu *persis* senjatanya kursi kayu? Bagaimana kau melihatnya sejelas itu dalam gelap gulita?
**Saksi** *(gugup, gemetar)* `hpunch`: I-itu... s-saya... saya kan cuma...
**Pengacara** *(pd)*: Jawab. Kalau ruangan gelap total, apa yang sebenarnya bisa kau lihat?

*(Musik berhenti.)*
**Detektif** *(terkejut)* `hpunch`: ...Ruangan gelap?

*(BGM ganti `bgm_panic.mp3`. Detak jantung.)*
**Saksi** *(panik)*: Baik! BAIK! Saya mengaku!
**Saksi** *(menangis)*: Saya tidak melihat pembunuhannya! Saya datang ke sana *setelah* kejadian, cuma mau menyalin kunci jawaban untuk saya jual!
**Saksi:** Waktu saya masuk, mayatnya sudah tergeletak. Saya panik, takut dituduh, jadi saya karang cerita itu!

**Pengacara** *(lega)*: Kesaksian dibatalkan. Satu-satunya 'saksi mata' baru saja mengaku berbohong.
**Jokiwi (batin):** Jadi dia pun pencuri yang berbohong demi menutupi dirinya sendiri. Aku... aku menang? Ini sudah selesai?

*(Saksi keluar dari layar.)*

---

## BABAK 3 — Bukti Absolut & Penentuan Nasib

**Detektif** *(tegang)*:
- Jika `saksi_hancur` **True**: "Bagus. Saksi kita coret dari daftar pembunuh."
- Jika `saksi_hancur` **False**: "Kesaksian tadi masih berdiri. Tapi itu bahkan bukan kartu terkuatku."

*(Kertas berdesir.)*

**Detektif** *(intimidasi)*: Kami menemukan ponsel korban. Isinya draf pesan ancaman untukmu, bukti dia memerasmu.
**Detektif:** Dan yang paling fatal: ada serpihan kain kemejamu di bawah kuku korban.

*(SFX `sfx_dramatic_hit`. BGM `bgm_panic`. `vpunch`.)*
**Pengacara** *(marah)*: Kamu...
**Pengacara:** Kamu... membohongiku?

> **Efek otomatis:** `pengacara_percaya -= 2`

**Jokiwi (batin):** Pesan ancaman itu membuktikan korban memerasku, motif yang kusembunyikan sejak awal. Apa pun yang kukatakan sekarang harus cukup untuk meyakinkan pengacaraku kembali.

### Pohon Keputusan Ending

```
if poin_curiga >= 3:
    → BAD ENDING (kecurigaan sudah terlanjur menumpuk sejak awal)

elif saksi_hancur == True:
    if pengacara_percaya >= 1:
        MENU:
          • "Saksi itu yang mencuri kunci jawaban..."   → NORMAL ENDING
          • "Saya tidak bermaksud membunuhnya..."       → TRUE ENDING
    else:  # pengacara_percaya < 1
        MENU (satu pilihan):
          • "Saksi itu yang harus bertanggung jawab!"   → NORMAL ENDING

else:  # saksi_hancur == False
    if pengacara_percaya >= 1:
        MENU (satu pilihan):
          • "Saya tidak bermaksud membunuhnya..."       → TRUE ENDING
    else:  # pengacara_percaya < 1
        → BAD ENDING (kesaksian masih berdiri + pengacara menyerah)
```

#### Cabang: `saksi_hancur` & `pengacara_percaya >= 1`
**Pengacara** *(curiga)*: Saksi sudah kehilangan kredibilitas di depan hakim. Tapi bukti ini terlalu kuat untuk diabaikan. Ceritakan yang sebenarnya, aku akan cari cara membelamu.

> **MENU — "Keputusan terakhirku:"**
> - "Saksi itu yang masuk untuk mencuri kunci jawaban! Dia mengarang cerita untuk menutupi jejaknya!" → **Normal Ending**
> - "Saya tidak bermaksud membunuhnya. Kami bergumul, dia terjatuh membentur meja. Saya panik dan kabur." → **True Ending**

#### Cabang: `saksi_hancur` & `pengacara_percaya < 1`
**Pengacara** *(dingin)*: Aku sudah tidak yakin dengan ucapanmu. Satu-satunya cara aku bisa membantu adalah kalau kamu menunjuk arah lain. Titik.

> **MENU — "Hanya ada satu jalan tersisa:"**
> - "Saksi itu yang sebenarnya masuk untuk mencuri kunci jawaban! Dia yang harus bertanggung jawab!" → **Normal Ending**

#### Cabang: `saksi_hancur == False` & `pengacara_percaya >= 1`
**Pengacara** *(curiga)*: Kesaksian itu masih kuat di mata hakim, tak bisa kita serang lagi. Tapi aku masih percaya kamu bukan pembunuh berencana. Katakan yang sebenarnya.

> **MENU — "Hanya ada satu jalan tersisa:"**
> - "Saya tidak bermaksud membunuhnya. Itu kecelakaan saat kami bergumul. Saya panik dan kabur." → **True Ending**

#### Cabang: `saksi_hancur == False` & `pengacara_percaya < 1`
**Pengacara** *(dingin)*: Aku sudah tidak bisa berbuat apa-apa lagi. Kesaksian itu masih berlaku, dan kamu bahkan tidak jujur padaku sejak awal.
**Narasi:** Pengacara menutup map di tangannya.
**Jokiwi (batin):** Tidak ada jalan keluar lagi. Kebohonganku terlalu dalam untuk dibongkar sekarang.
*(→ Bad Ending)*

---

## ENDING — BAD (Penjara Maksimal)
*Ruang Sidang. Beberapa minggu kemudian.*

**BGM:** `bgm_ruang_sidang.mp3` · **Ambient:** `sfx_gumama_sidang.mp3` · **Latar:** Kelas terang.

**Detektif** *(normal)*: Yang Mulia, seluruh bukti menunjukkan niat dan tindakan terdakwa. Poin kecurigaan yang terus meningkat sejak awal membuktikan ia tak pernah berniat jujur sejak hari pertama.

**Pengacara** *(diam)* — **Narasi:** Pengacara menunduk, tak mengangkat argumen apa pun.

**Hakim:** Berdasarkan seluruh bukti dan kesaksian yang dipaparkan, pengadilan memutuskan terdakwa bersalah atas pembunuhan berencana.

*(SFX `sfx_palu_tegas` + `vpunch`.)*
**Jokiwi (batin):** Aku menunggu penyesalan atau ketakutan datang. Yang datang justru kekosongan. Aku kehilangan kesempatan membela diri jauh sebelum sidang ini dimulai.

*(Layar hitam.)*
**Jokiwi (batin):** Pintu besi tertutup di belakangku. Untuk pertama kalinya, aku benar-benar sendirian dengan kebohongan yang kubuat sendiri.

> **BAD ENDING**
> *Penjara Maksimal*

---

## ENDING — NORMAL (Kambing Hitam)
*Ruang Sidang. Beberapa minggu kemudian.*

**BGM:** `bgm_ruang_sidang.mp3` · **Ambient:** `sfx_gumama_sidang.mp3` · **Latar:** Kelas terang.

**Pengacara** *(pd)*: Yang Mulia, kesaksian yang menjadi dasar tuduhan mengandung kontradiksi besar. Saksi sendiri mengakui berada di lokasi untuk tujuan berbeda dari yang ia sampaikan.

*(SFX `sfx_tangis_diseret`. Saksi menangis, diseret keluar.)*
**Saksi** *(menangis)*: Saya... saya cuma mau menyalin kunci jawaban juga! Saya nggak ada hubungannya sama kematian itu!

**Detektif** *(terkejut)* — **Narasi:** Detektif terdiam, menatap berkas di tangannya.

**Hakim:** Mengingat kredibilitas kesaksian yang runtuh, dan tidak adanya bukti langsung yang mengaitkan terdakwa dengan kekerasan, pengadilan membebaskan terdakwa dari seluruh tuduhan.

*(Layar hitam.)*
**Jokiwi (batin):** Aku bebas. Tapi kebebasan ini seperti utang yang belum kubayar. Aku tahu persis apa yang terjadi malam itu, dan itu bukan Saksi.
**Jokiwi (batin):** Mungkin suatu hari kebenaran ini akan mengejarku kembali. Tapi untuk sekarang, aku memilih berjalan terus.

> **NORMAL ENDING**
> *Kambing Hitam*

---

## ENDING - TRUE (Tidak Disengaja)
*Ruang Sidang. Beberapa minggu kemudian.*

**BGM:** `bgm_ruang_sidang.mp3` · **Ambient:** `sfx_gumama_sidang.mp3` · **Latar:** Kelas terang.

**Pengacara** *(pd)*: Yang Mulia, klien saya tidak pernah berniat mengakhiri nyawa siapa pun. Yang terjadi malam itu adalah kecelakaan dalam situasi penuh tekanan, bukan tindakan yang direncanakan.

*(Momen KUNCI: kamera lepas dari POV — wajah MC ditampilkan penuh di tengah.)*
**Jokiwi:** Saya panik. Saya cuma mau kabur, bukan menyakiti siapa pun. Tapi saya terlalu takut mengatakan yang sebenarnya sejak awal.

**Narasi:** Hakim menimbang lama, membolak-balik berkas.
**Hakim:** Pengadilan mempertimbangkan pengakuan jujur terdakwa serta tidak adanya unsur perencanaan dalam peristiwa ini.

*(SFX `sfx_palu_pelan`.)*
**Hakim:** Terdakwa dinyatakan bersalah atas kelalaian yang mengakibatkan kematian, dengan hukuman yang telah mempertimbangkan pengakuan dan kerja samanya.

**Pengacara** *(lega)* — **Narasi:** Pengacara menepuk pundakku.
**Pengacara:** Ini bukan akhir yang sempurna. Tapi ini akhir yang jujur.

*(Layar hitam.)*
**Jokiwi (batin):** Untuk pertama kalinya sejak malam itu, aku bisa bernapas lega. Bukan karena aku bebas, tapi karena aku akhirnya berhenti berbohong, bahkan pada diriku sendiri.

> **TRUE ENDING**
> *Tidak Disengaja*

---

## Penutup

*(Musik & ambient fade out.)*

> **TAMAT**
> *Kelas 666*

---

## Lampiran — Inventaris Aset yang Dipakai Naskah

### BGM (`audio/bgm/`)
| File | Dipakai di |
|------|-----------|
| `bgm_prolog_malam.mp3` | Prolog |
| `bgm_interrogation.mp3` | Babak 1 |
| `bgm_panic.mp3` | Babak 2 (klimaks) & Babak 3 |
| `bgm_ruang_sidang.mp3` | Semua ending |

### SFX (`audio/sfx/`)
`sfx_jam_dinding.mp3` (ambient prolog) · `sfx_langkah_pelan.mp3` · `sfx_brankas_decit.mp3` · `sfx_heartbeat.mp3` · `sfx_dorongan_benturan.mp3` · `sfx_sirene_polisi.mp3` · `sfx_desk_slam.mp3` · `sfx_paper_rustle.mp3` · `sfx_dramatic_hit.mp3` · `sfx_gumama_sidang.mp3` (ambient sidang) · `sfx_palu_tegas.mp3` · `sfx_palu_pelan.mp3` · `sfx_tangis_diseret.mp3`

### Ekspresi Sprite (`images/norm/<karakter>/<ekspresi>.png`)
Sprite dipisah per-karakter dalam subfolder, semua background sudah transparan (PNG RGBA):
- **`detektif/`:** normal, intimidasi, tegang, terkejut, terdiam
- **`pengacara/`:** pd, ragu, marah, curiga, lega, diam, dingin
- **`saksi/`:** normal, arogan, gugup, panik, menangis
- **`mc/`:** normal, gemetar *(kemeja bernoda + tangan gemetar; muncul di Prolog saat "Tanganku gemetar...")*
- **`rendra/`:** normal *(dipakai sebagai image `korban`)*

### Background (`images/background/`)
`bg_kelas666_redup.png` · `bg_kelas666_terang.png` · `bg_kelas666_siluet_hitam.png`

### Efek Layar
`vpunch` / `hpunch` (getar layar) · `flash_red` · `slam` · animasi sprite: `breathing`, `tremble`, `tremble_distress`, slide masuk `place_left/right/center`, sistem **active speaker** (pembicara membesar, lainnya meredup).
