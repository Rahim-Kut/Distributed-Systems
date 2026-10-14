# Distributed Systems

Python implementations from seminar assignments in the **Distributed Systems** course at **Örebro University**, autumn 2025.

The examples explore network communication, remote procedure calls (RPC), and coordination between separate processes.

## Repository contents

| Folder | Topic | Main files |
|---|---|---|
| `Seminar_1` | UDP communication and network measurements | `udp_client.py` |
| `Seminar_2` | RPC-based coordination of passengers and wagons | `station_server.py`, `passenger_node.py`, `wagon_node.py` |

## Seminar 1 — UDP communication

The UDP client sends a configurable number of messages to a server and measures the time taken to receive each response.

It records:
- Sent and received messages.
- Requests that time out.
- Estimated packet loss.
- Minimum, average, and maximum round-trip time.

The server address, port, message count, payload size, and timeout are configured in the script. A responding UDP server is required and is not included in this repository.

## Seminar 2 — RPC-based coordination

This example models passengers waiting to board wagons. Separate passenger and wagon processes communicate with a central station through Python's XML-RPC interface.

- **Station server:** Maintains passenger and wagon queues, allocates seats, tracks boarding and disembarking, and controls departure permission.
- **Passenger node:** Joins the queue, waits for a seat, reports boarding, and waits for permission to get off.
- **Wagon node:** Registers with the station, waits for departure permission, simulates a ride, and reports its completion.

The station selects passengers in queue order and grants departure permission once all selected passengers have reported boarding.

## How to run

### Seminar 1 — UDP communication

Configure `HOST` and `PORT` in `Seminar_1/udp_client.py` to point to a running UDP server that replies to messages, then run:

```bash
python Seminar_1/udp_client.py
```
The UDP server is not included in this repository.

### Seminar 2 — RPC-based coordination

Run each command in a **separate terminal**, starting from the repository's root folder. This example runs all processes on the same computer.

1. Start the station server:

   ```bash
   python Seminar_2/station_server.py
   ```

2. Start a wagon with two seats:

   ```bash
   python Seminar_2/wagon_node.py --station http://localhost:8000 --wagon 1 --seats 2
   ```

3. Start the first passenger:

   ```bash
   python Seminar_2/passenger_node.py --station http://localhost:8000 --person 1
   ```

4. Start the second passenger:

   ```bash
   python Seminar_2/passenger_node.py --station http://localhost:8000 --person 2
   ```

Once both passengers have boarded, the wagon departs, simulates a ride, and allows them to get off. The wagon then waits for more passengers.

Use a unique `--person` ID for each new passenger. Press **Ctrl+C** in each terminal to stop the running processes.

To run across multiple computers, replace `localhost` in the client commands with the station computer's IP address. The clients must be able to reach its port `8000`.

If your system uses `python3` as its Python command, use that instead of `python`.

## Requirements

- Python 3.
- Network connectivity between the participating processes.

All scripts use Python's standard library. The examples were developed for course seminars and use simplified, in-memory state.
