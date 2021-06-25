'''
A customer should be able to book car (which is not assigned to anyone else) for specific period duration (such as
2 hours). The manager can add new cars, delete existing cars, view information for any cars
and update status for any cars (assigned or not assigned). The customer can request for car,
which will be reserved if the car is available fre in the workshop else appropriate message
will be displayed.
'''
from datetime import datetime, timedelta
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)


class Frontdesk:
    added_car = False
    car_dict = {}


class Customer():

    def __init__(self, frontdesk) -> None:
        self.frontdesk = frontdesk
        self.username = str(input('Enter name: '))
        self.phone = str(input('Phone: '))

    def is_customer(func):
        def inner(self, **kwargs):
            if isinstance(self, Customer):
                func(self, **kwargs)
            else:
                print('Unauthorized Access')
        return inner

    def is_any_car_available(func):
        def inner(self, **kwargs):
            if self.frontdesk.added_car:
                # if isinstance(self.IAM, Customer):
                func(self, **kwargs)
            else:
                return('No cars available in stock right now!!')
        return inner

    @is_any_car_available
    @is_customer
    def show_car(self):
        if self.frontdesk.added_car:
            pp.pprint(self.frontdesk.car_dict)

    @is_any_car_available
    @is_customer
    def request_car(self):
        is_available = False
        for car in self.frontdesk.car_dict:
            if self.frontdesk.car_dict[car]['status'] == 'AVAILABLE' or self.frontdesk.car_dict[car]['duration'] < datetime.now():
                self.frontdesk.car_dict[car]['status'] = f'BOOKED to {self.username}'
                self.frontdesk.car_dict[car]['duration'] = datetime.now(
                )+timedelta(hours=os.getenv('time_duration', 2))
                is_available = True

        if not is_available:
            print('Sorry! no car can be booked at this time..check again later')


# Note: Assuming passkey is shared only among managers


class Manager():
    username, passkey = None, str(os.getenv('secret', 'secret'))


class Admin():

    def __init__(self, IAM, frontdesk):
        self.IAM = IAM
        self.frontdesk = frontdesk

    def is_manager(func):
        def inner(self, **kwargs):
            if isinstance(self.IAM, Manager):
                func(self, **kwargs)
            else:
                print('Unauthorized Access')
        return inner

    @is_manager
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
                        'duration': datetime.now(),
                        'status': 'AVAILABLE'
                    }
                })

            print(f'CAR {(i-start)+1} added')
            i += 1
            self.frontdesk.added_car = True
            key = str(
                input('Press q to stop adding or press Enter to add More car\n')).lower()

    @is_manager
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

    @is_manager
    def remove_car(self):
        self.view_car()
        try:
            reg = str(input('Enter Car registrarion number to remove: ')).upper()
            if reg not in self.frontdesk.car_dict:
                print('Try again..')
            else:
                print("Removed car id: ", self.frontdesk.car_dict.pop(reg))
        except:
            print('Try again....')

    @is_manager
    def view_car(self, has_reg_no=False):
        if has_reg_no:
            try:
                reg_id = str(input('enter your reg number:')).upper()
                pp.pprint(self.frontdesk.car_dict[int(reg_id)])
            except KeyError:
                print('No car found corrosponding resgistration number\n')
            except:
                print("Try again\n")
        else:
            pp.pprint(self.frontdesk.car_dict)


if __name__ == "__main__":
    frontdesk = Frontdesk()
    while True:
        try:
            choice = int(input("1.Manager login 2.User Login 3.Exit\n"))
        except:
            choice = None
        if choice == 1:
            manager = Manager()
            manager.username = str(input('Enter username: '))
            passwd = str(input('Enter manager passkey: '))
            loggedin = False
            if passwd == manager.passkey:
                print('Login successfull')
                loggedin = True
            else:
                print("\nwrong password, Try again.......\n")
            if loggedin:
                key = None
                admin = Admin(manager, frontdesk)
                while key != 6:
                    try:
                        key = int(input(
                            "1.Add car 2.Change car status 3.Remove car 4.View all cars 5.View car by Registration number 6.Logout \n"))
                    except:
                        print('wrong input..try again!!')

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
            msg = customer.show_car()
            if not msg == 'No cars available in stock right now!!':
                customer.request_car()
            else:
                print(msg)
        elif choice == 3:
            break
