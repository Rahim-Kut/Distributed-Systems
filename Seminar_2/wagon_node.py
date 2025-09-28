import time, argparse
from xmlrpc.client import ServerProxy

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--station", required=True, help="http://<STATION_IP>:8000")
    p.add_argument("--wagon", type=int, required=True)
    p.add_argument("--seats", type=int, default=3)
    p.add_argument("--ride", type=float, default=0.6)
    args = p.parse_args()

    rpc = ServerProxy(args.station, allow_none=True)
    while True:
        rpc.wagon_arrived(args.wagon, args.seats)
        while not rpc.check_if_can_depart(args.wagon):
            time.sleep(0.1)
        print(f"[WAGON {args.wagon}] Departing")
        time.sleep(args.ride)
        print(f"[WAGON {args.wagon}] Ride finished")
        rpc.ride_finished(args.wagon)
        time.sleep(0.05)

if __name__ == "__main__":
    main()
