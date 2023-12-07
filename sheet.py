from asyncio.log import logger
import gspread
import logging
from datetime import datetime
from datetime import timedelta
from datetime import date
import schedule
import threading
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
sa = gspread.service_account("service_account.json")
sh = sa.open("Доступ в К006")
wks = sh.worksheet("Расписание К006")
people = sh.worksheet("Список студентов с доступом")


class Sheet:
    days = {'Mon': 'B', 'Tue': 'C', 'Wed': 'D',
            'Thu': 'E', 'Fri': 'F', 'Sat': 'G', 'Sun': 'H'}
    days_int = {'Mon': 1, 'Tue': 2, 'Wed': 3,
                'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    times = {9: '3', 10: '4', 11: '5', 12: '6', 13: '7', 14: '8', 15: '9',
             16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15', 22: '16'}

    @classmethod
    def isLimitless(self, name):
        cell = people.find(name)
        if people.cell(cell.row, 7).value == '1':
            return True
        return False

    @classmethod
    def isOverLimit(self, name):
        reps = 0
        listed = wks.get('B3:H16')
        for rows in listed:
            for cells in rows:
                if cells.lower() == name.lower():
                    reps += 1
        if not self.isLimitless(name):
            if reps >= 2:
                return True
        return False

    @classmethod
    def isListed(self, username):
        user_conf = people.col_values(7)
        if username in user_conf:
            return True
        return False

    @classmethod
    def add(self, username, day, time):
        listed = people.col_values(2)
        user_conf = people.col_values(7)
        for i, person in enumerate(listed):
            arr = person.split()
            if len(person) <= 1:
                pass
            elif (username == user_conf[i]):
                name = (arr[0].lower().capitalize() +
                        ' ' + arr[-1].lower().capitalize())

        if not self.isOverLimit(name):
            slot = ''
            if day in self.days and time in self.times:
                slot = self.days[day] + self.times[time]
            if wks.acell(slot).value:
                return 'This time slot is already booked.'
            arr = name.split()
            name = arr[0].lower().capitalize() + ' ' + \
                arr[-1].lower().capitalize()

            wks.update(slot, name)
            logger.info("Time slot added by %s on %s at %s:00",
                        name, day, time)
            return 'Success. \nPlease, notify other people in case of cancelation.'
        return 'You have booked more than 2 slots'

    # @classmethod
    # def myslots(self, name):
    #     wks.get()
    #     pass

    @classmethod
    def delete(self, context, username, day, time):
        listed = people.col_values(2)
        user_conf = people.col_values(7)
        for i, person in enumerate(listed):
            arr = person.split()
            if len(person) <= 1:
                pass
            elif (username == user_conf[i]):
                name = (arr[0].lower().capitalize() +
                        ' ' + arr[-1].lower().capitalize())
        if date.isoweekday(date.today()) <= int(self.days_int[day]):
            slot = ''
            if day in self.days and time in self.times:
                slot = self.days[day] + self.times[time]
            if wks.acell(slot).value == None:
                return 'It is empty'

            arr = name.split()
            name = arr[0].lower().capitalize() + ' ' + \
                arr[-1].lower().capitalize()

            if wks.acell(slot).value != name:
                return 'You can not delete time slots of others'
            wks.update(slot, '')
            chat_id = -1001874582867
            deleted_message = f"A timeslot has been deleted. {day}, {time}:00-{time+1}:00"
            context.bot.send_message(chat_id=chat_id, text=deleted_message)
            logger.info("Time slot deleted by %s on %s at %s:00",
                        name, day, time)
            return 'Success. \nPlease, notify other people in case of cancelation.'

        return 'You can not delete slots from previous days'

    @classmethod
    def get_list_day(self, day):
        listed = wks.get(self.days[day] + '3:' + self.days[day] + '16')
        output = '{}:\n'.format(day)
        for i in range(14):
            output += '{}:00 - {}:00  '.format(i + 9, i + 10)
            if i < len(listed):
                if not listed[i]:
                    output += ''
                else:
                    list_per = listed[i]
                    output += str(list_per[0])
            output += '\n'
        return output

    @classmethod
    def get_all_list(self):
        output = ''
        for day in self.days.keys():
            output += self.get_list_day(day)
            output += '\n'
        return output

    @classmethod
    def reset_list(self):
        sh.values_clear("'Расписание К006'!B3:H16")
        print("Executed")
        wks.update('C11', "Art Revolution")
        wks.update('C12', "Art Revolution")

        wks.update('E11', "Art Revolution")
        wks.update('E12', "Art Revolution")

        wks.update('G11', "Art Revolution")
        wks.update('G12', "Art Revolution")

        wks.update('B13', "Vocal club")
        wks.update('B14', "Vocal club")

        wks.update('D13', "Vocal club")
        wks.update('D14', "Vocal club")
