import streamlit as st
import json
import os
import pandas as pd

# File to store the library data
LIBRARY_FILE = "library.txt"

# Initialize session state for library
if 'library' not in st.session_state:
    st.session_state.library = []

def load_library():
    """Load the library from a file if it exists."""
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as file:
                st.session_state.library = json.load(file)
            st.success("Library loaded from file.")
        except json.JSONDecodeError:
            st.error("Error loading library file. Starting with an empty library.")
            st.session_state.library = []
    else:
        st.info("No library file found. Starting with an empty library.")

def save_library():
    """Save the library to a file."""
    try:
        with open(LIBRARY_FILE, 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
        st.success("Library saved to file.")
    except Exception as e:
        st.error(f"Error saving library: {e}")

def add_book():
    """Add a new book to the library."""
    st.subheader("Add a Book")
    with st.form(key="add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1, max_value=2025, step=1)
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read this book?", ["Yes", "No"])
        
        submit = st.form_submit_button("Add Book")
        
        if submit:
            if title.strip() and author.strip() and genre.strip():
                book = {
                    "title": title.strip(),
                    "author": author.strip(),
                    "year": int(year),
                    "genre": genre.strip(),
                    "read": read == "Yes"
                }
                st.session_state.library.append(book)
                st.success("Book added successfully!")
            else:
                st.error("Please fill in all fields.")

def remove_book():
    """Remove a book from the library by title."""
    st.subheader("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if title.strip():
            for book in st.session_state.library[:]:
                if book["title"].lower() == title.strip().lower():
                    st.session_state.library.remove(book)
                    st.success("Book removed successfully!")
                    return
            st.error("Book not found in the library.")
        else:
            st.error("Please enter a book title.")

def search_book():
    """Search for a book by title or author."""
    st.subheader("Search for a Book")
    search_by = st.selectbox("Search by", ["Title", "Author"])
    search_term = st.text_input(f"Enter the {search_by.lower()}")
    
    if st.button("Search"):
        if search_term.strip():
            if search_by == "Title":
                matches = [book for book in st.session_state.library if search_term.lower() in book["title"].lower()]
            else:  # Author
                matches = [book for book in st.session_state.library if search_term.lower() in book["author"].lower()]
            
            if matches:
                st.write("**Matching Books:**")
                df = pd.DataFrame(matches)
                df['read'] = df['read'].apply(lambda x: "Read" if x else "Unread")
                st.dataframe(df[["title", "author", "year", "genre", "read"]])
            else:
                st.warning("No matching books found.")
        else:
            st.error(f"Please enter a {search_by.lower()} to search.")

def display_all_books():
    """Display all books in the library."""
    st.subheader("All Books")
    if st.session_state.library:
        df = pd.DataFrame(st.session_state.library)
        df['read'] = df['read'].apply(lambda x: "Read" if x else "Unread")
        st.dataframe(df[["title", "author", "year", "genre", "read"]])
    else:
        st.warning("Your library is empty.")

def display_statistics():
    """Display library statistics."""
    st.subheader("Library Statistics")
    if st.session_state.library:
        total_books = len(st.session_state.library)
        read_books = sum(1 for book in st.session_state.library if book["read"])
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        st.write(f"**Total books:** {total_books}")
        st.write(f"**Percentage read:** {percentage_read:.1f}%")
    else:
        st.warning("Your library is empty.")

def main():
    """Main function to run the library manager."""
    st.title("📚 Personal Library Manager")
    st.markdown("Manage your book collection with ease!")

    # Load library at startup
    if not st.session_state.library:
        load_library()

    # Menu system using sidebar
    menu = st.sidebar.selectbox(
        "Menu",
        ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Save and Exit"]
    )

    if menu == "Add a Book":
        add_book()
    elif menu == "Remove a Book":
        remove_book()
    elif menu == "Search for a Book":
        search_book()
    elif menu == "Display All Books":
        display_all_books()
    elif menu == "Display Statistics":
        display_statistics()
    elif menu == "Save and Exit":
        save_library()
        st.info("Library saved. You can close the app.")
        st.stop()

if __name__ == "__main__":
    main()