from hstest import *
import random
import string
import os


class Test(StageTest):
    def random_word(self, length):
        letters = string.ascii_lowercase
        capital_letter = random.choice(string.ascii_uppercase)
        return capital_letter + ''.join(random.choice(letters) for i in range(length))

    def random_password(self):
        buffer = string.ascii_lowercase + string.digits
        return ''.join(random.sample(buffer, 8))

    def create_file(self):
        with open("database.csv", "a") as file:
            file.write('id, nickname, password, consent to mailing')
            for index in range(1, 101):
                name = random.choice([self.random_word(8), '-'])
                password = self.random_password()
                mailing = random.choice(['yes', 'no', '-'])
                line = f'\n{index}, {name}, {password}, {mailing}'
                file.write(line)

    @dynamic_test()
    def test(self):
        random.seed(88)

        if not os.path.isfile('database.csv'):
            self.create_file()

        with open('database.csv') as f:
            lines = [line.strip('\n').split(', ') for line in f if len(line) > 1]
            if len(lines) < 101:
                open('database.csv', 'w').close()
                self.create_file()
                lines = [line.strip('\n').split(', ') for line in f if len(line) > 1]
            last_index = int(lines[-1][0])

        csv_index = last_index + 1
        csv_name = random.choice([self.random_word(8), '-'])
        csv_password = self.random_password()
        csv_mailing = random.choice(['yes', 'no', '-'])

        csv_row = f'\n{csv_index}, {csv_name}, {csv_password}, {csv_mailing}'

        with open('database.csv', 'a') as fd:
            fd.write(csv_row)

        main = TestedProgram()
        output = main.start()

        if csv_name not in output:
            return CheckResult.wrong(f'Your program print {output},'
                                     f' but expected {csv_name} nickname of user in the output.')

        if csv_mailing not in output:
            return CheckResult.wrong(f'Your program print "{output}",'
                                     f' but expected "{csv_mailing}" consent to mailing status in the output.')
        if output.count('\n') > 1:
            return CheckResult.wrong(f'It looks like you typed multiple lines when one is required,'
                                     f' or you used too many "\\n" characters')
        if len(output) > 100:
            return CheckResult.wrong(f'It looks like your program is outputting too many characters, even though'
                                     f' it takes significantly fewer characters to write one line with data.')

        with open("database.csv", "r") as f:
            lines = f.readlines()
        with open("database.csv", "w") as f:
            f.write('id, nickname, password, consent to mailing\n')
        with open("database.csv", "a") as f:
            for line in lines[1:last_index + 1]:
                if line == lines[last_index]:
                    f.write(line.strip('\n'))
                else:
                    f.write(line)

        return CheckResult.correct()


if __name__ == '__main__':
    Test().run_tests()
