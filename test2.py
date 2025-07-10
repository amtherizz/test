import requests
import uuid
import json,re
# idsys = str(uuid.uuid4())
# idusr = str(uuid.uuid4())
system_prompt = """
        Anda adalah asisten yang ahli dalam mengekstraksi informasi penting dari berita. Tugas Anda adalah mengidentifikasi paragraf-paragraf inti, sumber media, narasumber (jika ada), reporter (jika ada), sentimen terhadap Badan Informasi Geospasial (BIG) beserta buktinya, tanggal publikasi, dan juga menyajikan teks berita lengkap yang sudah bersih dari elemen non-berita.

        **Instruksi Detail:**
        1.  **inti_berita**: Ekstrak paragraf-paragraf utama yang paling relevan dan padat informasi. Pastikan ini adalah ringkasan yang komprehensif dari isi berita. Jangan hanya mengambil paragraf pertama atau terakhir, tetapi cari esensi beritanya.
        2.  **sumber_media**: Identifikasi nama media yang memublikasikan berita ini.
        3.  **narasumber**: Cari nama-nama orang yang dikutip atau diwawancarai dalam berita. Jika tidak ada, biarkan kosong.
        4.  **reporter**: Cari nama penulis atau reporter berita. Jika tidak ada, biarkan kosong.
        5.  **sentiment**: Analisis sentimen berita **khususnya terkait Badan Informasi Geospasial (BIG)**. Berikan nilai 'positif', 'netral', atau 'negatif'.
        6.  **bukti_sentiment**: Ekstrak **satu atau beberapa kalimat langsung dari berita yang paling jelas menunjukkan atau mendukung sentimen yang Anda berikan untuk Badan Informasi Geospasial (BIG)**. Kalimat ini harus secara eksplisit menyebutkan atau merujuk pada BIG dan menunjukkan nuansa positif, negatif, atau netral terkait peran/keterlibatan BIG dalam berita. Jika sentimennya 'netral', pilih kalimat yang menggambarkan fakta atau peran objektif BIG tanpa konotasi kuat.
        7.  **tanggal**: Ekstrak tanggal publikasi berita dalam format 'd/m/Y' (misal: 10/07/2025). Jika tidak ada, biarkan kosong.
        8.  **halaman_lebih_dari_satu**: Tentukan apakah berita ini kemungkinan memiliki lebih dari satu halaman atau bagian yang dipisah (misalnya, "bersambung ke halaman 2" atau "lanjutkan membaca"). Berikan `true` jika ya, `false` jika tidak. Ini seringkali sulit untuk diinferensi dari teks tunggal, jadi instruksikan model untuk membuat asumsi terbaik.

        **Format Output (HARUS JSON):**
        ```json
        {
          "inti_berita": "...",
          "sumber_media": "...",
          "narasumber": null,
          "reporter": null,
          "sentiment": "positif/netral/negatif",
          "tanggal": "d/m/Y",
          "halaman_lebih_dari_satu": true/false,
          "bukti_sentiment":"..."
        }
        ```
        **Catatan Penting:**
        * Jika suatu kolom tidak ditemukan, set nilainya ke `null` (kecuali `sentiment`, yang harus selalu diisi dengan salah satu dari tiga nilai yang ditentukan).
        * Pastikan format tanggal sesuai.
        * Sentimen harus benar-benar berfokus pada BIG.
        """
