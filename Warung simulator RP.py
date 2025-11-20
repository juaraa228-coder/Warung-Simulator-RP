import random
import time
import os
import itertools
import math

# ==========================
# UTILS
# ==========================
def round_to_500(x):
    return int(round(x / 500.0) * 500)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def fmt(x):
    return "Rp " + f"{x:,}".replace(",", ".")

# ==========================
# FUNGSI LOADING ESTETIK
# ==========================
def loading(text="Loading...", durasi=1.2):
    spinner = itertools.cycle(["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"])
    akhir = time.time() + durasi
    while time.time() < akhir:
        print(f"\r{next(spinner)} {text}", end="", flush=True)
        time.sleep(0.10)
    print("\r" + " " * 40, end="\r")

# ==========================
# KONFIGURASI AWAL
# ==========================
modal = 300_000
pajak_harian = 4000
rating = 0.0
hari = 1
auto_hari = True

# ==========================
# RIWAYAT PEMBELIAN
# ==========================
riwayat = []   # <=== FITUR BARU

# ==========================
# DATA BARANG DAN PAKET
# ==========================
barang = {
    "Indomie":     {"stok": 0, "beli": round_to_500(3000),  "jual": round_to_500(5000), "paket": 1, "terkunci": False},
    "Teh Botol":   {"stok": 0, "beli": round_to_500(3500),  "jual": round_to_500(6000), "paket": 1, "terkunci": False},
    "Aqua":        {"stok": 0, "beli": round_to_500(2500),  "jual": round_to_500(4000), "paket": 1, "terkunci": False},
    "Beras 1kg":   {"stok": 0, "beli": round_to_500(12000), "jual": round_to_500(16000),"paket": 2, "terkunci": True},
    "Minyak 1L":   {"stok": 0, "beli": round_to_500(14000), "jual": round_to_500(19000),"paket": 2, "terkunci": True},
    "Gula 1kg":    {"stok": 0, "beli": round_to_500(11000), "jual": round_to_500(15000),"paket": 2, "terkunci": True},
    "Telur 1kg":   {"stok": 0, "beli": round_to_500(22000), "jual": round_to_500(28000),"paket": 2, "terkunci": True},
    "Susu Kotak":  {"stok": 0, "beli": round_to_500(5500),  "jual": round_to_500(8000), "paket": 3, "terkunci": True},
    "Shampoo":     {"stok": 0, "beli": round_to_500(5000),  "jual": round_to_500(7500), "paket": 3, "terkunci": True},
    "Detergen":    {"stok": 0, "beli": round_to_500(9000),  "jual": round_to_500(13000),"paket": 3, "terkunci": True},
    "Coklat":      {"stok": 0, "beli": round_to_500(4000),  "jual": round_to_500(7000), "paket": 4, "terkunci": True},
    "Baterai":     {"stok": 0, "beli": round_to_500(6000),  "jual": round_to_500(9000), "paket": 4, "terkunci": True},
    "Saus":        {"stok": 0, "beli": round_to_500(4000),  "jual": round_to_500(6500), "paket": 5, "terkunci": True},
}

biaya_buka_paket = {1:0, 2:28000, 3:40000, 4:55000, 5:70000}
for k in list(biaya_buka_paket.keys()):
    biaya_buka_paket[k] = round_to_500(biaya_buka_paket[k])

bonus_paket = {1:0.0, 2:0.15, 3:0.2, 4:0.25, 5:0.3}

pecahan_uang = [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]

# ==========================
# BANNER
# ==========================
def banner_warung():
    hijau = "\033[92m"
    reset = "\033[0m"
    print(hijau + "===============================================")
    print("              SELAMAT DATANG DI WARUNG RP      ")
    print("===============================================" + reset)

