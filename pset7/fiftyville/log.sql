-- First running this query to know something more about the crime scene
SELECT * FROM crime_scene_reports WHERE day = 28 AND street = "Chamberlin Street";

-- Selecting everything from interviews of people for that day
SELECT * FROM interviews WHERE day = 28 AND year = 2020;
-- This way we knew that thief used a car as a getaway vehicle and had an accomplice who bought tickets

-- Seelcting all flights on the following day. Then selecting the earliest one.
SELECT * FROM flights WHERE day = 29 AND year = 2020
SELECT id,city, full_name FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE day = 29 AND year = 2020);
-- This is how we know now that thief escaped to London

-- So from information above we have the id of flight which is 36. And from this query we know the names of people who were on that flight
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);
Bobby
Roger
Madison
Danielle
Evelyn
Edward
Ernest
Doris
-- Now we just need to check who called who
-- After checking all it appears that Ernest has called to some number for less then a minute on the day of theft:
233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
-- He called  some guy Berthold
864400 | Berthold | (375) 555-8161 |  | 4V16VO0 (with no passport)
-- I tought that is suspicious.So I ran the license plates throug security footage
SELECT * FROM courthouse_security_logs WHERE license_plate = "4V16VO0";
id | year | month | day | hour | minute | activity | license_plate
248 | 2020 | 7 | 28 | 8 | 50 | entrance | 4V16VO0
249 | 2020 | 7 | 28 | 8 | 50 | exit | 4V16VO0
-- And it appears to me that This was very quick heist under a minute to go inside and to exit.
-- So because Ernest connected to Berthold. And Ernest is on that flight to London I can conclude that this is who we are looking for.