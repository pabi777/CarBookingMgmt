'''
A customer should be able to book car (which is not assigned to anyone else) for specific period duration (such as
2 hours). The manager can add new cars, delete existing cars, view information for any cars
and update status for any cars (assigned or not assigned). The customer can request for car,
which will be reserved if the car is available fre in the workshop o else appropriate message
will be displayed.


'''

import pprint

pp = pprint.PrettyPrinter(indent=4)
car_dict = {}


class Customer:
    username = None

# Assuming passkey is shared only among managers


class Manager:
    username, passkey = None, '1234'


class Admin:
    def is_manager(self, IAM):
        return True if isinstance(IAM, Manager) else False

    def add_car(self, IAM):
        if not self.is_manager(IAM):
            return 'Unauthorized'

        key = None
        i = 1
        while key != 'q':
            # Automatically generating registrarion number
            car_dict.update(
                {
                    i: {
                        'regnumber': i,
                        'name': f"CAR {i}",
                        # 2 hours rent time
                        'duration': 2,
                        'status': 'AVAILABLE'
                    }
                })

            print(f'car{i} added')
            i += 1
            key = str(input('Press q to stop adding or any key to continue\n'))

    def status_change(self, IAM):
        if not self.is_manager(IAM):
            return 'Unauthorized'
        self.view_car(IAM)
        reg = int(input('Enter Car registrarion number to update status:'))
        if reg not in car_dict:
            pp.pprint('Try again..')
        else:
            car_dict[reg]['status'] = str(
                input("Enter new status: Booked/Available: ")).upper()

    def remove_car(self, IAM):
        if not self.is_manager(IAM):
            return 'Unauthorized'
        self.view_car(IAM)
        reg = int(input('Enter Car registrarion number to remove: '))
        if reg not in car_dict:
            pp.pprint('Try again..')
        else:
            print("Removed car id: ", car_dict.pop(reg))

    def view_car(self, IAM, reg_id=None):
        if not self.is_manager(IAM):
            return 'Unauthorized'
        if reg_id:
            try:
                pp.pprint(car_dict[int(reg_id)])
            except KeyError:
                pp.pprint('No car found corrosponding resgistration number')
        else:
            pp.pprint(car_dict)


class Booking:
    customer = Customer()
    pp.pprint(isinstance(customer, Customer))


if __name__ == "__main__":
    #
    choice = int(input("1.Manager login 2.User Login\n"))
    if choice == 1:
        manager = Manager()
        manager.username = str(input('Enter username: '))
        passwd = str(input('Enter manager passkey: '))
        loggedin = False
        if passwd == manager.passkey:
            pp.pprint('Login successfull')
            loggedin = True
        else:
            pp.pprint("wrong password, Exiting.......")
        if loggedin:
            key = None
            admin = Admin()
            while key != 6:
                key = int(input(
                    "1.Add car 2.Change car status 3.Remove car 4.View all cars 5.View car by Registration number 6.exit\n"))
                if key == 1:
                    admin.add_car(manager)
                elif key == 2:
                    admin.status_change(manager)
                elif key == 3:
                    admin.remove_car(manager)
                elif key == 4:
                    admin.view_car(manager)
                elif key == 5:
                    reg = int(input('enter your reg number:'))
                    admin.view_car(manager, reg)
