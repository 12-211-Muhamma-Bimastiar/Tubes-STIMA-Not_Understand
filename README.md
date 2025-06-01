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
2. Bot akan mengutamakan diamond merah apabila selisihnya dengan diamond biru kurang dari 3 langkah
3. Bot akan mengambil red button apabila diamond terdekat berada 4 langkah lebih jauh atau lebih dari red button
4. Bot akan mencari diamond terdekat dengan base ketika inventorynya berisi 4 diamond
5. Bot kembali ke base saat inventorynya penuh atau waktu hampir habis
6. Bot mempertimbangkan teleport ketika mencari suatu target dan akan menuju teleport jika jarak menuju tujuan lebih dekat melalui teleport
7. Bot akan mencoba men-tackle musuh jika jaraknya 2 langkah dan musuh berada di posisi diagonal dari bot
8. Bot akan mencari diamond lain apabila terdapat musuh berjarak 3 langkah yang searah dengan diamond terdekat
9. Bot akan menghindari portal jika portal justru menjauhkan bot dengan tujuannya

## File Structures
```
*
├── README.md
├── doc
│   └── tbfoReborn.pdf
└── src
    ├── __pycache__
    │   └── decode.cpython-311.pyc
    ├── decode.py
    ├── game
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── api.cpython-311.pyc
    │   │   ├── board_handler.cpython-311.pyc
    │   │   ├── bot_handler.cpython-311.pyc
    │   │   ├── models.cpython-311.pyc
    │   │   └── util.cpython-311.pyc
    │   ├── api.py
    │   ├── board_handler.py
    │   ├── bot_handler.py
    │   ├── logic
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── base.cpython-311.pyc
    │   │   │   ├── mybot.cpython-311.pyc
    │   │   │   └── random.cpython-311.pyc
    │   │   ├── base.py
    │   │   ├── mybot.py
    │   │   └── random.py
    │   ├── models.py
    │   └── util.py
    ├── main.py
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
2. Clone repository berikut `git clone https://github.com/BryanLauw/Tubes1_tbfoReborn.git`
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
