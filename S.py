DELIMITER $$

CREATE TRIGGER calculate_total_travel_cost
AFTER INSERT ON expense_travel_mapper
FOR EACH ROW
BEGIN
    DECLARE last_total FLOAT;

    -- Get the last total cost for the same expense_request_id
    SELECT IFNULL(MAX(travel_total_expense), 0)
    INTO last_total
    FROM expense_travel_mapper
    WHERE expense_request_id = NEW.expense_request_id
    AND expense_travel_mapper_id != NEW.expense_travel_mapper_id;

    -- Update the total cost for the current record
    UPDATE expense_travel_mapper
    SET travel_total_expense = NEW.travel_total_expense + last_total
    WHERE expense_travel_mapper_id = NEW.expense_travel_mapper_id;
END $$

DELIMITER ;
