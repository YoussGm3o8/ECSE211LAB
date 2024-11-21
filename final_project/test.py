from components.object_detection import scan
import communication.client as client
import components.engine as engine
import time

if __name__ == "__main__":
    cl = client.Client()
    print(scan(cl.send))

#     try:
#         while True:
#             time.sleep(0.05)
#             state = engine.get_state()
#             cl.send(state)
#
#     finally:
#         engine.end()
# # def scan_mean(client_callback=None):