# ==========================
# EVENT RANDOM
# ==========================
def event_random():
    global modal, rating, barang

    daftar_event = [
        ("bonus", 20),
        ("diskon", 15),
        ("rating_up", 15),
        ("harga_naik", 10),
        ("kebakaran", 6),
        ("tikus", 1),
        ("denda", 3),
        ("rating_down", 1),
    ]

    total_prob = sum(e[1] for e in daftar_event)
    r = random.randint(1, total_prob)

    akumulasi = 0
    event_terpilih = None

    for e, p in daftar_event:
        akumulasi += p
        if r <= akumulasi:
            event_terpilih = e
            break

    print("\n=== EVENT HARI INI ===")

    if event_terpilih == "bonus":
        bonus = random.randint(5000, 25000)
        bonus = round_to_500(bonus)
        modal += bonus
        print(f"🎁 Bonus pelanggan tetap: +{fmt(bonus)}")

    elif event_terpilih == "diskon":
        item = random.choice(list(barang.keys()))
        pot = round_to_500(random.randint(500,1500))
        barang[item]["beli"] = max(500, round_to_500(barang[item]["beli"] - pot))
        print(f"📦 Supplier memberi diskon {item}: turun {fmt(pot)}")

    elif event_terpilih == "rating_up":
        rating = min(5.0, rating + 0.15)
        print(f"⭐ Rating naik: {rating:.2f}")

    elif event_terpilih == "harga_naik":
        item = random.choice([i for i,b in barang.items() if not b["terkunci"]])
        naik = round_to_500(random.randint(500,2000))
        barang[item]["jual"] = round_to_500(barang[item]["jual"] + naik)
        print(f"📈 Harga jual {item} naik {fmt(naik)}")

    elif event_terpilih == "kebakaran":
        item = random.choice(list(barang.keys()))
        hilang = random.randint(1,2)
        barang[item]["stok"] = max(0, barang[item]["stok"]-hilang)
        print(f"🔥 Kebakaran! Stok {item} -{hilang}")

    elif event_terpilih == "tikus":
        item = random.choice(["Indomie","Gula 1kg","Aqua"])
        hilang = random.randint(1,2)
        barang[item]["stok"] = max(0, barang[item]["stok"]-hilang)
        print(f"🐭 Tikus memakan stok {item}! -{hilang}")

    elif event_terpilih == "denda":
        denda = round_to_500(random.randint(3000,7000))
        modal -= denda
        print(f"💸 Denda lingkungan {fmt(denda)}")

    elif event_terpilih == "rating_down":
        rating = max(0, rating - 0.01)
        print("😡 Pelanggan komplain! Rating turun.")

    print("=" * 40)
    time.sleep(1)

# ==========================
# UBAH HARGA
# ==========================
def ubah_harga(tampilkan=True):
    if tampilkan:
        print("\n📢 Perubahan harga hari ini:")

    for nama, info in barang.items():
        if info.get("terkunci", False):
            continue

        beli_lama = info["beli"]
        jual_lama = info["jual"]

        info["beli"] = max(500, round_to_500(info["beli"] + random.randint(-800,1500)))
        info["jual"] = max(info["beli"]+300, round_to_500(info["jual"] + random.randint(-500,1500)))

        if tampilkan:
            pb = ((info['beli']-beli_lama)/beli_lama)*100
            pj = ((info['jual']-jual_lama)/jual_lama)*100
            print(f"- {nama}: Beli {fmt(info['beli'])} ({pb:+.1f}%), Jual {fmt(info['jual'])} ({pj:+.1f}%)")

# ==========================
# PELANGGAN
# ==========================
def jumlah_pelanggan_berdasarkan_rating(r):
    if r < 1: return 1
    if r < 2: return 2
    if r < 3: return random.randint(3,4)
    if r < 4: return random.randint(5,6)
    return random.randint(7,8)

def paket_terbuka(nama):
    return not barang[nama]["terkunci"]

