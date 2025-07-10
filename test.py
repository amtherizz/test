from openai import OpenAI
import re,json
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
def extrak_berita(news):
    completion = client.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {
            "role": "user",
            "content": news
        },
        {
            "role":"system",
            "content":"""ambil inti dari isi berita ini tanpa merubah kalimat nya dan balas dalam bentuk json {'inti_berita':'','sumber_media':'','narasumber':'','reporter':'','sentiment':'sentiment keseluruhan berita','tanggal':'d/m/Y','halaman_lebih_dari_satu':true/false} jika ada yang tidak tersedia, null kan saja(kecuali sentimen'positif/netral/negatif')"""
        }
    ]
    )
    json_match = re.search(r"```(?:json)?(.*?)```", completion.choices[0].message.content, re.DOTALL).group(1).strip()
    print(json_match)
extrak_berita("""
Skip to content
Rabu, Juli 9, 2025
Terbaru:

    Wakili Gubernur Kepri, Hadiri Seminar Internasional Peringatan 865 Tahun Bintan
    Kapal Julung-Julung Tertabrak Tongkang di Santuyung, Seluruh Penumpang Dilaporkan Selamat
    Tim Terpadu Kota Batam Bongkar Bangunan Kos-kosan yang Jadi Sarang Narkoba di Kawasan Ruli Kampung Madani
    Waspadai Penipuan, Warga Diimbau Abaikan Permintaan Data Pribadi Melalui Telepon
    Dispar Kepri Latih 40 Barista Pemula Menjadi Profesional

www.kepriraya.com

    HOME
    KEPRI

        ANAMBAS
        BATAM
        BINTAN
        KARIMUN
        LINGGA
        NATUNA
        TANJUNGPINANG
    DAERAH
    HUKRIM
    POLITIK

BINTAN
BREAKING NEWS
DAERAH
Bintan Jadi Pilot Project Pemberdayaan Nelayan Pesisir dan Pulau Terluar BNPP RI
Mei 21, 2025
Zuki Haluan

Pemerintah Kabupaten Bintan bersama Badan Nasional Pengelola Perbatasan Republik Indonesia (BNPP RI) menggelar kegiatan Pemberdayaan Masyarakat Nelayan di Pesisir dan Pulau-Pulau Kecil Terluar (PPKT), Rabu (21/05) di Aula Bandar Seri Bentan. f-Diskominfo Bintan

BINTAN, (kepriraya.com)– Pemerintah Kabupaten Bintan bersama Badan Nasional Pengelola Perbatasan Republik Indonesia (BNPP RI) menggelar kegiatan Pemberdayaan Masyarakat Nelayan di Pesisir dan Pulau-Pulau Kecil Terluar (PPKT), Rabu (21/05) di Aula Bandar Seri Bentan. Kegiatan ini bertujuan meningkatkan kesejahteraan nelayan melalui edukasi, penguatan kapasitas dan pemahaman batas wilayah laut.

Sekretaris Daerah Kabupaten Bintan Ronny Kartika dalam sambutannya menyampaikan apresiasi atas terpilihnya Bintan sebagai pilot project. Ia menegaskan komitmen Pemerintah Daerah untuk mendukung penuh upaya pemberdayaan masyarakat nelayan yang berkelanjutan dan berbasis regulasi.

“Beberapa kasus menunjukkan bahwa sebagian nelayan Bintan karena keterbatasan informasi dan tekanan ekonomi terpaksa melaut hingga ke wilayah perairan negara tetangga. Hal ini perlu menjadi perhatian dan dukungan bersama dengan memperkuat sinergi antara Pemerintah Pusat dan Daerah, aparat penegak hukum, TNI dan instansi terkait khususnya dalam pengelolaan dan pengawasan batas wilayah negara baik laut maupun udara” paparnya.

Rangkaian kegiatan Kunker BNPP RI berlangsung selama tiga hari, meliputi koordinasi kunjungan kerja, edukasi di Desa Berakit bersama narasumber dari Badan Informasi Geospasial (BIG), Polairud dan Bakamla terkait batas laut dan pengawasan wilayah perairan, serta kunjungan ke Pulau Malang Berdaun dan Pulau Berakit yang termasuk dalam PPKT.

Melalui program tersebut juga diharapkan masyarakat nelayan di wilayah PPKT khususnya di Bintan, dapat memahami pentingnya batas wilayah laut sebagai bagian dari kedaulatan negara. Dengan edukasi dan pelatihan yang diberikan, para nelayan diharapkan mampu meningkatkan kapasitas dalam pengelolaan sumber daya laut, mematuhi regulasi yang berlaku serta menerapkan teknologi tangkap yang ramah lingkungan dan berkelanjutan.

Deputi Pengelolaan Batas Wilayah Negara BNPP RI Nurdin, dalam kesempatan tersebut menyampaikan apresiasi yang sebesar-besarnya kepada Pemerintah Kabupaten Bintan atas sinergi dan dukungan penuh terhadap pelaksanaan kegiatan Pemberdayaan Masyarakat Nelayan di Pesisir dan Pulau-Pulau Kecil Terluar (PPKT) ini. Kegiatan tersebut merupakan bagian dari komitmen BNPP RI dalam mendorong pembangunan wilayah perbatasan dan memperkuat ketahanan wilayah melalui pemberdayaan masyarakat yang tinggal di garis depan kedaulatan negara.

Ke depan ia berharap kegiatan tersebut tidak hanya menjadi agenda sesaat, tetapi menjadi awal dari kolaborasi yang lebih luas dan berkelanjutan antara Pemerintah Pusat dan Daerah dalam memperkuat posisi masyarakat perbatasan sebagai garda terdepan penjaga wilayah NKRI. (*)
Post Views: 200
0Shares

Cukai Batam Ungkap Tiga Penyelundupan Sabu dengan Berbagai Modus di Bandara Hang Nadim
TP-PKK Tanjungpinang Gelar Rapat Persiapan HKG PKK ke-53 Tahun 2025, Fokuskan Kegiatan Sosial dan Pelestarian Lingkungan
Anda Juga Mungkin Suka
Sukses, Pesantren Ramadhan 1444 H Tingkat SD dan SMP di Tanjungpinang Ditutup Melalui Khataman Al Qur’an 
April 4, 2023
Aspidsus Kejati Kepri Pimpin Upacara Hari Kebangkitan Nasional 2024
Mei 20, 2024
Bhabinkamtibmas Kelurahan Sungai Lumpur Kecamatan Singkep, Briptu Rian Ardian Sambangi Masyarakat
Januari 4, 2023
Tinggalkan Balasan

Alamat email Anda tidak akan dipublikasikan. Ruas yang wajib ditandai *

Komentar *

Nama *

Email *

Situs Web

Simpan nama, email, dan situs web saya pada peramban ini untuk komentar saya berikutnya.

HEADLINE
Waspadai Penipuan, Warga Diimbau Abaikan Permintaan Data Pribadi Melalui Telepon
BREAKING NEWS
HEADLINE
TANJUNGPINANG
Waspadai Penipuan, Warga Diimbau Abaikan Permintaan Data Pribadi Melalui Telepon
Juli 8, 2025
Zuki Haluan

Kepala Dinas Komunikasi dan Informatika Kota Tanjungpinang Teguh Susanto TANJUNGPINANG, (kepriraya.com)—Kepala Dinas Komunikasi dan Informatika Kota Tanjungpinang Teguh Susanto mengimbau,
PMII Desak Pemkab Bintan Prioritaskan Pendidikan di Kepulauan
PMII Desak Pemkab Bintan Prioritaskan Pendidikan di Kepulauan
Juli 3, 2025
Masyarakat Pasir Panjang Unjuk Rasa di PT Karimun Granite Minta Tuntutan Kosesi dan PPM
Masyarakat Pasir Panjang Unjuk Rasa di PT Karimun Granite Minta Tuntutan Kosesi dan PPM
April 16, 2025
BERITA TERBARU
Tim Terpadu Kota Batam Bongkar Bangunan Kos-kosan yang Jadi Sarang Narkoba di Kawasan Ruli Kampung Madani
BATAM
BREAKING NEWS
Uncategorized
Tim Terpadu Kota Batam Bongkar Bangunan Kos-kosan yang Jadi Sarang Narkoba di Kawasan Ruli Kampung Madani
Juli 8, 2025
Zuki Haluan

Rumah liar di kawasan Kampung Madani Sei Beduk dibongkar tim terpadu Kota Batam, Selasa (8/7/2025). Ist BATAM, (kepriraya.com)– Tim Terpadu
Waspadai Penipuan, Warga Diimbau Abaikan Permintaan Data Pribadi Melalui Telepon
Waspadai Penipuan, Warga Diimbau Abaikan Permintaan Data Pribadi Melalui Telepon
Juli 8, 2025
Dispar Kepri Latih 40 Barista Pemula Menjadi Profesional
Dispar Kepri Latih 40 Barista Pemula Menjadi Profesional
Juli 8, 2025
Wakili Gubernur Kepri, Hadiri Seminar Internasional Peringatan 865 Tahun Bintan
Wakili Gubernur Kepri, Hadiri Seminar Internasional Peringatan 865 Tahun Bintan
Juli 8, 2025
About Us
LAMAN

    Redaksi
    Pendoman Media Siber
    Perlindungan Wartawan
    Kode Etik Jurnalistik
    Disclaimer

Hak Cipta © 2025 www.kepriraya.com. Keseluruhan Hak Cipta.
Tema: ColorMag oleh ThemeGrill. Dipersembahkan oleh WordPress.
""")
