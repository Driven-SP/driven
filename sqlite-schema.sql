DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Vendors;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS AddressVendorsMap;

CREATE TABLE IF NOT EXISTS Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT
);

CREATE TABLE IF NOT EXISTS Vendors (
  vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
  vendor_name TEXT NOT NULL,
  phone TEXT
);

CREATE TABLE IF NOT EXISTS Address (
  address_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  address TEXT NOT NULL,
  start_date TEXT,
  end_date TEXT,
  FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AddressVendorsMap (
  vendor_id INTEGER,
  address_id INTEGER,
  vendor_access BOOLEAN NOT NULL CHECK (vendor_access IN (0, 1)),
  PRIMARY KEY(vendor_id, address_id),
  FOREIGN KEY(vendor_id) REFERENCES Vendors(vendor_id) ON DELETE CASCADE,
  FOREIGN KEY(address_id) REFERENCES Address(address_id) ON DELETE CASCADE
);
