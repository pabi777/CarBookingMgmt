'''
Problem statement:

A customer should be able to book car (which is not assigned to anyone else) for specific period duration (such as
2 hours). The manager can add new cars, delete existing cars, view information for any cars
and update status for any cars (assigned or not assigned). The customer can request for car,
which will be reserved if the car is available fre in the workshop else appropriate message
will be displayed.
'''

from datetime import datetime, timedelta
import os
import pprint
from copy import deepcopy
pp = pprint.PrettyPrinter(indent=4)


class Frontdesk:
    added_car = False
    car_dict = {}

    def formatter(self, cardict):
        if cardict:
            temp = deepcopy(cardict)
            print(cardict)
            for item in temp:
                if temp[item]['duration']:
                    temp[item]['duration'] = temp[item]['duration'].strftime(
                        '%d-%m-%Y %H:%M:%S')
            return temp
        else:
            return cardict

    def single_formatter(self, item1):
        item = item1.copy()
        if item['duration']:
            item['duration'] = item['duration'].strftime(
                '%d-%m-%Y %H:%M:%S')
        return item

    def list_formatter(self, item1):
        item = deepcopy(item1)
        for i in item:
            if i['duration']:
                i['duration'] = i['duration'].strftime(
                    '%d-%m-%Y %H:%M:%S')
        return item


class Available_Maker:

    def __init__(self, frontdesk) -> None:
        self.frontdesk = frontdesk

    def checker(self):
        if self.frontdesk.added_car:
            for item in self.frontdesk.car_dict:
                if self.frontdesk.car_dict[item]['duration']:
                    if self.frontdesk.car_dict[item]['duration'] < datetime.now():
                        self.frontdesk.car_dict[item]['status'] = 'AVAILABLE'
                        self.frontdesk.car_dict[item]['duration'] = ''


class Customer(Available_Maker):

    def __init__(self, frontdesk) -> None:
        self.frontdesk = frontdesk
        self.username = str(input('Enter name: '))
        self.phone = str(input('Phone: '))
        if not self.username or (not len(self.phone)==10):
            print("invalid details...please provide valid username and phone number. Length of the phonenumber must be 10")
            self.__init__(frontdesk)
        super().__init__(frontdesk)

    def is_any_car_available(func):
        def inner(self, **kwargs):
            if self.frontdesk.car_dict:
                # if isinstance(self.IAM, Customer):
                func(self, **kwargs)
            else:
                print('No cars available in stock right now!!')
                return('No cars available in stock right now!!')
        return inner

    @is_any_car_available
    def show_car(self):
        if self.frontdesk.added_car:
            self.checker()
            cars = [
                self.frontdesk.car_dict[x] for x in self.frontdesk.car_dict if self.frontdesk.car_dict[x]['status'] == f'AVAILABLE']
            car_count = len(cars)
            pp.pprint(self.frontdesk.list_formatter(cars))
            print(f'\n{car_count} Car available \n')

    @is_any_car_available
    def request_car(self):
        is_available = True
        for i, car in enumerate(self.frontdesk.car_dict):
            if self.frontdesk.car_dict[car]['status'] == 'AVAILABLE' or self.frontdesk.car_dict[car]['duration'] < datetime.now():
                self.show_car()
                ch = str(
                    input('Do you want to book car? y/n: ')).lower()
                if ch == 'n':
                    is_available = True
                    break
                self.frontdesk.car_dict[car]['status'] = f'BOOKED to {self.username}'
                self.frontdesk.car_dict[car]['duration'] = datetime.now(
                )+timedelta(hours=int(os.getenv('time_duration', 2)))
            else:
                is_available = False

        if not is_available:
            print('Sorry! no car can be booked at this time..check again later')

    def booked_cars(self):
        self.checker()
        carlist = [self.frontdesk.car_dict[x]
                   for x in self.frontdesk.car_dict if self.frontdesk.car_dict[x]['status'] == f'BOOKED to {self.username}']
        print(self.frontdesk.list_formatter(carlist))

# Note: Assuming passkey is shared only among managers


