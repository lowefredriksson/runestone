# #!/usr/bin/python
# import websocket
# import _thread
# import time
#
#
# def on_message(ws, message):
#     print(message)
#
#
# def on_error(ws, error):
#     print(error)
#
#
# def on_close(ws):
#     print("### closed ###")
#
#
# def on_open(ws):
#     def run(*args):
#         for i in range(30000):
#             time.sleep(1)
#             ws.send("Hello %d" % i)
#         time.sleep(1)
#         ws.close()
#         print("thread terminating...")
#     _thread.start_new_thread(run, ())
#
#
# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("ws://localhost:8080",
#                                 on_message = on_message,
#                                 on_error = on_error,
#                                 on_close = on_close)
#     ws.on_open = on_open
#
#     ws.run_forever()

from tornado import websocket
import tornado.ioloop

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("Websocket Opened")

    def on_message(self, message):
        self.write_message(u"You said: %s" % message)

    def on_close(self):
        print("Websocket closed")

application = tornado.web.Application([(r"/", EchoWebSocket),])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()