import sqlite3 #import library dan untuk mengelola database sqlite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') #Menghubungkan atau membuat database SQLite
    cursor = conn.cursor() #membuat kursor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    conn.commit() #menyimpan perubahan
    conn.close() #Menutup koneksi database

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db') #menhubungkan database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa") #mengambil semua data
    rows = cursor.fetchall() # Menyimpan hasil query ke dalam variabel
    conn.close()# Menutup koneksi
    return rows# Mengembalikan data

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()# Menyimpan perubahan
    conn.close()

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:# Jika nilai Biologi paling tinggi tampilkan kedokteran
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris: # Jika nilai Fisika paling tinggi tampilkan teknik
        return "Teknik"
    elif inggris > biologi and inggris > fisika:# Jika nilai Inggris paling tinggi tampilkan bahasa
        return "Bahasa"
    else:
        return "Tidak Diketahui"# Jika nilai sama atau tidak bisa ditentukan

# Fungsi untuk menangani tombol submit
def submit():
    try:
        nama = nama_var.get() # Membaca input nama siswa
        biologi = int(biologi_var.get())# Membaca input nilai Biologi
        fisika = int(fisika_var.get())# Membaca input nilai Fisika
        inggris = int(inggris_var.get()) # Membaca input nilai Inggris

        if not nama:# Validasi jika nama kosong
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)# Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)# Menyimpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")# Tampilkan info sukses
        clear_inputs()# Mengosongkan input
        populate_table()# Memperbarui tabel dengan data terbaru
    except ValueError as e:# Menangani kesalahan jika input tidak valid
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani tombol update
def update():
    try:
        if not selected_record_id.get(): # Validasi jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())# Membaca ID data yang dipilih
        nama = nama_var.get()# Membaca input nama siswa
        biologi = int(biologi_var.get())# Membaca input nilai Biologi
        fisika = int(fisika_var.get())# Membaca input nilai Fisika
        inggris = int(inggris_var.get())# Membaca input nilai Inggris

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)# Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")# Mengosongkan input nama
    biologi_var.set("")# Mengosongkan input nilai Biologi
    fisika_var.set("")# Mengosongkan input nilai Fisika
    inggris_var.set("")# Mengosongkan input nilai Inggris
    selected_record_id.set("")# Mengosongkan input ID data

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children(): # Menghapus semua baris dalam tabel
        tree.delete(row)
    for row in fetch_data():# Menambahkan data dari database ke tabel
        tree.insert("", "end", values=row)

# Fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] # Mengambil baris yang dipilih
        selected_row = tree.item(selected_item)['values']# Mendapatkan nilai dari baris

        selected_record_id.set(selected_row[0]) # Mengisi ID
        nama_var.set(selected_row[1])# Mengisi nama siswa
        biologi_var.set(selected_row[2])# Mengisi nilai Biologi
        fisika_var.set(selected_row[3])# Mengisi nilai Fisika
        inggris_var.set(selected_row[4]) # Mengisi nilai Inggris
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")# Tampilkan pesan kesalahan jika tidak valid

# Inisialisasi database
create_database()# Membuat database dan tabel jika belum ada

# Membuat GUI dengan Tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")# Menentukan judul aplikasi
root.configure(bg="#e28743")

# Variabel tkinter
nama_var = StringVar()  # Variabel untuk input nama siswa
biologi_var = StringVar()  # Variabel untuk input nilai Biologi
fisika_var = StringVar()  # Variabel untuk input nilai Fisika
inggris_var = StringVar()  # Variabel untuk input nilai Inggris
selected_record_id = StringVar()  # Variabel untuk menyimpan ID data yang dipilih

# Elemen GUI untuk input data
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)  # Label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)  # Input nama siswa

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)  # Label untuk nilai Biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  # Input nilai Biologi

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)  # Label untuk nilai Fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)  # Input nilai Fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)  # Label untuk nilai Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)  # Input nilai Inggris

# Tombol untuk submit, update, dan delete
Button(root, text="Submit", command=submit).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, padx=10, pady=10)

# Treeview untuk menampilkan data dalam bentuk tabel
tree = ttk.Treeview(root, columns=("ID", "Nama", "Biologi", "Fisika", "Inggris", "Fakultas"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama")
tree.heading("Biologi", text="Biologi")
tree.heading("Fisika", text="Fisika")
tree.heading("Inggris", text="Inggris")
tree.heading("Fakultas", text="Fakultas")
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", fill_inputs_from_table)  # Event untuk mengisi input berdasarkan baris yang dipilih

populate_table()  # Memuat data dari database ke tabel

root.mainloop()  # Menjalankan loop utama GUI