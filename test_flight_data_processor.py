import unittest
from typing import Dict,Union,List
from flightdata.FlightDataProcessor import FlightDataProcessor
import time

class TestFlightDataProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.processor: FlightDataProcessor = FlightDataProcessor()
        self.sample_flights: List[Dict[str, Union[str, int]]] = [
            {
                "flight_number": "AZ001",
                "departure_time": "2025-02-19 15:30",
                "arrival_time": "2025-02-20 03:45",
                "duration_minutes": 375,
                "status": "ON_TIME"
            },
            {
                "flight_number": "AZ002",
                "departure_time": "2025-02-21 11:00",
                "arrival_time": "2025-02-21 16:00",
                "duration_minutes": 300,
                "status": "DELAYED"
            }
        ]
        for flight in self.sample_flights:
            self.processor.add_flight(flight)

    def test_add_flight(self) -> None:
        new_flight = {
            "flight_number": "AZ003",
            "departure_time": "2025-03-01 08:00",
            "arrival_time": "2025-03-01 12:00",
            "duration_minutes": 240,
            "status": "ON_TIME"
        }
        start_time = time.time()
        self.processor.add_flight(new_flight)
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 0.1, "Performance issue: Adding flight took too long")
        self.assertEqual(len(self.processor.flights), 3)
        self.assertIn(new_flight, self.processor.flights)

    def test_remove_flight(self) -> None:
        self.processor.remove_flight("AZ001")
        self.assertEqual(len(self.processor.flights), 1)
        self.assertNotIn("AZ001", [f["flight_number"] for f in self.processor.flights])

    def test_flights_by_status(self) -> None:
        flights = self.processor.flights_by_status("ON_TIME")
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0]["flight_number"], "AZ001")

    def test_get_longest_flight(self) -> None:
        longest_flight = self.processor.get_longest_flight()
        self.assertEqual(longest_flight["flight_number"], "AZ001")
        self.assertEqual(longest_flight["duration_minutes"], max(f["duration_minutes"] for f in self.sample_flights))

    def test_update_flight_status(self) -> None:
        self.processor.update_flight_status("AZ001", "DELAYED")
        self.assertEqual(self.processor.flights[0]["status"], "DELAYED")

    def test_add_duplicate_flight(self) -> None:
        duplicate_flight = self.sample_flights[0].copy()
        initial_length = len(self.processor.flights)
        self.processor.add_flight(duplicate_flight)
        self.assertEqual(len(self.processor.flights), initial_length, "Duplicate flight should not be added")

    def test_remove_nonexistent_flight(self) -> None:
        self.processor.remove_flight("NONEXISTENT")
        self.assertEqual(len(self.processor.flights), 2)

    def test_get_longest_flight_empty(self) -> None:
        for flight in self.sample_flights:
            self.processor.remove_flight(flight["flight_number"])
        self.assertIsNone(self.processor.get_longest_flight())

    def test_update_nonexistent_flight_status(self) -> None:
        self.processor.update_flight_status("NONEXISTENT", "CANCELLED")
        self.assertNotIn("NONEXISTENT", [f["flight_number"] for f in self.processor.flights])

    def test_add_flight_with_missing_fields(self) -> None:
        incomplete_flight = {
            "flight_number": "AZ004",
            "departure_time": "2025-04-10 12:00"
        }
        initial_length = len(self.processor.flights)
        self.processor.add_flight(incomplete_flight)
        self.assertEqual(len(self.processor.flights), initial_length, "Flights with missing fields should not be added")

    def test_remove_flight_from_empty_list(self) -> None:
        self.processor.flights.clear()
        self.processor.remove_flight("AZ001")
        self.assertEqual(len(self.processor.flights), 0)

    def test_update_flight_with_invalid_status(self) -> None:
        invalid_status = "INVALID_STATUS"
        self.processor.update_flight_status("AZ001", invalid_status)
        self.assertNotIn(invalid_status, {"ON_TIME", "DELAYED", "CANCELLED"})
        self.assertNotEqual(self.processor.flights[0]["status"], invalid_status)

if __name__ == "__main__":
    unittest.main()
