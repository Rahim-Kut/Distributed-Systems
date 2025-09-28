import time, argparse
from xmlrpc.client import ServerProxy

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--station", required=True, help="http://<STATION_IP>:8000")
    p.add_argument("--person", type=int, required=True)
    p.add_argument("--delay", type=float, default=0.0)  # arrive later to show fairness
    args = p.parse_args()

    rpc = ServerProxy(args.station, allow_none=True)

    time.sleep(args.delay)
    rpc.join_line(args.person)

    wagon_id = -1
    while wagon_id < 0:
        wagon_id = rpc.check_if_seat_granted(args.person)
        time.sleep(0.1)
    print(f"[PERSON {args.person}] Got a seat on wagon {wagon_id}")

    rpc.say_i_got_on(args.person, wagon_id)
    print(f"[PERSON {args.person}] Boarded wagon {wagon_id}")

    while not rpc.check_if_may_get_off(args.person, wagon_id):
        time.sleep(0.1)
    rpc.say_i_got_off(args.person, wagon_id)
    print(f"[PERSON {args.person}] Got off wagon {wagon_id}")

if __name__ == "__main__":
    main()
