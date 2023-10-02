import sqlite3


conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate DATE,
              FOREIGN KEY(BookID) REFERENCES Books(BookID),
              FOREIGN KEY(UserID) REFERENCES Users(UserID))''')

conn.commit()

def add_book():
    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")
    
    c.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
              (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully.")

def find_book_detail():
    book_id = input("Enter Book ID: ")
    c.execute("SELECT Books.*, Users.Name, Users.Email FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID WHERE Books.BookID = ?", (book_id,))
    book_detail = c.fetchone()
    if book_detail:
        print("Book detail:")
        print("BookID:", book_detail[0])
        print("Title:", book_detail[1])
        print("Author:", book_detail[2])
        print("ISBN:", book_detail[3])
        print("Status:", book_detail[4])
        if book_detail[6]:
            print("Reserved by:", book_detail[6])
            print("User Name:", book_detail[7])
            print("User Email:", book_detail[8])
    else:
        print("Book not found.")

def find_reservation_status():
    search_text = input("Enter BookID, Title, UserID, or ReservationID: ")
    
    if search_text.startswith('LB'):
        c.execute("SELECT * FROM Books WHERE BookID = ?", (search_text,))
        book = c.fetchone()
        if book is None:
            print("Book not found.")
            return
        c.execute("SELECT * FROM Reservations WHERE BookID = ?", (search_text,))
        reservation = c.fetchone()
        if reservation:
            print("Reservation status: Reserved")
            print("Reservation Date:", reservation[3])
            user_id = reservation[2]
            c.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
            user = c.fetchone()
            print("User Name:", user[1])
            print("User Email:", user[2])
        else:
            print("Reservation status: Not reserved")
            
    elif search_text.startswith('LU'):
        c.execute("SELECT * FROM Users WHERE UserID = ?", (search_text,))
        user = c.fetchone()
        if user is None:
            print("User not found.")
            return
        c.execute("SELECT * FROM Reservations WHERE UserID = ?", (search_text,))
        reservations = c.fetchall()
        if len(reservations) > 0:
            print("Reservation status: Reserved")
            for reservation in reservations:
                book_id = reservation[1]
                c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
                book = c.fetchone()
                print("Book Title:", book[1])
                print("Book Author:", book[2])
                print("Reservation Date:", reservation[3])
        else:
            print("Reservation status: Not reserved")
    
    elif search_text.startswith('LR'):
        c.execute("SELECT * FROM Reservations WHERE ReservationID = ?", (search_text,))
        reservation = c.fetchone()
        if reservation is None:
            print("Reservation not found.")
            return
        book_id = reservation[1]
        user_id = reservation[2]
        c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
        book = c.fetchone()
        c.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
        user = c.fetchone()
        print("Book Title:", book[1])
        print("Book Author:", book[2])
        print("Reservation Date:", reservation[3])
        print("User Name:", user[1])
        print("User Email:", user[2])
    
    else:
        c.execute("SELECT * FROM Books WHERE Title = ?", (search_text,))
        books = c.fetchall()
        if len(books) > 0:
            print("Books found:")
            for book in books:
                print("BookID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("ISBN:", book[3])
                print("Status:", book[4])
        else:
            print("Book not found.")
            

def find_all_books():
    c.execute("SELECT Books.*, Users.Name, Users.Email FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID")
    books = c.fetchall()
    if len(books) > 0:
        print("All books:")
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            if book[6]:
                print("Reserved by:", book[6])
                print("User Name:", book[7])
                print("User Email:", book[8])
            print("----------------------")
    else:
        print("No books found.")

def modify_book_details():
    book_id = input("Enter Book ID: ")
    
    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = c.fetchone()
    if book is None:
        print("Book not found.")
        return
    
    option = input("What details do you want to modify?\n1. Title\n2. Author\n3. ISBN\n4. Status\nChoose an option: ")
    
    if option not in {'1', '2', '3', '4'}:
        print("Invalid option.")
        return
    
    if option == '1':
        new_title = input("Enter new title: ")
        c.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (new_title, book_id))
    elif option == '2':
        new_author = input("Enter new author: ")
        c.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (new_author, book_id))
    elif option == '3':
        new_isbn = input("Enter new ISBN: ")
        c.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (new_isbn, book_id))
    elif option == '4':
        new_status = input("Enter new status: ")
        c.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
    
    c.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    reservation = c.fetchone()
    if reservation:
        reservation_id = reservation[0]
        c.execute("UPDATE Reservations SET BookID = ? WHERE ReservationID = ?", (book_id, reservation_id))
    
    conn.commit()
    print("Book details modified successfully.")

def delete_book():
    book_id = input("Enter Book ID: ")
    
    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = c.fetchone()
    if book is None:
        print("Book not found.")
        return
    
    c.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    reservation = c.fetchone()
    if reservation:
        reservation_id = reservation[0]
        c.execute("DELETE FROM Reservations WHERE ReservationID = ?", (reservation_id,))
    
    c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully.")

def exit_program():
    conn.close()
    print("Library management system closed.")
    exit(0)

while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all books")
    print("5. Modify/update book details")
    print("6. Delete a book")
    print("7. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        add_book()
    elif choice == '2':
        find_book_detail()
    elif choice == '3':
        find_reservation_status()
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        modify_book_details()
    elif choice == '6':
        delete_book()
    elif choice == '7':
        exit_program()
    else:
        print("Invalid choice. Please try again.")