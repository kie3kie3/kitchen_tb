import threading
import handler
import loop


def startBots():
    threadLoop = threading.Thread(target=loop.main)
    threadHandler = threading.Thread(target=handler.main)
    threadLoop.start()
    threadHandler.start()
    print('Nice')


def main():
    startBots()


main()