class Manager():
    username, passkey = None, str(os.getenv('secret', 'secret'))


class Admin(Available_Maker):

    def __init__(self, IAM, frontdesk):
        self.IAM = IAM
        self.frontdesk = frontdesk
        super().__init__(frontdesk)

    def is_manager(func):
        def inner(self, **kwargs):
            if isinstance(self.IAM, Manager):
                func(self, **kwargs)
            else:
                print('Unauthorized Access')
        return inner

    @ is_manager
    def add_car(self):
        key = None
        i = 1000
        start = i
        while key != 'q':
            # Automatically generating registrarion number
            self.frontdesk.car_dict.update(
                {
                    f'WB {i}': {
                        'regnumber': f'WB {i}',
                        'name': f"CAR {(i-start)+1}",
                        # 2 hours rent time
                        'duration': '',
                        'status': 'AVAILABLE'
                    }
                })

            print(f'CAR {(i-start)+1} added')
            i += 1
            self.frontdesk.added_car = True
            key = str(
                input('Press q to stop adding or press Enter to add More car\n')).lower()

    @ is_manager
    def status_change(self):
        self.view_car()
        try:
            reg = str(
                input('Enter Car registrarion number to update status:')).upper()
            if reg not in self.frontdesk.car_dict:
                print('Try again..')
            else:
                self.frontdesk.car_dict[reg]['status'] = str(
                    input("Enter new status: Booked/Available: ")).upper()
        except:
            print('Try again.....')

    @ is_manager
    def remove_car(self):
        self.view_car()
        try:
            reg = str(input('Enter Car registrarion number to remove: ')).upper()
            if reg not in self.frontdesk.car_dict:
                print('Try again..')
            else:
                print("Removed car details: ", self.frontdesk.single_formatter(
                    self.frontdesk.car_dict.pop(reg)))
        except:
            print('Try again....')

    @ is_manager
    def view_car(self, has_reg_no=False):
        self.checker()
        if has_reg_no:
            try:
                reg_id = str(input('Enter reg number:')).upper()
                pp.pprint(self.frontdesk.single_formatter(
                    self.frontdesk.car_dict[reg_id]))
            except KeyError:
                print('No car found corrosponding resgistration number\n')
            except:
                # raise
                print("Try again\n")
        else:
            pp.pprint(self.frontdesk.formatter(self.frontdesk.car_dict))


if __name__ == "__main__":
    frontdesk = Frontdesk()
    while True:
        try:
            choice = int(input("1.Manager login 2.User Login 3.Exit\n"))
        except:
            choice = None
        if choice == 1:
            manager = Manager()
            username = str(input('Enter username: '))
            if not username:
                print('Please provide a username\n')
                continue
            manager.username = username
            passwd = str(input('Enter manager passkey: '))
            loggedin = False
            if passwd == manager.passkey:
                print('Login successfull')
                loggedin = True
            else:
                print("\nWrong password, Try again.......\n")
            if loggedin:
                key = None
                admin = Admin(manager, frontdesk)
                while key != 6:
                    try:
                        key = int(input(
                            "1.Add car 2.Change car status 3.Remove car 4.View all cars 5.View car by Registration number 6.Logout \n"))
                    except:
                        print('Wrong input..try again!!')

                    if key == 1:
                        admin.add_car()
                    elif key == 2:
                        admin.status_change()
                    elif key == 3:
                        admin.remove_car()
                    elif key == 4:
                        admin.view_car()
                    elif key == 5:
                        admin.view_car(has_reg_no=True)
        elif choice == 2:
            customer = Customer(frontdesk)
            while True:
                try:
                    cust_choice = int(
                        input("1.Show availabe car 2.Book car 3.Show booked car 4.Exit\n"))
                except:
                    cust_choice = None

                msg = ''
                if cust_choice == 1:
                    msg = customer.show_car()

                elif cust_choice == 2:
                    if not msg == 'No cars available in stock right now!!':
                        customer.request_car()
                    else:
                        print(msg)
                elif cust_choice == 3:
                    customer.booked_cars()
                elif cust_choice == 4:
                    break

        elif choice == 3:
            break
