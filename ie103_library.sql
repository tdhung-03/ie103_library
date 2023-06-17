-- Database: ie103_library

-- DROP DATABASE IF EXISTS ie103_library;

CREATE DATABASE ie103_library
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	
-- Create the Author table
CREATE TABLE Author (
  author_id SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

-- Create the Category table
CREATE TABLE Category (
  category_id SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

-- Create the Member table
CREATE TABLE Member (
  member_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  phone_number VARCHAR(100),
  address VARCHAR(200)
);

-- Create the Book table
CREATE TABLE Book (
  book_id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  publication_date DATE,
  amount INTEGER
);

-- Create the Loan table
CREATE TABLE Loan (
  loan_id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES Book(book_id),
  member_id INTEGER REFERENCES Member(member_id),
  loan_date DATE,
  due_date DATE,
  return_date DATE NULL
);

-- Create the Reservation table
CREATE TABLE Reservation (
  reservation_id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES Book(book_id),
  member_id INTEGER REFERENCES Member(member_id),
  reservation_date DATE
);

-- Create the Author_Book table for the many-to-many relationship between Author and Book
CREATE TABLE Author_Book (
  author_book_id SERIAL PRIMARY KEY,
  author_id INTEGER REFERENCES Author(author_id),
  book_id INTEGER REFERENCES Book(book_id)
);

-- Create the Book_Category table for the many-to-many relationship between Book and Category
CREATE TABLE Book_Category (
  book_category_id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES Book(book_id),
  category_id INTEGER REFERENCES Category(category_id)
);

-- Create the Review table
CREATE TABLE Review (
  review_id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES Book(book_id),
  member_id INTEGER REFERENCES Member(member_id),
  comment TEXT,
  review_date DATE
);

-- Create the Favorite table
CREATE TABLE Favorite (
  favorite_id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES Book(book_id),
  member_id INTEGER REFERENCES Member(member_id)
);

-- Triggers
-- 1. Trigger to update the amount of available books when a loan is added or returned.
CREATE OR REPLACE FUNCTION update_book_amount()
  RETURNS TRIGGER AS
$$
BEGIN
  IF TG_OP = 'INSERT' THEN
    -- Decrease the amount of available books when a loan is added
    UPDATE Book
    SET amount = amount - 1
    WHERE book_id = NEW.book_id;
  ELSIF TG_OP = 'UPDATE' THEN
    -- Increase the amount of available books when a loan is returned
    UPDATE Book
    SET amount = amount + 1
    WHERE book_id = OLD.book_id;
  END IF;
  
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER loan_trigger
AFTER INSERT OR UPDATE ON Loan
FOR EACH ROW
EXECUTE FUNCTION update_book_amount();

-- 2. Trigger to enforce a constraint on the maximum number of loans per member.
CREATE OR REPLACE FUNCTION check_loan_count()
  RETURNS TRIGGER AS
$$
DECLARE
  max_loans INTEGER := 5; -- Maximum number of loans per member
  current_loans INTEGER;
BEGIN
  SELECT COUNT(*) INTO current_loans
  FROM Loan
  WHERE member_id = NEW.member_id
    AND return_date IS NULL; -- Only count loans that are not returned
  
  IF current_loans >= max_loans THEN
    RAISE EXCEPTION 'Maximum loan count exceeded for the member.';
  END IF;
  
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER loan_count_check_trigger
BEFORE INSERT ON Loan
FOR EACH ROW
EXECUTE FUNCTION check_loan_count();

-- 3. Trigger to automatically update the due date when a loan is created.
CREATE OR REPLACE FUNCTION set_due_date()
  RETURNS TRIGGER AS
$$
DECLARE
  loan_duration INTEGER := 14; -- Loan duration in days
BEGIN
  NEW.due_date := NEW.loan_date + loan_duration;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER due_date_update_trigger
BEFORE INSERT ON Loan
FOR EACH ROW
EXECUTE FUNCTION set_due_date();

-- 4. Trigger to check the availability of a book before creating a loan
CREATE OR REPLACE FUNCTION check_book_availability()
  RETURNS TRIGGER AS
$$
BEGIN
  IF (SELECT amount FROM Book WHERE book_id = NEW.book_id) <= 2 THEN
    RAISE EXCEPTION 'The requested book is not available.';
  END IF;

  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER book_availability_trigger
BEFORE INSERT ON Loan
FOR EACH ROW
EXECUTE FUNCTION check_book_availability();

-- Procedures
-- 1. Procedure to create a loan
CREATE OR REPLACE PROCEDURE create_loan(
  in_book_id INTEGER,
  in_member_id INTEGER,
  in_loan_date DATE,
  out_loan_id OUT INTEGER
)
AS $$
BEGIN
  INSERT INTO Loan (book_id, member_id, loan_date, due_date)
  VALUES (in_book_id, in_member_id, in_loan_date, in_loan_date + INTERVAL '14 days')
  RETURNING loan_id INTO out_loan_id;
END;
$$
LANGUAGE plpgsql;

-- 2. Procedure to handle the return of a book
CREATE OR REPLACE PROCEDURE handle_return(
  in_loan_id INTEGER
)
AS $$
BEGIN
  -- Update the return_date in the Loan table
  UPDATE Loan
  SET return_date = CURRENT_DATE
  WHERE loan_id = in_loan_id;
  
  -- Output a success message
  RAISE NOTICE 'Book returned successfully.';
END;
$$
LANGUAGE plpgsql;

-- 3. Procedure to create a reservation
CREATE OR REPLACE PROCEDURE create_reservation(
  in_book_id INTEGER,
  in_member_id INTEGER,
  in_reservation_date DATE,
  out_reservation_id OUT INTEGER
)
AS $$
BEGIN
  INSERT INTO Reservation (book_id, member_id, reservation_date)
  VALUES (in_book_id, in_member_id, in_reservation_date)
  RETURNING reservation_id INTO out_reservation_id;
END;
$$
LANGUAGE plpgsql;

-- 4. Procedure to add a review
CREATE OR REPLACE PROCEDURE add_review(
  in_book_id INTEGER,
  in_member_id INTEGER,
  in_comment TEXT,
  in_review_date DATE,
  out_review_id OUT INTEGER
)
AS $$
BEGIN
  INSERT INTO Review (book_id, member_id, comment, review_date)
  VALUES (in_book_id, in_member_id, in_comment, in_review_date)
  RETURNING review_id INTO out_review_id;
END;
$$
LANGUAGE plpgsql;

-- 5. Procedure to add a book to favorites
CREATE OR REPLACE PROCEDURE add_to_favorites(
  in_book_id INTEGER,
  in_member_id INTEGER,
  out_favorite_id OUT INTEGER
)
AS $$
BEGIN
  INSERT INTO Favorite (book_id, member_id)
  VALUES (in_book_id, in_member_id)
  RETURNING favorite_id INTO out_favorite_id;
END;
$$
LANGUAGE plpgsql;

INSERT INTO Author (name) VALUES ('John Smith');
INSERT INTO Author (name) VALUES ('Jane Doe');
INSERT INTO Author (name) VALUES ('Michael Johnson');

INSERT INTO Category (name) VALUES ('Fiction');
INSERT INTO Category (name) VALUES ('Mystery');
INSERT INTO Category (name) VALUES ('Science Fiction');

INSERT INTO Member (name, phone_number, address) VALUES ('Alice Johnson', '1234567890', '123 Main St');
INSERT INTO Member (name, phone_number, address) VALUES ('Bob Smith', '9876543210', '456 Elm St');
INSERT INTO Member (name, phone_number, address) VALUES ('Carol Davis', '5555555555', '789 Oak St');

INSERT INTO Book (title, publication_date, amount) VALUES ('Book 1', '2022-01-01', 30);
INSERT INTO Book (title, publication_date, amount) VALUES ('Book 2', '2022-02-01', 25);
INSERT INTO Book (title, publication_date, amount) VALUES ('Book 3', '2022-03-01', 21);

INSERT INTO Author_Book (author_id, book_id) VALUES (1, 1);
INSERT INTO Author_Book (author_id, book_id) VALUES (2, 2);
INSERT INTO Author_Book (author_id, book_id) VALUES (3, 3);

INSERT INTO Book_Category (book_id, category_id) VALUES (1, 1);
INSERT INTO Book_Category (book_id, category_id) VALUES (2, 2);
INSERT INTO Book_Category (book_id, category_id) VALUES (3, 3);

-- Tesing trigger and procedures
-- Call the create_loan procedure
DO $$
DECLARE
  loan_id INTEGER;
BEGIN
  CALL create_loan(1, 1, '2023-06-17', loan_id);
  RAISE NOTICE 'Loan ID: %', loan_id;
END $$

-- Call the handle_return procedure
DO $$
DECLARE
  loan_id INTEGER := 1; -- Specify the loan_id of the book to be returned
BEGIN
  CALL handle_return(loan_id);
END $$

-- Call the create_reservation procedure
DO $$
DECLARE
  reservation_id INTEGER;
BEGIN
  CALL create_reservation(2, 2, '2023-06-17', reservation_id);
  RAISE NOTICE 'Reservation ID: %', reservation_id;
END $$

-- Call the add_review procedure
DO $$
DECLARE
  review_id INTEGER;
BEGIN
  CALL add_review(3, 1, 'Great book!', '2023-06-17', review_id);
  RAISE NOTICE 'Review ID: %', review_id;
END $$

-- Call the add_to_favorites procedure
DO $$
DECLARE
  favorite_id INTEGER;
BEGIN
  CALL add_to_favorites(1, 2, favorite_id);
  RAISE NOTICE 'Favorite ID: %', favorite_id;
END $$

-- DELETE
DELETE FROM Author;
SELECT setval(pg_get_serial_sequence('author', 'author_id'), 1, false);
DELETE FROM Category;
SELECT setval(pg_get_serial_sequence('category', 'category_id'), 1, false);
DELETE FROM Member;
SELECT setval(pg_get_serial_sequence('member', 'member_id'), 1, false);
DELETE FROM Book;
SELECT setval(pg_get_serial_sequence('book', 'book_id'), 1, false);
DELETE FROM Loan;
SELECT setval(pg_get_serial_sequence('loan', 'loan_id'), 1, false);
DELETE FROM Reservation;
SELECT setval(pg_get_serial_sequence('reservation', 'reservation_id'), 1, false);
DELETE FROM Author_Book;
SELECT setval(pg_get_serial_sequence('author_book', 'author_book_id'), 1, false);
DELETE FROM Book_Category;
SELECT setval(pg_get_serial_sequence('book_category', 'book_category_id'), 1, false);
DELETE FROM Favorite;
SELECT setval(pg_get_serial_sequence('favorite', 'favorite_id'), 1, false);
DELETE FROM Review;
SELECT setval(pg_get_serial_sequence('review', 'review_id'), 1, false);