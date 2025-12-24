import tkinter as tk
from tkinter import messagebox, ttk
from controller import *
from database import init_db
from config import *

def run_gui():
    init_db()

    root = tk.Tk()
    root.title("PROJEK UAS ALPRO")
    root.geometry("700x550")
    root.configure(bg=BG_MAIN)

    # ================= FUNGSI LOGIKA GUI =================
    def refresh_table():
        """Mengambil data terbaru dari database dan menampilkannya di tabel"""
        for item in table.get_children():
            table.delete(item)
        for book in get_books_controller():
            table.insert("", "end", values=book)

    def handle_add():
        """Mengambil input user dan mengirim ke controller"""
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()

        if add_book_controller(title, author, year):
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
            # Kosongkan form setelah input
            entry_title.delete(0, tk.END)
            entry_author.delete(0, tk.END)
            entry_year.delete(0, tk.END)
            refresh_table()
        else:
            messagebox.showwarning("Gagal", "Semua kolom harus diisi!")

    def handle_delete():
        """Menghapus buku yang dipilih di tabel"""
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin dihapus!")
            return
        
        # Ambil ID dari kolom pertama baris yang diklik
        book_id = table.item(selected_item)['values'][0]
        delete_book_controller(book_id)
        messagebox.showinfo("Sukses", "Buku berhasil dihapus")
        refresh_table()

    def handle_search():
        """Mencari buku berdasarkan keyword"""
        keyword = entry_search.get()
        results = search_books_controller(keyword)
        for item in table.get_children():
            table.delete(item)
        for book in results:
            table.insert("", "end", values=book)

    # ===== TITLE =====
    tk.Label(
        root,
        text="MINI PERPUSTAKAAN",
        font=("Segoe UI", 20, "bold"),
        bg=BG_MAIN,
        fg="white"
    ).pack(pady=10)

    # ================= FORM INPUT =================
    frame_form = tk.Frame(root, bg=BG_FORM, bd=2, relief="groove")
    frame_form.pack(padx=10, pady=10)

    tk.Label(frame_form, text="JUDUL BUKU :", bg=BG_FORM, fg=FG_TEXT, font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
    entry_title = tk.Entry(frame_form, width=30)
    entry_title.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="PENULIS :", bg=BG_FORM, fg=FG_TEXT, font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
    entry_author = tk.Entry(frame_form, width=30)
    entry_author.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="TAHUN TERBIT :", bg=BG_FORM, fg=FG_TEXT, font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
    entry_year = tk.Entry(frame_form, width=30)
    entry_year.grid(row=2, column=1, padx=5, pady=2)

    # ================= BUTTON UTAMA =================
    frame_btn = tk.Frame(root, bg=BG_MAIN)
    frame_btn.pack(pady=10)

    # Command sekarang mengarah ke fungsi handle
    tk.Button(frame_btn, text="Tambah Buku", command=handle_add, width=15).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Hapus Buku", command=handle_delete, width=15, bg="#ff4d4d", fg="white").grid(row=0, column=1, padx=5)

    # ================= SEARCH =================
    frame_search = tk.Frame(root, bg=BG_FORM, padx=10, pady=5)
    frame_search.pack(pady=5)

    tk.Label(frame_search, text="Cari Buku:", bg=BG_FORM).pack(side=tk.LEFT)
    entry_search = tk.Entry(frame_search, width=30)
    entry_search.pack(side=tk.LEFT, padx=5)

    tk.Button(frame_search, text="Cari", command=handle_search).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_search, text="Reset", command=refresh_table).pack(side=tk.LEFT, padx=2)

    # ================= TABLE =================
    columns = ("ID", "Judul", "Penulis", "Tahun")
    table = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100 if col == "ID" or col == "Tahun" else 200)

    table.pack(expand=True, fill="both", padx=10, pady=10)

    # Jalankan refresh table sekali saat start agar data muncul
    refresh_table()

    root.mainloop()