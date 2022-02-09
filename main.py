

import multiprocessing


def producer(queue, condition):
    while True:
        print(str(multiprocessing.current_process()) + "trying to take lock")
        with condition:
            while queue.qsize() > 5:
                condition.wait()
            print(str(multiprocessing.current_process()) + "put element to queue")
            queue.put(1)
            condition.notify()
            print(str(multiprocessing.current_process()) + "release lock")


def consumer(queue, condition):
    while True:
        print(str(multiprocessing.current_process()) + "trying to take lock")
        with condition:
            while queue.qsize() == 0:
                condition.wait()
            print(str(multiprocessing.current_process()) + "get element from queue")
            queue.get(1)
            condition.notify()
            print(str(multiprocessing.current_process()) + "release lock")


def main():
    queue = multiprocessing.Queue()
    condition = multiprocessing.Condition()
    provider1 = multiprocessing.Process(target=producer, args=(queue, condition,))
    provider2 = multiprocessing.Process(target=producer, args=(queue, condition,))
    consumer1 = multiprocessing.Process(target=consumer, args=(queue, condition,))
    consumer2 = multiprocessing.Process(target=consumer, args=(queue, condition,))
    consumer3 = multiprocessing.Process(target=consumer, args=(queue, condition,))
    provider1.start()
    provider2.start()
    consumer1.start()
    consumer2.start()
    consumer3.start()
    provider1.join()
    provider2.join()
    consumer1.join()
    consumer2.join()
    consumer3.join()


if __name__ == "__main__":  # для определения какой процесс был главным то есть первым
    main()

