from hstest import *
import random
import hashlib
import os
import string


class Test(StageTest):
    def random_word(self, length):
        letters = string.ascii_lowercase
        capital_letter = random.choice(string.ascii_uppercase)
        return capital_letter + ''.join(random.choice(letters) for i in range(length))

    def random_password(self):
        buffer = string.ascii_lowercase + string.digits
        return ''.join(random.sample(buffer, 8))

    def create_file(self, variant):
        if variant == 'database':
            with open("database.csv", "a") as file:
                file.write('id, nickname, password, consent to mailing')
                for index in range(1, 101):
                    name = random.choice([self.random_word(8), '-'])
                    password = self.random_password()
                    mailing = random.choice(['yes', 'no', '-'])
                    line = f'\n{index}, {name}, {password}, {mailing}'
                    file.write(line)
        if variant == 'hash_database':
            with open("hash_database.csv", "a") as file:
                file.write('id, nickname, password, consent to mailing\n')

    @dynamic_test()
    def test(self):
        random.seed(88)

        if not os.path.isfile('database.csv'):
            self.create_file('database')

        with open('database.csv') as f:
            lines = [line.strip('\n').split(', ') for line in f if len(line) > 1]
            if len(lines) < 101:
                open('database.csv', 'w').close()
                self.create_file('database')
                lines = [line.strip('\n').split(', ') for line in f if len(line) > 1]
            lines.pop(0)
            last_index = int(lines[-1][0])

        if not os.path.isfile('hash_database.csv'):
            self.create_file('hash_database')

        main = TestedProgram()
        main.start()

        with open('hash_database.csv') as f:
            hash_lines = [hash_line.split(', ') for hash_line in f if len(hash_line) > 1]
            if len(hash_lines) == 0:
                return CheckResult.wrong("The hash_database.csv file seems to be empty!")
            if hash_lines[0] != ['id', 'nickname', 'password', 'consent to mailing\n']:
                return CheckResult.wrong("It looks like your file is missing the first line 'id, nickname, password, " 
                                         "consent to mailing'. It should be in the first place, "
                                         " as indicated in the screenshot in the task.")
            if len(hash_lines) < 101:
                return CheckResult.wrong("It looks like your hash_database.csv file has fewer lines "
                                         "than your original database.csv file. You may have lost some lines!")
            if len(hash_lines) > 101:
                return CheckResult.wrong("It seems your hash_database.csv file contains more rows than expected!"
                                         " You may have duplicated the data!")
            hash_lines.pop(0)
            last_index = int(lines[-1][0])

        random_line = random.choice(lines)
        random_id = random_line[0]

        test_hash_password = hashlib.sha256(random_line[2].encode('utf-8')).hexdigest()

        if len(hash_lines[int(random_id) - 1]) < 4:
            return CheckResult.wrong("It seems that you have changed the structure of the string, "
                                     "for example using a delimiter other than a comma in hash_database.csv file!")

        if test_hash_password != hash_lines[int(random_id) - 1][2]:
            return CheckResult.wrong(f'The password hash of the user with id = {random_id} does not match.'
                                f' Your file has {hash_lines[int(random_id) - 1][2]} but expects {test_hash_password}')

        return CheckResult.correct()


if __name__ == '__main__':
    Test().run_tests()
