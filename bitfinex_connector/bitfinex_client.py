import os
from common_components.client import Client
import asyncio


class BitfinexClient(Client):

    def __init__(self, ccy):
        super(BitfinexClient, self).__init__(ccy, 'bitfinex')

    def run(self):
        """
        Handle incoming level 3 data on a separate process
        (or process, depending on implementation)
        :return:
        """
        print('BitfinexClient run - Process ID: %s\nThread: %s' % (str(os.getpid()), self.name))
        while True:
            msg = self.queue.get()

            if self.book.new_tick(msg) is False:
                print('\n%s missing a tick...going to try and reload the order book\n' % self.sym)
                self.subscribe()
                self.retry_counter += 1
                self.queue.task_done()
                continue

            self.queue.task_done()


# -------------------------------------------------------------------------------------------------------

# """
# This __main__ function is used for testing the
# BitfinexClient class in isolation.
# """
# if __name__ == "__main__":
#     print('BitfinexClient __main__ - Process ID: %s' % str(os.getpid()))
#     symbols = ['tETHUSD']  #, 'tBCHUSD', 'tETHUSD', 'tLTCUSD']
#     print('Initializing...%s' % symbols)
#     loop = asyncio.get_event_loop()
#     p = dict()
#
#     for sym in symbols:
#         p[sym] = BitfinexClient(sym)
#         p[sym].start()
#
#     tasks = asyncio.gather(*[(p[sym].subscribe()) for sym in symbols])
#     print('Gathered %i tasks' % len(symbols))
#
#     try:
#         loop.run_until_complete(tasks)
#         loop.close()
#         print('loop closed.')
#
#     except KeyboardInterrupt as e:
#         print("Caught keyboard interrupt. Canceling tasks...")
#         tasks.cancel()
#         # loop.run_forever()
#         for sym in symbols:
#             p[sym].join()
#             print('Closing [%s]' % p[sym].name)
#
#     finally:
#         loop.close()
#         print('\nFinally done.')