DROP TABLE IF EXISTS UKSLEEK.AIRTRAIN.sales_uk;

CREATE TABLE UKSLEEK.AIRTRAIN.sales_uk (
    sales_date DATE,
    quantity_sold INT,
    unit_sell_price DECIMAL(10, 2),
    unit_purchase_cost DECIMAL(10, 2)
);

INSERT INTO sales_uk VALUES
-- 2022
('2022-01-15', 100, 25.00, 18.00),
('2022-05-10', 50, 30.00, 22.00),
('2022-09-25', 80, 27.00, 20.00),

-- 2023
('2023-02-12', 120, 28.00, 21.00),
('2023-06-05', 70, 32.00, 24.00),
('2023-11-19', 90, 29.00, 23.00),

-- 2024
('2024-03-20', 110, 31.00, 25.00),
('2024-07-08', 60, 33.00, 26.00),
('2024-12-30', 75, 34.00, 27.00);



SELECT * FROM sales_uk ORDER BY quantity_sold;