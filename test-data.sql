INSERT INTO Users
  (fname, lname, email, phone)
VALUES
  ('Kaushik', 'Mishra', 'kaushik@flowerschool.org', '212-434-565'),
  ('John', 'Doe', 'john@flowerschool.org', '121-211-994'),
  ('Mohan', 'Cena', 'mohan@flowerschool.org', ''),
  ('Deep', 'Singh', 'deep@flowerschool.org', '');

INSERT INTO Vendors
  (vendor_name, phone)
VALUES
  ('Bank of America', '800-432-1000'),
  ('Pied Piper', ''),
  ('Hooli', ''),
  ('Google LLC', '866-246-6453');

INSERT INTO Address
  (user_id, address, start_date, end_date)
VALUES
  (1, '8772 West Washington Ave, San Duperino, MT, 20221', '', '2019-09-23'),
  (1, '323 East California Ave, Danger City, NC, 20211', '2019-09-16', '2019-09-24'),
  (2, '423 Seattle Ave, San Fernandinho, MV, 10391', '', ''),
  (2, '32  Johny Ave, Chinatown, BT, 12291', '', ''),
  (3, '582 West Skyline Ave, Bloomington, AT, 97491', '2020-03-20' , ''),
  (4, '2322 Atomic Ave, Harrison, AT, 97321', '', '');

INSERT INTO AddressVendorsMap
  (vendor_id, address_id, vendor_access)
VALUES
  (1, 1, 1),
  (2, 1, 1),
  (2, 2, 1),
  (2, 3, 1),
  (2, 4, 1),
  (3, 1, 1),
  (3, 2, 1),
  (3, 3, 1),
  (4, 1, 1);
