-- Trigger for status updating
CREATE OR REPLACE FUNCTION update_fish_n_status()
RETURNS trigger AS
$$
BEGIN
    IF NEW.product_key='fish_forel' THEN
        UPDATE orders
            SET pay_stat = 'Yes'
            WHERE order_id = NEW.order_id;

        UPDATE orders
            SET result_price = (
                SELECT SUM(oc.price)
                    FROM orders_content oc
                    WHERE oc.order_id = NEW.order_id
            )
            WHERE order_id = NEW.order_id
        ;
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER update_status_on_fish_load
AFTER UPDATE
ON orders_content
FOR EACH ROW
EXECUTE PROCEDURE update_fish_n_status();

-- Triiger for clearing orders_content when removing any order.
CREATE OR REPLACE FUNCTION clear_orders_content()
RETURNS trigger AS
$$
BEGIN
	DELETE FROM orders_content
		WHERE order_id = OLD.order_id;
	RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER clear_orders_content_on_delete
BEFORE DELETE
ON orders
FOR EACH ROW
EXECUTE PROCEDURE clear_orders_content();

-- Trigger for updating stock on deleting orders;
CREATE OR REPLACE FUNCTION back_update_stock()
RETURNS trigger AS
$$
BEGIN
	UPDATE products
        SET in_stock = in_stock + OLD.amount
        WHERE product_key = OLD.product_key;
	RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER backup_stock
AFTER DELETE
ON orders_content
FOR EACH ROW
EXECUTE PROCEDURE back_update_stock();


-- Trigger for stock updating after  creating new order
CREATE OR REPLACE FUNCTION update_stock()
RETURNS trigger AS
$$
BEGIN
	UPDATE products SET in_stock = in_stock - NEW.amount WHERE product_key = NEW.product_key;
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER on_order_creating
AFTER INSERT
ON orders_content
FOR EACH ROW
EXECUTE PROCEDURE update_stock();


-- Trigger for Supply table using =)
CREATE OR REPLACE FUNCTION update_supply_n_oc()
RETURNS trigger AS
$$
DECLARE
    amounts CURSOR (PRK VARCHAR(15)) IS
        SELECT *
        FROM supply
        WHERE
            product_key = PRK
                AND
            in_stock > 0
        ORDER BY supply_id;

    L supply%ROWTYPE;

    result_price    NUMERIC(8,2);
    balance_amount  NUMERIC(8,2);
    last_price      NUMERIC(8,2);
BEGIN
    result_price   := 0;
    balance_amount := NEW.amount;

    FOR L IN amounts(NEW.product_key) LOOP
        last_price := L.price;
        EXIT WHEN (balance_amount = 0);
        IF L.in_stock >= balance_amount THEN
            result_price := result_price + balance_amount*L.price;
            UPDATE supply SET in_stock = L.in_stock - balance_amount WHERE supply_id = L.supply_id AND product_key = L.product_key;
            balance_amount := 0;
        ELSE
            result_price := result_price + L.in_stock*L.price;
            UPDATE supply SET in_stock = 0 WHERE supply_id = L.supply_id AND product_key = L.product_key;
            balance_amount := balance_amount - L.in_stock;
        END IF;
    END LOOP;

    IF balance_amount = NEW.amount THEN
        RETURN NEW;
    ELSE
        result_price := result_price + balance_amount*last_price;
    END IF;

    NEW.cost_price := ROUND(result_price);
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER on_insert_to_orders_cont
BEFORE INSERT
ON orders_content
FOR EACH ROW
EXECUTE PROCEDURE update_supply_n_oc();

-- Trigger for NULLed cost_price products in order_content
CREATE OR REPLACE FUNCTION upd_oc_on_sup_ins_func()
RETURNS trigger AS
$$
BEGIN
    UPDATE orders_content SET cost_price = amount*NEW.price WHERE cost_price is NULL AND product_key = NEW.product_key;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER upd_oc_on_sup_ins
BEFORE INSERT
ON supply
FOR EACH ROW
EXECUTE PROCEDURE upd_oc_on_sup_ins_func();

