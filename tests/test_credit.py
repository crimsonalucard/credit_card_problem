from unittest import TestCase
from monads.IO_monad import IO_monad, bind_io, pass_io, print_string, runtime, get_file_descipter_from_string, \
    readline_IO
from utils import compose


class testMain(TestCase):
    def setUp(self):
        print("test begin")

    def test_print_string(self):
        main = lambda: pass_io(print_string("hello"), print_string("world"))
        runtime(main)

    def test_input_io(self):
        main = lambda: bind_io(IO_monad(lambda: "Hello World"), print_string)
        runtime(main)

    def test_get_file_string(self):
        def main():
            x = get_file_descipter_from_string("input_file.txt")
            z = x >= readline_IO
            y = z >= print_string
            return y

        runtime(main)

    def test_compose(self):
        x = lambda i: i + 1
        y = lambda i: i - 1
        w = compose(x, y)
        z = compose(y, y, y)
        self.assertEqual(w(0), 0)
        self.assertEqual(z(0), -3)
