use littlelemon;
CALL CancelOrder('54-366-6861');
-- Task 1: Create the Bookings table and insert records

-- Task 1: Create 'bookings' table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT PRIMARY KEY,
    booking_date DATE,
    table_number INT,
    customer_id VARCHAR(50),  -- Match customer_id with the customers table
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
select * from customers;

-- Step 1: Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT PRIMARY KEY,
    booking_date DATE,
    table_number INT,
    customer_id VARCHAR(50),  -- Change to match the data type in customers table
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Step 2: Insert sample data into bookings
INSERT INTO bookings (booking_id, booking_date, table_number, customer_id) VALUES
    (1, '2022-10-10', 5, '72-055-7985'),
    (2, '2022-11-12', 3, '90-876-6799'),
    (3, '2022-10-11', 2, '65-353-0657'),
    (4, '2022-10-13', 2, '77-111-2020');

DELIMITER //

CREATE PROCEDURE CheckBooking(IN booking_date DATE, IN table_number INT)
BEGIN
    DECLARE booking_status VARCHAR(20);

    SELECT COUNT(*) INTO booking_status
    FROM bookings
    WHERE booking_date = booking_date AND table_number = table_number;

    IF booking_status > 0 THEN
        SELECT 'Table is already booked.' AS Status;
    ELSE
        SELECT 'Table is available.' AS Status;
    END IF;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE AddValidBooking(IN booking_date DATE, IN table_number INT, IN customer_id INT)
BEGIN
    DECLARE booking_exists INT DEFAULT 0;

    -- Start the transaction
    START TRANSACTION;

    -- Check if the table is already booked
    SELECT COUNT(*) INTO booking_exists
    FROM bookings
    WHERE booking_date = booking_date AND table_number = table_number;

    IF booking_exists > 0 THEN
        -- If booked, rollback the transaction
        ROLLBACK;
        SELECT 'Booking declined: Table is already booked.' AS Status;
    ELSE
        -- If available, insert the new booking
        INSERT INTO bookings (booking_id, booking_date, table_number, customer_id)
        VALUES (NULL, booking_date, table_number, customer_id);
        -- Commit the transaction
        COMMIT;
        SELECT 'Booking confirmed.' AS Status;
    END IF;
END //

DELIMITER ;
CALL CheckBooking('2022-10-10', 5);
CALL AddValidBooking('2022-10-10', 5, 1);
DELIMITER //

CREATE PROCEDURE AddBooking(
    IN booking_id INT,
    IN customer_id INT,
    IN booking_date DATE,
    IN table_number INT
)
BEGIN
    -- Insert a new booking record into the bookings table
    INSERT INTO bookings (booking_id, customer_id, booking_date, table_number)
    VALUES (booking_id, customer_id, booking_date, table_number);
    
    SELECT 'Booking added successfully.' AS Status;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE UpdateBooking(
    IN booking_id INT,
    IN new_booking_date DATE
)
BEGIN
    -- Update the booking date for the specified booking_id
    UPDATE bookings
    SET booking_date = new_booking_date
    WHERE booking_id = booking_id;
    
    SELECT 'Booking updated successfully.' AS Status;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE CancelBooking(
    IN booking_id INT
)
BEGIN
    -- Delete the booking record for the specified booking_id
    DELETE FROM bookings
    WHERE booking_id = booking_id;
    
    SELECT 'Booking canceled successfully.' AS Status;
END //

DELIMITER ;
CALL AddBooking(5, 1, '2023-10-20', 4);
CALL UpdateBooking(1, '2023-10-25');
CALL CancelBooking(1);

