from components.object_detection import scan, follow_gradient, run_row, run_row_v2, follow_gradient_ranged_v2, follow_gradient_ranged
import communication.client as client
import components.engine as engine
import time
import sys

if __name__ == "__main__":
    if len(sys.argv) !=2:
        print("please provide an argument")
        exit()
    cl = client.Client()
    if sys.argv[1] == "--scan":
        scan(client_callback=cl.send)
    if sys.argv[1] == "--nav":
        follow_gradient_ranged_v2(40, cl.send)
    elif sys.argv[1] == "--test":
        try:
            while True:
                time.sleep(0.05)
                state = engine.get_state()
                cl.send(("test", state))

        finally:
            engine.end()
    elif sys.argv[1] == "--row":
        run_row_v2(client_callback=cl.send)
