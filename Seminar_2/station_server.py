from xmlrpc.server import SimpleXMLRPCServer
from collections import deque

# People (person_id)
people_queue = deque()

# Wagons (wagon_id, capacity)
wagon_queue = deque()

# Trip info for the wagon currently boarding at the front of the line
trip = {}

# If the first wagon can be filled, pick the earliest people and set up its trip
def _try_to_fill_front_wagon():
    while wagon_queue and len(people_queue) >= wagon_queue[0][1]:
        wagon_id, capacity = wagon_queue[0]  # keep it at the front until this whole trip is done
        if wagon_id in trip:
            break  # already busy boarding this wagon
        chosen = [people_queue.popleft() for _ in range(capacity)]
        trip[wagon_id] = {
            "capacity": capacity,
            "chosen_people": set(chosen),
            "boarded_count": 0,
            "off_count": 0,
            "seat_granted": {pid: True for pid in chosen},
            "can_depart": False,
            "may_get_off": {pid: False for pid in chosen},
            "boarded_mark": {},
            "off_mark": {}
        }
        break  # only handle the very front wagon

# Passenger side
def join_line(person_id):
    people_queue.append(person_id)
    _try_to_fill_front_wagon()
    return True

def check_if_seat_granted(person_id):
    # Return wagon_id if this person has a seat, otherwise -1
    for wagon_id, info in trip.items():
        if info["seat_granted"].get(person_id):
            return wagon_id
    return -1

def say_i_got_on(person_id, wagon_id):
    info = trip.get(wagon_id)
    if not info or person_id not in info["chosen_people"]:
        return False
    if not info["boarded_mark"].get(person_id):
        info["boarded_mark"][person_id] = True
        info["boarded_count"] += 1
        if info["boarded_count"] == info["capacity"]:
            info["can_depart"] = True
    return True

def check_if_may_get_off(person_id, wagon_id):
    info = trip.get(wagon_id)
    return bool(info and info["may_get_off"].get(person_id, False))

def say_i_got_off(person_id, wagon_id):
    info = trip.get(wagon_id)
    if not info or person_id not in info["chosen_people"]:
        return False
    if not info["off_mark"].get(person_id):
        info["off_mark"][person_id] = True
        info["off_count"] += 1
        if info["off_count"] == info["capacity"]:
            # Trip finished: move this wagon to the back, clear trip, try next
            if wagon_queue and wagon_queue[0][0] == wagon_id:
                wagon_queue.popleft()
            wagon_queue.append((wagon_id, info["capacity"]))
            trip.pop(wagon_id, None)
            _try_to_fill_front_wagon()
    return True

# Wagon side
def wagon_arrived(wagon_id, capacity):
    # Ignore repeat registration: finished wagons are already requeued.
    if any(queued_id == wagon_id for queued_id, _ in wagon_queue):
        return True
    wagon_queue.append((wagon_id, capacity))
    _try_to_fill_front_wagon()
    return True

def check_if_can_depart(wagon_id):
    info = trip.get(wagon_id)
    return bool(info and info["can_depart"])

def ride_finished(wagon_id):
    info = trip.get(wagon_id)
    if not info:
        return False
    info["can_depart"] = False
    # Allow the chosen people to get off
    for pid in info["chosen_people"]:
        info["may_get_off"][pid] = True
    return True

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
    for fn in [join_line, check_if_seat_granted, say_i_got_on, check_if_may_get_off, say_i_got_off,
               wagon_arrived, check_if_can_depart, ride_finished]:
        server.register_function(fn)
    print("Station listening on :8000")
    server.serve_forever()