#8.  **full_berita**: Berikan kembali keseluruhan teks berita **yang sudah bersih dari segala macam menu navigasi, iklan, footer, header, daftar postingan terkait, komentar, atau elemen-elemen lain yang bukan bagian inti dari artikel berita**. Pastikan hanya teks naratif utama berita yang tersisa, termasuk judul dan sub-judul jika relevan, tetapi tanpa sisa-sisa HTML atau string yang tidak relevan (seperti 'Likes', 'Followers', 'Trending', dll. yang sering muncul dari `BeautifulSoup.text`). Ini harus merupakan teks berita lengkap yang ringkas dan mudah dibaca.
# idsys,idusr = "d81d6fdb-f80c-40fc-9da9-feedc160c0df","85265ea2-fb6d-427c-b61a-ebdf0444f339"
idusr,idsys = str(uuid.uuid4()),str(uuid.uuid4())
print(idusr,idsys)
def ekstrak_berita(news: str) -> str:
    headers = {
        'User-Agent': 'Ktor client',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Charset': 'UTF-8',
    }

    files = {
        'data': (None, json.dumps({
            "id": str(uuid.uuid4()),
            "model": "vgpt-g2-4",
            "messages": [
                {
                    "content": system_prompt,
                    "id": idsys,
                    "role": "system",
                    "model": "vgpt-g2-4"
                },
                {
                    "content": news,
                    "id": idusr,
                    "role": "user",
                    "model": "vgpt-g2-4"
                }
            ]
        })),
    }

    response = requests.post(
        'https://streaming.vyro.ai/v1/chatly/android/chat/completions',
        headers=headers,
        files=files,
        stream=True
    )

    output = ""
    # print(response.content)
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue

        if line.startswith("event: done"):
            break

        if line.startswith("data: "):
            try:
                data_json = json.loads(line[6:])
                content = data_json.get("content", "")
                # print(content)
                output += content
            except json.JSONDecodeError as e:
                print("Gagal parse JSON:", line)
    json_match = re.search(r"```(?:json)?(.*?)```", output, re.DOTALL).group(1).strip()
    return json.loads(json_match)