def pelanggan_datang():
    global modal, rating

    jumlah = jumlah_pelanggan_berdasarkan_rating(rating)
    print(f"\nHari ini datang {jumlah} pelanggan\n")

    for _ in range(jumlah):
        item = random.choice([b for b in barang if paket_terbuka(b)])
        qty = random.randint(1,3)
        print(f"Pelanggan membeli {item} x{qty}")

        if barang[item]["stok"] < qty:
            print("❌ Stok habis! Rating turun.")
            rating -= 0.05
            input("ENTER...")
            continue

        total = round_to_500(barang[item]["jual"] * qty)
        print(f"Total belanja: {fmt(total)}")

        # Hitung uang pelanggan
        lembar_awal = random.choice([1,2,3])
        uang_list = [random.choice(pecahan_uang) for _ in range(lembar_awal)]
        uang_pelanggan = sum(uang_list)

        attempts = 0
        while uang_pelanggan < total and attempts < 6:
            uang_list.append(random.choice(pecahan_uang))
            uang_pelanggan = sum(uang_list)
            attempts += 1

        uang_pelanggan = round_to_500(max(500, uang_pelanggan))
        print(f"Uang pelanggan: {fmt(uang_pelanggan)} | Lembar: {uang_list}")

        if uang_pelanggan < total:
            print("❌ Uang kurang! Rating turun.")
            rating -= 0.08
            input("ENTER...")
            continue

        kembalian_seharusnya = uang_pelanggan - total

        try:
            inp = input("Masukkan kembalian: ").strip().replace(",","")
            user_kembalian = int(inp)
        except:
            print("❌ Input salah! Rating turun.")
            rating -= 0.1
            input("ENTER...")
            continue

        if user_kembalian % 500 != 0:
            print("❌ Kembalian harus kelipatan 500.")
            rating -= 0.15
            input("ENTER...")
            continue

        if user_kembalian != kembalian_seharusnya:
            print(f"❌ Harusnya {fmt(kembalian_seharusnya)}!")
            rating -= 0.15
            input("ENTER...")
            continue

        # SUKSES
        barang[item]["stok"] -= qty
        modal += total

        paket = barang[item]["paket"]
        bonus = round_to_500(int(total * bonus_paket[paket]))
        modal += bonus

        print(f"✔️ Sukses! Terjual {item} x{qty} → {fmt(total)}")
        if bonus > 0: print(f"Bonus Paket {paket}: +{fmt(bonus)}")
        print(f"Saldo: {fmt(modal)}")

        rating = min(5.0, rating + 0.10)
        print(f"Rating sekarang: {rating:.2f}")
        input("ENTER...")

        # ================================
        # RIWAYAT PEMBELIAN (BARU)
        # ================================
        riwayat.append({
            "hari": hari,
            "item": item,
            "qty": qty,
            "total": total,
            "bonus": bonus,
            "saldo": modal
        })

    rating = min(5.0, max(0, rating))

# ==========================
# RIWAYAT MENU (BARU)
# ==========================
def menu_riwayat():
    clear_screen()
    banner_warung()
    print("\n=== RIWAYAT PEMBELIAN ===\n")

    if not riwayat:
        print("Belum ada transaksi.")
        input("\nENTER...")
        loading("Menutup riwayat")
        return

    for i, r in enumerate(riwayat, start=1):
        print(f"{i}. Hari {r['hari']} | {r['item']} x{r['qty']} | Total: {fmt(r['total'])} | Bonus: {fmt(r['bonus'])} | Saldo: {fmt(r['saldo'])}")

    input("\nENTER...")
    loading("Menutup riwayat")

# ==========================
# PAJAK
# ==========================
def bayar_pajak():
    global modal
    modal -= pajak_harian
    print(f"💸 Pajak {fmt(pajak_harian)} | Saldo {fmt(modal)}")

# ==========================
# HARI
# ==========================
def pengaturan_hari():
    global auto_hari
    clear_screen()
    banner_warung()

    print("\n=== PENGATURAN HARI ===")
    print(f"Mode saat ini: {'Otomatis' if auto_hari else 'Manual'}")
    print("1. Otomatis")
    print("2. Manual")
    print("0. Kembali")

    pilih = input("Pilih: ")
    loading("Menyimpan")

    if pilih == "1":
        auto_hari = True
    elif pilih == "2":
        auto_hari = False

def lanjut_hari():
    global hari
    hari += 1
    event_random()
    ubah_harga(False)
    bayar_pajak()
    print(f"➡ Hari {hari}")
    loading("Menyiapkan hari...")

