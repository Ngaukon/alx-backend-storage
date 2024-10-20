-- Creates a trigger to reduce the quantity of an item after a new order is added
-- This trigger decreases the item’s quantity based on the number ordered
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMITER $$
CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END $$
DELIMITER ;