print(
    ekstrak_berita("""
Langsung ke konten
Breaking News
Digeruduk Warga Soal Limbah, PT AJP Janjikan Kompensasi dan Perbaikan Mesin Wakil Bupati Sambut Jamaah Haji Tapsel Kloter 20 di Medan Hendak Seludupkan Sabu Cair, WNI dan WN Malaysia Ditangkap Ketahuan Hendak Edarkan Sabu, Pasutri Nekat Serang Petugas Pakai Senpi Rakitan Eks Sekretaris Pribadi Nadiem Diperiksa Kasus Korupsi Chromebook
Home
Redaksi
Radarindo

    HOME
    SUMUT
    ACEH
    MEDAN
    KABUPATEN
    KOTA
    NUSANTARA
    HEADLINE
    EDITORIAL
    Ekonomi
    OPINI
    BUMN

    INTERNASIONAL
    SPORT
    HUKUM
    KRIMINAL
    JAWA
    POLITIK
    RAGAM
    KESEHATAN
    PERISTIWA
    PENDIDIKAN
    SOSOK

Beranda NUSANTARA
NUSANTARA  
Polemik Pulau Mangkir Gadang, Angga Munandar: “Ini Bukan Sekadar Titik Koordinat”
Redaksi Radarindo
Sabtu, 7 Juni 2025
58 views

RADARINDO.co.id – Medan : Polemik mengenai status Pulau Mangkir Gadang, sebuah pulau kecil yang berada di sekitar perairan Aceh Singkil, namun tercatat dalam administrasi Kabupaten Tapanuli Tengah (Tapteng), Sumatera Utara, terus menjadi perbincangan.

Baca juga: Usai Didemo Terkait Dugaan Pungli, Kepala SMAN 9 Tambun Selatan Dinonaktifkan

Sorotan bukan hanya datang dari masyarakat lokal, tetapi juga dari kalangan profesional hukum, salah satunya Angga Munandar SH, seorang advokat muda kelahiran Sigli, Aceh.

Dalam pernyataan tertulisnya, yang diterima, Sabtu (07/6/2025), Angga menekankan bahwa isu ini perlu dipandang lebih dari sekadar aspek teknis batas wilayah.

“Pulau Mangkir Gadang bukan sekadar titik koordinat dalam peta, tapi bagian dari kehidupan masyarakat Aceh, terutama mereka yang hidup di pesisir Singkil,” ujar Angga.

Menurutnya, dalam konteks hukum tata wilayah dan otonomi daerah, kejelasan batas administratif memang penting. Namun lanjutnya, yang lebih penting adalah memastikan bahwa proses penetapan batas tersebut dilakukan secara partisipatif dan adil, dengan mempertimbangkan faktor sejarah, sosial-budaya, serta pemanfaatan wilayah oleh masyarakat lokal.

“Aceh memiliki kekhususan dalam tata kelola pemerintahan melalui UU No. 11 Tahun 2006. Ketika muncul data spasial yang tidak sejalan dengan kenyataan sosial masyarakat, sudah semestinya ada ruang untuk mengajukan keberatan dan peninjauan ulang secara hukum,” jelasnya.

Angga menyampaikan bahwa pemerintah daerah, dalam hal ini Pemerintah Aceh maupun DPR Aceh, memiliki kewenangan untuk menyampaikan keberatan administratif kepada pemerintah pusat dan meminta kajian ulang atas peta wilayah yang dikeluarkan Badan Informasi Geospasial (BIG).

“Saya percaya penyelesaian terbaik adalah dengan membangun ruang dialog antara Aceh, Sumatera Utara, dan pemerintah pusat. Bukan untuk mencari siapa salah, tapi untuk mencari keadilan dan kepastian hukum yang berpihak pada masyarakat,” tambahnya.

Baca juga: Sebagai Efek Jera, Anggota Genk Motor Perusak Rumah Dikenakan Pasal Pidana

Menutup pernyataannya, Angga mengajak masyarakat untuk tetap tenang namun tidak pasif dalam menyikapi isu ini.

“Sebagai putra kelahiran Aceh, saya hanya ingin memastikan bahwa suara masyarakat kita tidak diabaikan. Ini bukan soal ambisi wilayah, tapi tentang keadilan, tentang pengakuan atas sejarah, dan tentang menjaga marwah daerah,” tutupnya. (KRO/RD/Is M)
Aceh Angga Munandar Bukan Sekadar Mangkir Gadang Sumut Titik Koordinat

Baca Juga
Eks Sekretaris Pribadi Nadiem Diperiksa Kasus Korupsi Chromebook
KPK Sita Uang Rp10 Miliar Terkait Kasus Pengadaan EDC BRI
Jadi Tersangka Dugaan Obat Racikan Berbahaya, Anak Bos Apotek Gama Grup Layangkan Gugatan
Dalami Kasus Kuota Haji 2024, KPK Periksa Sejumlah Saksi
KPK Panggil 7 Saksi Terkait Kasus Pembangunan Gedung Pemkab Lamongan
Wakil Walikota Tanjungbalai Hadiri Munas I Aswakada di Yogyakarta

Aceh

    KPA Tamiang Tegaskan Tak Terlibat “Aksi Aceh Melawan”	
    Selasa, 8 Juli 2025
    KPA Tamiang Tegaskan Tak Terlibat “Aksi Aceh Melawan”
    Menhan dan Panglima TNI Diminta Kaji Ulang Soal Penambahan Batalyon di Aceh	
    Selasa, 8 Juli 2025
    Menhan dan Panglima TNI Diminta Kaji Ulang Soal Penambahan Batalyon di Aceh
    Uang Zakat ASN di Bener Meriah “Ditilep” untuk Kepentingan Pribadi	
    Jumat, 4 Juli 2025
    Uang Zakat ASN di Bener Meriah “Ditilep” untuk Kepentingan Pribadi
    Belasan Pejabat BUMN Diperiksa Kasus Korupsi KEK Arun Lhokseumawe	
    Selasa, 1 Juli 2025
    Belasan Pejabat BUMN Diperiksa Kasus Korupsi KEK Arun Lhokseumawe
    Kejari Periksa Adik Irwandi Yusuf Terkait Dugaan Korupsi KEK Arun	
    Sabtu, 28 Juni 2025
    Kejari Periksa Adik Irwandi Yusuf Terkait Dugaan Korupsi KEK Arun

Selengkapnya
NUSANTARA

    Eks Sekretaris Pribadi Nadiem Diperiksa Kasus Korupsi Chromebook	
    Rabu, 9 Juli 2025
    Eks Sekretaris Pribadi Nadiem Diperiksa Kasus Korupsi Chromebook
    KPK Sita Uang Rp10 Miliar Terkait Kasus Pengadaan EDC BRI	
    Rabu, 9 Juli 2025
    KPK Sita Uang Rp10 Miliar Terkait Kasus Pengadaan EDC BRI
    Jadi Tersangka Dugaan Obat Racikan Berbahaya, Anak Bos Apotek Gama Grup Layangkan Gugatan	
    Selasa, 8 Juli 2025
    Jadi Tersangka Dugaan Obat Racikan Berbahaya, Anak Bos Apotek Gama Grup Layangkan Gugatan
    Dalami Kasus Kuota Haji 2024, KPK Periksa Sejumlah Saksi	
    Selasa, 8 Juli 2025
    Dalami Kasus Kuota Haji 2024, KPK Periksa Sejumlah Saksi
    KPK Panggil 7 Saksi Terkait Kasus Pembangunan Gedung Pemkab Lamongan	
    Selasa, 8 Juli 2025
    KPK Panggil 7 Saksi Terkait Kasus Pembangunan Gedung Pemkab Lamongan

Selengkapnya
HUKUM

    Tiga ASN DPRD Bengkulu Ditahan Kasus Korupsi Rp150 Miliar	
    Rabu, 9 Juli 2025
    Tiga ASN DPRD Bengkulu Ditahan Kasus Korupsi Rp150 Miliar
    Kejati Riau Tetapkan Tiga Tersangka Kasus Proyek Pelabuhan Sagu-sagu Lukit	
    Rabu, 9 Juli 2025
    Kejati Riau Tetapkan Tiga Tersangka Kasus Proyek Pelabuhan Sagu-sagu Lukit
    Peras Korban Investasi Bodong, Jaksa Divonis 7 Tahun Penjara	
    Selasa, 8 Juli 2025
    Peras Korban Investasi Bodong, Jaksa Divonis 7 Tahun Penjara
    Tuntutan 7 Tahun Tom Lembong Dinilai Terlalu Berat	
    Selasa, 8 Juli 2025
    Tuntutan 7 Tahun Tom Lembong Dinilai Terlalu Berat
    Direktur PT BCM Terancam 15 Tahun Penjara Akibat Jual Kayu Ilegal	
    Senin, 7 Juli 2025
    Direktur PT BCM Terancam 15 Tahun Penjara Akibat Jual Kayu Ilegal

Selengkapnya
Radarindo

    TUPOKSI REDAKSITentang KamiRedaksiDisclaimerPedoman Media SiberPrivacy PolicyIndeks Berita

© Radarindo.co.id | All Rights Reserved
Radarindo

    Laman
        Tentang Kami
        TUPOKSI REDAKSI
        Redaksi
        Pedoman Media Siber
        Disclaimer
        Privacy Policy
        Indeks Berita
    Kategori
    SUMUT
    ACEH
        Aceh Barat
        Aceh Selatan
        Aceh Singkil
        Aceh Tamiang
        Aceh Tengah
        Aceh Tenggara
        Aceh Timur
        Aceh Utara
        Banda Aceh
        Langsa
        Lhokseumawe
        Simeulue
    MEDAN
    KABUPATEN
        Asahan
        Batu Bara
        Dairi
        Deli Serdang
        Humbang Hasundutan
        Labuhan Batu
        Labuhan Batu Selatan
        Labuhan Batu Utara
        Langkat
        Mandailing Natal
        NIAS
        Nias Barat
        Nias Selatan
        Nias Utara
        Padang Lawas
        Padanglawas Utara
        Pakpak Bharat
        Samosir
        Serdang Bedagai
        Sibolga
        Simalungun
        Tanah Karo
        Tapanuli Selatan
        Tapanuli Tengah
        Tapanuli Utara
        Toba
    KOTA
        Binjai
        Gunungsitoli
        Padangsidimpuan
        Pematangsiantar
        Sibolga
        Tanjung Balai
        Tebing Tinggi
    NUSANTARA
        Batam
        Bengkulu
        Inhil/Rokan Hulu
        Jambi
        Kampar
        Kepri
        Lampung
        MAKASAR
        Maluku
        Padang
        Palembang
        Pekan Baru
        Pesawaran
        Riau
        Tanggamus
    HEADLINE
    EDITORIAL
    EKONOMI
    BUMN
    INTERNASIONAL
    RADARSport
    HUKUM
    KRIMINAL
    JAWA
    Opini
    Politik
    Ragam
    Kesehatan
    Peristiwa
    Pendidikan
    Sosok""")

)