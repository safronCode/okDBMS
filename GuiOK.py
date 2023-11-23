import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import *
class OKDataViewer:

    def __init__(self, root):
        self.root = root
        self.root.title("Одноклассники: База данных")
        self.root.geometry("1350x1200")
        self.root.config(bg="snow3")
        self.root.resizable(0,0)

        self.show_data = tk.BooleanVar(value=True)
        self.min_likes = tk.StringVar(value='0')
        self.min_comments = tk.StringVar(value='0')
        self.sort_column = None  # Инициализация столбца для сортировки
        self.sort_descending = False  # Инициализация направления сортировки

        self.load_groups()
        self.load_users()
        self.load_posts()
        self.load_comments()
        self.load_media()

        self.create_gui()
    def load_groups(self):
        self.conn = sqlite3.connect('okDBSM1.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM groups')
        self.data_groups = cursor.fetchall()
        self.conn.close()

    def load_users(self):
        self.conn = sqlite3.connect('okDBSM1.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        self.data_users = cursor.fetchall()
        self.conn.close()

    def load_posts(self):
        self.conn = sqlite3.connect('okDBSM1.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM posts')
        self.data_posts = cursor.fetchall()
        self.conn.close()

    def load_comments(self):
        self.conn = sqlite3.connect('okDBSM1.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM comments')
        self.data_comments = cursor.fetchall()
        self.conn.close()

    def load_media(self):
        self.conn = sqlite3.connect('okDBSM1.db')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM media')
        self.data_media = cursor.fetchall()
        self.conn.close()

    def update_data(self):
        print("Запрос ",self.entry.get()," выполнен")
        self.conn = sqlite3.connect('okDBSM1.db')
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.entry.get())
        except Exception as e:
            print(e.__repr__())
        else:
            self.entry.delete(0, 'end')
            self.data = cursor.fetchall()
            self.conn.close()
            self.create_gui()

            if self.show_data:
                tree = self.AnswerTree
                tree.delete(*tree.get_children())
                for row_data in self.data:
                    values = row_data
                    tree.insert("", "end", values=values)

    def toggle_data(self):
         self.show_data = not self.show_data
         self.load_groups()
         self.load_users()
         self.load_posts()
         self.load_comments()
         self.load_media()
         self.create_gui()

    def sort_groups(self, column):
        self.load_groups()
        self.data_groups.sort(key=lambda row: row[column], reverse=self.sort_descending)
        self.sort_column = column
        self.sort_descending = not self.sort_descending
        self.create_gui()

    def sort_users(self, column):
        self.load_users()
        self.data_users.sort(key=lambda row: row[column], reverse=self.sort_descending)
        self.sort_column = column
        self.sort_descending = not self.sort_descending
        self.create_gui()

    def sort_comments(self, column):
        self.load_comments()
        self.data_comments.sort(key=lambda row: row[column], reverse=self.sort_descending)
        self.sort_column = column
        self.sort_descending = not self.sort_descending
        self.create_gui()

    def sort_media(self, column):
        self.load_media()
        self.data_media.sort(key=lambda row: row[column], reverse=self.sort_descending)
        self.sort_column = column
        self.sort_descending = not self.sort_descending
        self.create_gui()

    def sort_posts(self, column):
        self.load_posts()
        self.data_posts.sort(key=lambda row: row[column], reverse=self.sort_descending)
        self.sort_column = column
        self.sort_descending = not self.sort_descending
        self.create_gui()


    def create_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        toggle_button = tk.Button(self.root, text="Dominic`s Button" if self.show_data else "Show Data", command=self.toggle_data,width=16,height=6, bg ="Grey", fg = "White")
        toggle_button.place(x=0, y=0)

        self.entry = tk.Entry(foreground='black', justify='left', width=135)
        self.entry.place(x=500, y=20)
        btn = tk.Button(text='Execute!', command=self.update_data, width=115, height=2, bg="Grey", fg="White")
        btn.place(x=500, y=40)

        groupsLabel = tk.Label(text = "Снизу таблица gruops")


        postsLabel = tk.Label(text="Снизу таблица posts")


        mediaLabel = tk.Label(text="Снизу таблица media")


        commentsLabel = tk.Label(text="Снизу таблица comments")


        usersLabel = tk.Label(text="Снизу таблица users")


        instructionLabel = tk.Label(text="Введите SQL запрос и нажмите на EXECUTE\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t")
        instructionLabel.pack()
        instructionLabel.place(x=500, y=0)

        if self.show_data:
            self.groupsTree = ttk.Treeview(self.root, columns=("id", "link", "name"), show="headings")
            self.groupsTree.heading("id", text="id",command=lambda: self.sort_data(0))
            self.groupsTree.column("id", width=50)
            self.groupsTree.heading("link", text="link", command=lambda: self.sort_data(1))
            self.groupsTree.column("link", width=175)
            self.groupsTree.heading("name", text="name", command=lambda: self.sort_data(2))
            self.groupsTree.column("name", width=185)
            self.groupsTree.place(x=0,y=90)
            groupsLabel.place(x=0,y=70)
            for row_data in self.data_groups:
                self.groupsTree.insert("", "end", values=row_data)

            self.usersTree = ttk.Treeview(self.root, columns=("id", "link", "name"), show="headings")
            self.usersTree.heading("id", text="id",command=lambda: self.sort_users(0))
            self.usersTree.column("id", width=50)
            self.usersTree.heading("link", text="link",command=lambda: self.sort_users(1))
            self.usersTree.heading("name", text="name",command=lambda: self.sort_users(2))
            self.usersTree.place(x=900, y=580)
            usersLabel.place(x=900,y=560)
            for row_data in self.data_users:
                self.usersTree.insert("","end",values=row_data)

            self.postsTree = ttk.Treeview(self.root, columns=("id", "link", "date", "text", "cnt_comments", "cnt_likes", "id_group"), show="headings")
            self.postsTree.heading("id", text="id", command=lambda: self.sort_posts(0))
            self.postsTree.column("id", width=50)
            self.postsTree.heading("link", text="link", command=lambda: self.sort_posts(1))
            self.postsTree.column("link", width=250)
            self.postsTree.heading("date", text="date", command=lambda: self.sort_posts(2))
            self.postsTree.column("date", width=130)
            self.postsTree.heading("text", text="text", command=lambda: self.sort_posts(3))
            self.postsTree.column("text", width=200)
            self.postsTree.heading("cnt_comments", text="cnt_comments", command=lambda: self.sort_posts(4))
            self.postsTree.column("cnt_comments", width=100)
            self.postsTree.heading("cnt_likes", text="cnt_likes", command=lambda: self.sort_posts(5))
            self.postsTree.column("cnt_likes", width=70)
            self.postsTree.heading("id_group", text="id_group", command=lambda: self.sort_posts(6))
            self.postsTree.column("id_group", width=70)
            self.postsTree.place(x=0, y=580)
            postsLabel.place(x=0,y=560)

            for row_data in self.data_posts:
                self.postsTree.insert("", "end", values=row_data)

            self.commentsTree = ttk.Treeview(self.root,columns=("id", "date", "text", "id_post", "id_group"),show="headings")
            self.commentsTree.heading("id", text="id", command=lambda: self.sort_comments(0))
            self.commentsTree.column("id", width=50)
            self.commentsTree.heading("date", text="date", command=lambda: self.sort_comments(1))
            self.commentsTree.column("date", width=250)
            self.commentsTree.heading("text", text="text", command=lambda: self.sort_comments(2))
            self.commentsTree.column("text", width=130)
            self.commentsTree.heading("id_post", text="id_post", command=lambda: self.sort_comments(3))
            self.commentsTree.column("id_post", width=200)
            self.commentsTree.heading("id_group", text="id_group", command=lambda: self.sort_comments(4))
            self.commentsTree.column("id_group", width=70)
            self.commentsTree.place(x=650, y=330)
            commentsLabel.place(x=650,y=310)

            for row_data in self.data_comments:
                self.commentsTree.insert("", "end", values=row_data)

            self.mediaTree = ttk.Treeview(self.root, columns=("id", "file_link", "file_type","id_post"), show="headings")
            self.mediaTree.heading("id", text="id", command=lambda: self.sort_media(0))
            self.mediaTree.column("id", width=50)
            self.mediaTree.heading("file_link", text="file_link", command=lambda: self.sort_media(1))
            self.mediaTree.column("file_link", width=400)
            self.mediaTree.heading("file_type", text="file_type", command=lambda: self.sort_media(2))
            self.mediaTree.column("file_type", width=80)
            self.mediaTree.heading("id_post", text="id_post", command=lambda: self.sort_media(3))
            self.mediaTree.column("id_post", width=70)
            self.mediaTree.place(x=0, y=330)
            mediaLabel.place(x=0, y=310)

            for row_data in self.data_media:
                self.mediaTree.insert("", "end", values=row_data)

            self.AnswerTree = ttk.Treeview(self.root, columns=("Result"),show="headings")
            self.AnswerTree.heading("Result", text="Result")
            self.AnswerTree.column("Result", width=815)
            self.AnswerTree.place(x=500,y=80)
        else:
            # SecretPicture
            our_image = PhotoImage(file="dominicTorreto.png")
            our_image = our_image.subsample(1, 1)
            our_label = Label(root)
            our_label.image = our_image
            our_label['image'] = our_label.image
            our_label.place(x=70, y=100)


if __name__ == '__main__':
    root = tk.Tk()
    app = OKDataViewer(root)
    root.mainloop()
