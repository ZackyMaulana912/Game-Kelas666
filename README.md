# Kelas 666

> Visual novel interogasi bergaya *courtroom drama* — dibuat dengan **Ren'Py**.

MC tertangkap di Kelas 666 pada malam hari bersama sebuah mayat dan brankas soal ujian yang terbuka. Seorang saksi menudingnya sebagai pembunuh. Lewat tiga babak interogasi yang menegangkan, pemain harus menyusun kebohongan, mematahkan kesaksian, dan menentukan nasib MC sendiri — dengan **3 ending** berbeda.

---

## Tentang Game

| | |
|---|---|
| **Genre** | Visual Novel / Mystery / Interrogation Drama |
| **Engine** | Ren'Py 8.6.0 |
| **Resolusi** | 1920 × 1080 |
| **Sudut Pandang** | First-Person (layar = mata MC) |
| **Platform Target** | macOS (`.app` / `.dmg`) & Windows (`.exe`) |

### Tiga Ending
- **Bad Ending — Penjara Maksimal:** kebohongan runtuh, hukuman berat.
- **Normal Ending — Kambing Hitam:** saksi disalahkan, MC selamat tapi di-DO.
- **True Ending — Manslaughter:** MC mengaku, skandal pemerasan terbongkar.

Ending ditentukan oleh akumulasi variabel: `poin_curiga`, `pengacara_percaya`, dan `saksi_hancur`.

---

## Struktur Project

```
Game-Kelas666/
├── game/
│   ├── script.rpy      # Alur cerita & logika percabangan
│   ├── options.rpy     # Konfigurasi game & build
│   ├── gui.rpy         # Pengaturan tampilan (1920×1080)
│   ├── images/         # Sprite karakter & background
│   └── audio/
│       ├── bgm/        # Musik latar
│       └── sfx/        # Efek suara
└── README.md
```

---

## Cara Menjalankan

**Butuh:** [Ren'Py SDK 8.6.0](https://www.renpy.org/latest.html)

### Lewat Ren'Py Launcher (disarankan)
1. Buka **Ren'Py Launcher**.
2. Set **projects directory** ke folder yang memuat `Game-Kelas666`.
3. Pilih project **Game-Kelas666** → klik **Launch Project**.

### Lewat terminal (macOS)
```bash
~/renpy-8.6.0-sdk/renpy.app/Contents/MacOS/renpy /path/ke/Game-Kelas666
```

---

## Build Distribusi

Lewat **Ren'Py Launcher → Build Distributions**, centang target Mac & Windows:

| Platform | Output |
|----------|--------|
| macOS | `.app` → dibungkus jadi `.dmg` |
| Windows | `.exe` |

---

## Tim

| Peran | Anggota |
|-------|---------|
| Lead Programmer | **Zacky** |
| Narrative Designer | Andy |
| Character Artist | Venerdi |
| Environment & Audio | Deva |
| QA & Script Editor | Vichras |

---

## Status Pengembangan

- [x] **Minggu 1** — Setup project, deklarasi variabel, prototipe logika 3 ending *(lint lulus)*
- [ ] **Minggu 2** — Naskah penuh + sprite diwarnai
- [ ] **Minggu 3** — Integrasi aset gambar & audio (beta build)
- [ ] **Minggu 4** — Testing, polish, build final `.app` / `.dmg` / `.exe`
