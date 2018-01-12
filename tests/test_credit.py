from unittest import TestCase
from utils import compose, string_to_list_of_strings, string_of_nums_to_list_of_ints, dollar_to_number
from validators import validate_charge, validate_number, validate_decorator, card_pass_decorator
from card import create_card, charge_card, credit_card
from custrom_types import Card
from state import state, add, charge, credit, get_card, set_card
from parsing import string_to_command, list_of_strings_to_commands
from display import display_card_error, card_to_string, state_to_str


class TestMain(TestCase):
    def setUp(self):
        self.dummyCard = Card("brian", 400, 1000, [1, 2, 3])
        self.tom = Card("Tom", 0, 1000, [int(i) for i in '4111111111111111'])
        self.lisa = Card('lisa', 0, 300, [int(i) for i in '5454545454545454'])
        self.quincy = Card('Quincy', 0, 2000, [int(i) for i in '1234567890123456'])

    def test_compose(self):
        x = lambda i: i + 1
        y = lambda i: i - 1
        w = compose(x, y)
        z = compose(y, y, y)
        self.assertEqual(w(0), 0)
        self.assertEqual(z(0), -3)

    def test_string_to_list_of_strings(self):
        self.assertEqual(string_to_list_of_strings("Hello World"), ["Hello", "World"])

    def test_charge_validation(self):
        self.assertTrue(validate_charge(self.dummyCard, 200))
        self.assertFalse(validate_charge(self.dummyCard, 5000))

    def test_luhn10_validation(self):
        self.assertTrue(validate_number(self.tom))
        self.assertTrue(validate_number(self.lisa))
        self.assertFalse(validate_number(self.quincy))
        self.assertTrue(validate_number(create_card("blah", string_of_nums_to_list_of_ints("49927398716"), 2000)))
        test_cases = [4206478516190347, 4419983825796737, 4946298813581617, 2479385739857934857983]
        test_cases = [string_of_nums_to_list_of_ints(str(i)) for i in test_cases]
        for number in test_cases:
            if string_of_nums_to_list_of_ints(str(2479385739857934857983)) != number:
                self.assertTrue(validate_number(create_card("blah", number, 2000)))
            else:
                self.assertFalse(validate_number(create_card("blah", number, 2000)))

    def test_validate_decortator(self):
        id = lambda x: x

        @validate_decorator(id, lambda *args, **kwargs: 99, lambda *args, **kwargs: -1)
        def test_func(x):
            return x

        self.assertEqual(test_func(True), 99)
        self.assertEqual(test_func(False), -1)

    def test_card_pass_decorator(self):
        @card_pass_decorator(validate_number)
        def test_func(card):
            return self.lisa

        self.assertEqual(self.lisa, test_func(self.tom))
        self.assertEqual(self.quincy, test_func(self.quincy))

    def test_dollar_to_number(self):
        self.assertEqual(dollar_to_number("$1000"), 1000)
        self.assertEqual(dollar_to_number("$1000\n "), 1000)

    def test_create_card(self):
        number = string_of_nums_to_list_of_ints("4111111111111111")
        self.assertEqual(Card("brian", 0, 0, number), create_card("brian", number, 0, 0))

    def test_charge_card(self):
        number = string_of_nums_to_list_of_ints("4111111111111111")
        card = create_card("brian", number, 1000)
        card2 = create_card("brian", number, 1000, 100)
        self.assertEqual(charge_card(card, 2000), card)
        self.assertEqual(charge_card(card, 100), card2)

        number = string_of_nums_to_list_of_ints("4111234243345111111111")
        card = create_card("brian", number, 1000)
        self.assertEqual(charge_card(card, 200), card)
        self.assertEqual(charge_card(card, 100), card)

    def test_credit_card(self):
        number = string_of_nums_to_list_of_ints("4111111111111111")
        card = create_card("brian", number, 1000)
        card2 = create_card("brian", number, 1000, -200)
        self.assertEqual(credit_card(card, 200), card2)

        number = string_of_nums_to_list_of_ints("411111112343453511111111")
        card = create_card("brian", number, 1000)
        self.assertEqual(credit_card(card, 200), card)

    def test_state_add(self):
        add("brian", "4111111111111111", "$2000")
        self.assertEqual(state["brian"], create_card("brian", string_of_nums_to_list_of_ints("4111111111111111"), 2000))

    def test_state_charge(self):
        charge("brian", "$200")
        self.assertEqual(state["brian"],
                         create_card("brian", string_of_nums_to_list_of_ints("4111111111111111"), 2000, 200))

    def test_state_get_card(self):
        self.assertEqual(state["brian"], get_card("brian"))

    def test_state_set_card(self):
        set_card(create_card("susie", string_of_nums_to_list_of_ints("4111111111111111"), 2000))
        self.assertEqual(state["susie"], get_card("susie"))

    def test_state_credit(self):
        credit("brian", "$200")
        self.assertEqual(state["brian"], create_card("brian", string_of_nums_to_list_of_ints("4111111111111111"), 2000))

    def test_command_add(self):
        command = string_to_command("Add marv 4111111111111111 $2000")
        command()
        self.assertEqual(state["marv"], create_card("marv", string_of_nums_to_list_of_ints("4111111111111111"), 2000))

    def test_command_charge(self):
        command = string_to_command("Add marv 4111111111111111 $2000")
        command2 = string_to_command("Charge marv $200")
        command()
        command2()
        self.assertEqual(state["marv"],
                         create_card("marv", string_of_nums_to_list_of_ints("4111111111111111"), 2000, 200))

        command = string_to_command("Add marv 41111111345611111111 $2000")
        command2 = string_to_command("Charge marv $200")
        command()
        command2()
        self.assertEqual(state["marv"],
                         create_card("marv", string_of_nums_to_list_of_ints("41111111345611111111"), 2000))

    def test_command_credit(self):
        command = string_to_command("Add sam 4111111111111111 $2000")
        command2 = string_to_command("Credit sam $200")
        command()
        command2()
        self.assertEqual(state["sam"],
                         create_card("sam", string_of_nums_to_list_of_ints("4111111111111111"), 2000, -200))

        command = string_to_command("Add sam 41111111345611111111 $2000")
        command2 = string_to_command("Credit sam $200")
        command()
        command2()
        self.assertEqual(state["sam"],
                         create_card("sam", string_of_nums_to_list_of_ints("41111111345611111111"), 2000))

    def test_list_of_strings_to_commands(self):
        x = ["Add sam 4111111111111111 $2000", "Credit sam $200"]
        commands = list_of_strings_to_commands(x)
        commands[0]()
        commands[1]()
        self.assertEqual(state["sam"],
                         create_card("sam", string_of_nums_to_list_of_ints("4111111111111111"), 2000, -200))

        x = ["Add sam 411111111134534111111 $2000", "Credit sam $200"]
        commands = list_of_strings_to_commands(x)
        commands[0]()
        commands[1]()
        self.assertEqual(state["sam"],
                         create_card("sam", string_of_nums_to_list_of_ints("411111111134534111111"), 2000))

    def test_display_card_error(self):
        self.assertEqual(display_card_error(self.lisa), "lisa: error")

    def test_card_to_string(self):
        card = create_card("sam", string_of_nums_to_list_of_ints("4111111111111111"), 1000, 200)
        card2 = create_card("fred", string_of_nums_to_list_of_ints("4111111111111111"), 1000, -200)
        card3 = create_card("bob", string_of_nums_to_list_of_ints("41111111353411111111"), 1000, -200)
        self.assertEqual(card_to_string(card), "sam: $200")
        self.assertEqual(card_to_string(card2), "fred: $-200")
        self.assertEqual(card_to_string(card3), "bob: error")

    def test_state(self):
        x = [key for key in state]
        for key in x:
            del state[key]

        strings = ["Add Tom 4111111111111111 $1000",
                   "Add Lisa 5454545454545454 $3000",
                   "Add Quincy 1234567890123456 $2000",
                   "Charge Tom $500",
                   "Charge Tom $800",
                   "Charge Lisa $7",
                   "Credit Lisa $100",
                   "Credit Quincy $200"]
        commands = list_of_strings_to_commands(strings)
        [i() for i in commands]
        test = state_to_str(state)
        test2 = ["Lisa: $-93",
                 "Quincy: error",
                 "Tom: $500"]
        self.assertEqual(set(test), set(test2))
