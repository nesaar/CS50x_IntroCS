-- Keep a log of any SQL queries you execute as you solve the mystery.

-- have a look at the crime scene reports table
select * from crime_scene_reports

-- check for the specific crime location
select * from crime_scene_reports where street = "Humphrey Street";
-- 10.15am

-- check whats in the interviews table
select * from interviews;

-- check what interviews were done on the day of the crime 28.07.2021
select * from interviews where year = 2021 and month = 7 and day = 28;

-- who are the witnesses for the interviews [Eugene; Raymond; Ruth]
-- who was at the ATM the morning of the robbery on Leggett Street
select c.* from atm_transactions a, bank_accounts b, people c where c.id = b.person_id and a.account_number = b.account_number and atm_location = "Leggett Street" and year = "2021" and month = "7" and day = "28" and transaction_type = "withdraw";
-- Bruce is in this list

-- check the flights table for the earliest flight out of fiftyville the next day
-- as well as the longest flight
select * from flights where year = 2021 and month = 7 and day = 29;
-- flight id = 36 from fiftyville
-- it is going to LaGuardia

-- who were the passengers on this early flight on the morning (8h20)
select * from passengers a, people b where flight_id = 36 and a.passport_number = b.passport_number;
-- Bruce/Kenny/Luca/Taylor

-- who made phone calls on the day of the robbery for less than 60s as per the witness statement
select * from phone_calls where year = 2021 and month = 7 and day = 28 and duration < 60;
select * from people where phone_number in (select caller from phone_calls where year = 2021 and month = 7 and day = 28 and duration < 60);
select * from people where phone_number in (select receiver from phone_calls where year = 2021 and month = 7 and day = 28 and duration < 60);
+--------+------------+----------------+-----------------+---------------+
|   id   |    name    |  phone_number  | passport_number | license_plate |
+--------+------------+----------------+-----------------+---------------+
| 250277 | James      | (676) 555-6554 | 2438825627      | Q13SVG6       |
| 251693 | Larry      | (892) 555-8872 | 2312901747      | O268ZZ0       |
| 484375 | Anna       | (704) 555-2131 |                 |               |
| 567218 | Jack       | (996) 555-8899 | 9029462229      | 52R0Y8U       |
| 626361 | Melissa    | (717) 555-1342 | 7834357192      |               |
| 712712 | Jacqueline | (910) 555-3251 |                 | 43V0R5D       |
| 847116 | Philip     | (725) 555-3243 | 3391710505      | GW362R6       |
| 864400 | Robin      | (375) 555-8161 |                 | 4V16VO0       |
| 953679 | Doris      | (066) 555-9701 | 7214083635      | M51FA04       |
+--------+------------+----------------+-----------------+---------------+


-- check the bakery logs for a car driving away at the time of the robbery. This is from a witness statement
SELECT name, bakery_security_logs.hour, bakery_security_logs.minute
  FROM people
  JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
 WHERE bakery_security_logs.year = 2021
   AND bakery_security_logs.month = 7
   AND bakery_security_logs.day = 28
   AND bakery_security_logs.activity = 'exit'
   AND bakery_security_logs.hour = 10
   AND bakery_security_logs.minute >= 15
   AND bakery_security_logs.minute <= 25
 ORDER BY bakery_security_logs.minute
 -- Bruce/Luca



