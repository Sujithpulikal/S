DELIMITER $$

CREATE TRIGGER update_total_on_accommodation_insert
AFTER INSERT ON expense_accommodation_mapper
FOR EACH ROW
BEGIN
    DECLARE travel_total FLOAT;
    DECLARE accommodation_total FLOAT;
    DECLARE travel_count INT;
    
    -- Check if travel data exists for this request
    SELECT COUNT(*)
    INTO travel_count
    FROM expense_travel_mapper
    WHERE expense_request_id = NEW.expense_request_id;
    
    -- Proceed only if travel data exists
    IF travel_count > 0 THEN
        -- Get total from travel table
        SELECT IFNULL(SUM(travel_total_expense), 0)
        INTO travel_total
        FROM expense_travel_mapper
        WHERE expense_request_id = NEW.expense_request_id;

        -- Get total from accommodation table
        SELECT IFNULL(SUM(total_accommodation_cost), 0)
        INTO accommodation_total
        FROM expense_accommodation_mapper
        WHERE expense_request_id = NEW.expense_request_id;

        -- Update total in expense_request table
        UPDATE expense_request
        SET total_amount = travel_total + accommodation_total
        WHERE expense_request_id = NEW.expense_request_id;
    END IF;
END $$

DELIMITER ;
