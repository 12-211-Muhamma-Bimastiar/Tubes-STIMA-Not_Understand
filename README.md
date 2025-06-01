# Tubes-STIMA-Not_Understand

> by Not Understand

## Table of Contents

- [General Information](#general-information)
- [File Structures](#file-structures)
- [Requirement](#requirement)
- [Setup and Usage](#setup-and-usage)
- [Authors](#authors)

## General Information

Bot otomatis untuk permainan Diamonds dengan strategi greedy<br>
Terkait permainan dapat dilihat pada pranala [ini](https://drive.google.com/file/d/17_d7sRWhr0TspjS0ZqIIQCnQnElPaeDR/view)<br>

Algoritma greedy yang digunakan sebagai berikut:

1. Bot akan mencari diamond terdekat
2. Bot akan mengutamakan diamond merah apabila selisihnya dengan diamond biru cukup signifikan
3. Jika menggunakan portal lebih cepat, bot akan memilih lewat portal
4. Bot akan memilih tombol merah jika jaraknya hanya sedikit lebih jauh dari diamond
5. Jika inventory penuh atau waktu hampir habis, bot akan kembali ke base
6. Bot menghindari portal kecuali jika sedang menuju portal sebagai target
7. Bot akan tackle musuh jika berada dalam jarak 2 langkah secara diagonal
8. Jika musuh terlalu dekat (jarak 3 langkah), bot akan menghindar dan memilih diamond di arah berbeda

## File Structures
```
*
├── doc
│   └── Not_Understand.pdf
└── src
    ├── __pycache__
    │   └── decode.cpython-311.pyc
    ├── game
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── api.cpython-311.pyc
    │   │   ├── board_handler.cpython-311.pyc
    │   │   ├── bot_handler.cpython-311.pyc
    │   │   ├── models.cpython-311.pyc
    │   │   └── util.cpython-311.pyc
    │   ├── logic
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── base.cpython-311.pyc
    │   │   │   ├── Not_U.cpython-311.pyc
    │   │   │   └── random.cpython-311.pyc
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── Not_U.py
    │   │   └── random.py
    │   ├── __init__.py
    │   ├── api.py
    │   ├── board_handler.py
    │   ├── bot_handler.py
    │   ├── models.py
    │   └── util.py
    ├── gitignore
    ├── decode.py
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── run-bots.bat
    └── run-bots.sh
```

## Requirement

- `Python` 3.X
- `Node.js` install pada pranala [berikut](https://nodejs.org/en)
- Docker dekstop install pada pranala [berikut](https://www.docker.com/products/docker-desktop/)
- Instalasi library python pada `src/requirement.txt`
- Yarn, install dengan perintah berikut
```
npm install --global yarn
```

## Setup and Usage

1. Download dan lakukan instalasi game engine dengan mengikuti instruksi pada pranala [berikut](https://docs.google.com/spreadsheets/d/1FJ0SS6AtDuOtYBe7_bViBHV0cmOipCHIhLPDQMhwvlE/edit?gid=0#gid=0)
2. Clone repository berikut `https://github.com/12-211-Muhamma-Bimastiar/Tubes-STIMA-Not_Understand.git`
3. Ganti ke root directory folder src dengan perintah `cd src`
4. Install package python dengan perintah `pip install -r requirement.txt`
5. Untuk menjalankan bot, nyalakan terlebih dahulu game engine
6. Untuk menjalankan satu bot, jalankan perintah

```
python main.py --logic MyBot --email=your_email@example.com --name=your_name --password=your_password --team etimo
```

Untuk menjalankan beberapa bot sekaligus jalankan perintah berikut
- Untuk Windows
```
./run-bots.bat
```
- Untuk Linux
```
./run-bots.sh
```
7. Bot sudah dapat berjalan

## Authors

| NIM       | Nama                     |
| --------- | ------------------------ |
| 123140014 | Alliyah Salsabilla       |
| 123140201 | Awi Septian Preasetyo    |
| 123140211 | Muhammad Bimastiar       |