# ==========================
# BELI BARANG
# ==========================
def menu_beli_barang():
    global modal
    while True:
        clear_screen()
        banner_warung()

        print("\n=== BELI / BUKA PAKET ===")
        daftar = list(barang.keys())

        for i,nama in enumerate(daftar,1):
            info = barang[nama]
            status = "Terkunci" if info["terkunci"] else "Terbuka"
            h_buka = biaya_buka_paket[info["paket"]] if info["terkunci"] else 0
            print(f"{i}. {nama} | Beli {fmt(info['beli'])} | Jual {fmt(info['jual'])} | Stok {info['stok']} | {status} | Paket {info['paket']} | Buka: {fmt(h_buka)}")

        print("0. Kembali")
        pilih = input("Pilih: ")

        if pilih == "0": 
            loading("Kembali")
            break

        try:
            idx = int(pilih)-1
            nama_item = daftar[idx]
        except:
            continue

        info = barang[nama_item]

        if info["terkunci"]:
            biaya = biaya_buka_paket[info["paket"]]
            if modal < biaya:
                print("Uang kurang!")
                time.sleep(1)
                continue
            modal -= biaya
            info["terkunci"] = False
            print(f"🔓 {nama_item} terbuka!")
            loading("Membuka paket")

        try:
            qty = int(input(f"Jumlah {nama_item}: "))
        except:
            qty = 0

        if qty <= 0: continue

        total = round_to_500(info["beli"] * qty)
        if modal < total:
            print("Uang tidak cukup!")
            time.sleep(1)
            continue

        modal -= total
        info["stok"] += qty
        print(f"✔️ Berhasil beli {nama_item} x{qty} | Saldo {fmt(modal)}")
        loading("Memproses...")

# ==========================
# LIHAT BARANG
# ==========================
def menu_lihat_barang():
    clear_screen()
    banner_warung()
    print("\n=== DAFTAR BARANG ===\n")

    for nama,info in barang.items():
        status = "Terkunci" if info["terkunci"] else "Terbuka"
        h_buka = biaya_buka_paket[info["paket"]] if info["terkunci"] else 0
        print(f"{nama} | Stok {info['stok']} | Beli {fmt(info['beli'])} | Jual {fmt(info['jual'])} | {status} | Paket {info['paket']} | Buka: {fmt(h_buka)}")

    input("\nENTER...")
    loading("Menutup...")

# ==========================
# START SCREEN
# ==========================
def start_screen():
    clear_screen()
    banner_warung()

    print("\n📜 RULES PERMAINAN:")
    print("""
1. Kelola stok & modal.
2. Harga berubah tiap hari.
3. Rating bagus → pelanggan banyak.
4. Paket tinggi memberi bonus.
5. Event random bisa untung/rugi.
6. Pajak dibayar tiap hari.
""")

    input("ENTER untuk mulai...")
    loading("Memulai...")
    event_random()

# ==========================
# MAIN LOOP
# ==========================
def main_loop():
    global hari

    while True:
        clear_screen()
        banner_warung()

        print(f"Hari: {hari} | Modal: {fmt(modal)} | Rating: {rating:.2f}")
        print("============================================")
        print("1. Beli Barang / Buka Paket")
        print("2. Buka Warung (layani pelanggan)")
        print("3. Lihat Barang")
        print("4. Lihat Harga Naik/Turun (%)")
        print("5. Lihat Riwayat Pembelian")   # <=== MENU BARU

        if auto_hari:
            print("6. Pengaturan Hari")
        else:
            print("6. Lanjut Hari")
            print("7. Pengaturan Hari")

        print("0. Keluar")

        pilih = input("Pilih: ")

        if pilih == "1":
            loading("Membuka menu beli")
            menu_beli_barang()

        elif pilih == "2":
            loading("Membuka warung")
            pelanggan_datang()

        elif pilih == "3":
            loading("Menampilkan barang")
            menu_lihat_barang()

        elif pilih == "4":
            loading("Mengambil data...")
            ubah_harga(True)
            input("ENTER...")

        elif pilih == "5":
            loading("Membuka riwayat")
            menu_riwayat()

        elif pilih == "6" and auto_hari:
            pengaturan_hari()

        elif pilih == "6" and not auto_hari:
            lanjut_hari()

        elif pilih == "7" and not auto_hari:
            pengaturan_hari()

        elif pilih == "0":
            loading("Keluar...")
            break

        if auto_hari:
            lanjut_hari()

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    start_screen()
    main_loop()