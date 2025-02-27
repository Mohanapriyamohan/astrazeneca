from typing import List, Dict, Optional, Union



class FlightDataProcessor:
    """
    A class to process and manage flight data.
    """

    def __init__(self) -> None:
        """Initializes an empty flight list."""
        self.flights: List[Dict[str, Union[str, int]]] = []

    def add_flight(self, data: Dict[str, Union[str, int]]) -> None:
        """To add flight"""
        required_keys = {"flight_number", "departure_time", "arrival_time", "duration_minutes", "status"}
        if not required_keys.issubset(data.keys()):
            return  # Ignore incomplete flight entries

        if not any(f["flight_number"] == data["flight_number"] for f in self.flights):
            self.flights.append(data)

    def remove_flight(self, flight_number: str) -> None:
        """Removes a flight based on the flight number."""
        self.flights = [f for f in self.flights if f["flight_number"] != flight_number]

    def flights_by_status(self, status: str) -> List[Dict[str, Union[str, int]]]:
        """Returns all flights with a given status."""
        return [f for f in self.flights if f["status"] == status]

    def get_longest_flight(self) -> Optional[Dict[str, Union[str, int]]]:
        """Returns the flight with the longest duration in minutes."""
        return max(self.flights, key=lambda f: f.get("duration_minutes", 0), default=None)

    def update_flight_status(self, flight_number: str, new_status: str) -> None:
        """Updates the status of a flight only if the new status is valid."""
        if new_status not in ["ON_TIME", "DELAYED", "CANCELLED"]:
            return  # Ignore invalid status updates
        for f in self.flights:
            if f["flight_number"] == flight_number:
                f["status"] = new_status
                break
