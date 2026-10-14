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

## Requirements

- Python 3.
- Network connectivity between the participating processes.

All scripts use Python's standard library. The examples were developed for course seminars and use simplified, in-memory state.
