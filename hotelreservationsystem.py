import sys
from datetime import date, timedelta

STAFF_PASSWORD = "staff123"
ALLOWED_EMAILS = ["@gmail.com", "@yahoo.com", "@outlook.com", "@icloud.com", "@hotmail.com"]

ROOM_TYPES = ["Standard", "Deluxe", "Suite"]
MAX_TOTAL_GUESTS = 35
MAX_ROOMS = 5

rooms = [
    {"number": 100, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 101, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 102, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 103, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 104, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 105, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 106, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 107, "type": "Standard", "price": 1000, "max_guests": 3, "status": "AVAILABLE"},
    {"number": 200, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 201, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 202, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 203, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 204, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 205, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 206, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 207, "type": "Deluxe", "price": 2500, "max_guests": 5, "status": "AVAILABLE"},
    {"number": 300, "type": "Suite", "price": 5000, "max_guests": 7, "status": "AVAILABLE"},
    {"number": 301, "type": "Suite", "price": 5000, "max_guests": 7, "status": "AVAILABLE"},
    {"number": 302, "type": "Suite", "price": 5000, "max_guests": 7, "status": "AVAILABLE"},
    {"number": 303, "type": "Suite", "price": 5000, "max_guests": 7, "status": "AVAILABLE"},
]

reservations = []
payments = []


def ask_number(ask, low, high, allow_back=False):
    while True:
        text = input(ask).strip()
        if allow_back and text.lower() == "back":
            return None
        if not text.isdecimal():
            print("Invalid input! Please enter numbers only.")
        else:
            number = int(text)
            if number >= low and number <= high:
                return number
            print(f"Please enter a number between {low} and {high}.")


def format_date(d):
    return d.strftime("%B %d, %Y")


def days_in_month(year, month):
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        return 28
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    return 31


def is_valid_email(email):
    if " " in email or email.count("@") != 1:
        return False
    name, domain = email.split("@")
    if name == "" or name.startswith(".") or name.endswith(".") or ".." in name:
        return False
    for letter in name:
        if not (letter.isalnum() or letter in "._-+"):
            return False
    return "@" + domain in ALLOWED_EMAILS


def find_room(room_number):
    for room in rooms:
        if room["number"] == room_number:
            return room
    return None


def find_booking(booking_id):
    for res in reservations:
        if res["id"] == booking_id:
            return res
    return None


def is_room_free(room_number, start, end, skip_id=""):
    for res in reservations:
        if res["id"] == skip_id:
            continue
        if res["room"] == room_number and (res["status"] == "CONFIRMED" or res["status"] == "CHECKED-IN"):
            if start < res["check_out"] and end > res["check_in"]:
                return False
    return True


def show_booking(res):
    room = find_room(res["room"])
    print(f"Booking ID: {res['id']}")
    print(f"Guest Name: {res['name']}")
    print(f"Contact Number: {res['contact']}")
    print(f"Email Address: {res['email']}")
    print(f"Check-in Date: {format_date(res['check_in'])}")
    print(f"Check-out Date: {format_date(res['check_out'])}")
    print(f"Guests: {res['guests']}")
    print(f"Room: {res['room']} ({room['type']})")
    print(f"Cost: {res['nights']} night(s) x ₱{room['price']} = ₱{res['total']}")
    print(f"Payment Status: {res['payment_status']}")
    print(f"Amount Paid: ₱{res['paid']} via {res['pay_method']} (Ref: {res['pay_ref']})")
    print(f"Booking Status: {res['status']}")
    if res["group"] != "none":
        print(f"Same Reservation As: {res['group']}")


def get_dates():
    print("\n--- CHECK-IN & CHECK-OUT DATES ---")
    today = date.today()
    while True:
        month = ask_number("Enter Check-in Month (1-12): ", 1, 12, True)
        if month is None:
            return None
        day = ask_number("Enter Check-in Day (1-31): ", 1, 31, True)
        if day is None:
            return None

        if day > days_in_month(today.year, month):
            print("Invalid calendar date! Please try again.")
            continue

        check_in = date(today.year, month, day)

        if check_in < today:
            print(f"\n{format_date(check_in)} has already passed.")
            print("1. Book for next year instead")
            print("2. Enter a different date")
            if ask_number("Enter choice (1-2): ", 1, 2) == 2:
                continue
            if day > days_in_month(today.year + 1, month):
                print("That date does not exist next year. Please try again.")
                continue
            check_in = date(today.year + 1, month, day)

        break

    nights = ask_number("How many nights will you stay? ", 1, 30, True)
    if nights is None:
        return None
    check_out = check_in + timedelta(days=nights)
    print(f"Check-in: {format_date(check_in)}  |  Check-out: {format_date(check_out)}")
    return check_in, check_out, nights


def show_rooms(room_type):
    print(f"\n--- {room_type.upper()} ROOMS ---")

    total_rooms = 0
    sample = None
    for room in rooms:
        if room["type"] == room_type:
            total_rooms += 1
            sample = room

    today = date.today()
    free_tonight = len(get_free_rooms(room_type, today, today + timedelta(days=1), ""))

    print(f"Price: ₱{sample['price']} / night")
    print(f"Max Guests per Room: {sample['max_guests']}")
    print(f"Total Rooms: {total_rooms}")
    print(f"Available Tonight: {free_tonight} of {total_rooms}")

    has_booking = False
    for res in reservations:
        res_room = find_room(res["room"])
        if res_room["type"] == room_type and (res["status"] == "CONFIRMED" or res["status"] == "CHECKED-IN") and res["check_out"] > today:
            if not has_booking:
                print("\nUpcoming booked dates (1 room each):")
                has_booking = True
            print(f"  - {format_date(res['check_in'])} to {format_date(res['check_out'])}")

    print()
    input("Press Enter to go back...")


def get_free_rooms(room_type, start, end, skip_id):
    free = []
    for room in rooms:
        if room["type"] == room_type and is_room_free(room["number"], start, end, skip_id):
            free.append(room)
    return free


def choose_room_type(check_in, check_out, guests_per_room, rooms_needed, skip_id):
    print(f"\n--- ROOM AVAILABILITY ({format_date(check_in)} to {format_date(check_out)}) ---")
    available = []

    for room_type in ROOM_TYPES:
        sample = None
        for room in rooms:
            if room["type"] == room_type:
                sample = room
                break

        left = len(get_free_rooms(room_type, check_in, check_out, skip_id))
        if sample["max_guests"] < guests_per_room:
            status = f"[TOO SMALL - max {sample['max_guests']} guests per room]"
        elif left == 0:
            status = "[FULLY BOOKED]"
        elif left < rooms_needed:
            status = f"[NOT ENOUGH ROOMS - only {left} left]"
        else:
            status = f"[AVAILABLE - {left} room(s) left]"
            available.append(room_type)
        print(f"{room_type} Room (₱{sample['price']}/night, max {sample['max_guests']} guests) -> {status}")

    if len(available) == 0:
        print("\nSorry! No room is available for your dates, guests, and rooms.")
        return None

    print("\n--- SELECT A ROOM TYPE ---")
    number = 1
    for room_type in available:
        print(f"{number}. {room_type} Room")
        number += 1

    print(f"{number}. Go Back")

    choice = ask_number(f"Select a room type (1-{number}): ", 1, number)
    if choice == number:
        print("\nGoing back. No room was selected.")
        return None
    return available[choice - 1]


def ask_card():
    while True:
        cardholder = input("Enter Name on Card: ").strip()
        if cardholder.lower() == "back":
            return None
        letters = cardholder.replace(" ", "").replace(".", "").replace("'", "").replace("-", "")
        if len(cardholder) >= 2 and letters.isalpha():
            break
        print("Invalid name! Use letters only.")

    while True:
        number = input("Enter 16-digit Card Number: ").replace(" ", "")
        if number.lower() == "back":
            return None
        if number.isdecimal() and len(number) == 16:
            break
        print("Invalid card number! It must be 16 digits.")

    while True:
        cvv = input("Enter 3-digit CVV: ").strip()
        if cvv.lower() == "back":
            return None
        if cvv.isdecimal() and len(cvv) == 3:
            break
        print("Invalid CVV! It must be 3 digits.")

    return [cardholder.upper(), number]


def ask_wallet(method):
    while True:
        number = input(f"Enter your {method} Number (11 digits starting with 09): ").strip()
        if number.lower() == "back":
            return None
        if number.isdecimal() and len(number) == 11 and number.startswith("09"):
            return number
        print("Invalid number! Must be 11 digits and start with '09'.")


def take_payment(amount):
    print(f"\nAmount to pay: ₱{amount}")
    print("(You can type 'back' on any question to return to the payment methods.)")
    while True:
        print("\n--- PAYMENT METHOD ---")
        print("1. Debit/Credit Card")
        print("2. GCash/Maya")
        print("3. Cancel Payment")
        choice = ask_number("Enter choice (1-3): ", 1, 3)
        if choice == 3:
            return []

        cardholder = ""
        if choice == 1:
            method = "Debit/Credit Card"
            details = ask_card()
            if details is None:
                continue
            cardholder = details[0]
            number = details[1]
        else:
            method = "GCash/Maya"
            number = ask_wallet(method)
            if number is None:
                continue
        break

    reference = "PAY-" + str(len(payments) + 1).zfill(4)
    payments.append(reference)
    pay_method = f"{method} (ending {number[-4:]})"

    print("\n--- PAYMENT RECEIPT ---")
    print(f"Reference: {reference}")
    print(f"Method: {pay_method}")
    if cardholder != "":
        print(f"Cardholder: {cardholder}")
    print(f"Amount Paid: ₱{amount}")
    print("Payment successful!")

    return [pay_method, reference]


def make_reservation():
    print("\n--- MAKE A RESERVATION ---")
    print("(You can type 'back' on any question to return to the menu.)")

    dates = get_dates()
    if dates is None:
        return False
    check_in = dates[0]
    check_out = dates[1]
    nights = dates[2]

    guests = ask_number("Number of Guests: ", 1, MAX_TOTAL_GUESTS, True)
    if guests is None:
        return False

    while True:
        rooms_needed = ask_number("Number of Rooms: ", 1, MAX_ROOMS, True)
        if rooms_needed is None:
            return False
        if rooms_needed <= guests:
            break
        print("You cannot book more rooms than guests.")

    guests_per_room = guests // rooms_needed
    if guests % rooms_needed != 0:
        guests_per_room += 1

    room_type = choose_room_type(check_in, check_out, guests_per_room, rooms_needed, "")
    if room_type is None:
        input("\nPress Enter to return to menu...")
        return False

    print("\nPlease enter your details.")

    while True:
        name = input("Enter Guest Name (First and Last Name): ").strip()
        if name.lower() == "back":
            return False
        letters = name.replace(" ", "").replace(".", "").replace("'", "").replace("-", "")
        if " " in name and letters.isalpha():
            break
        print("Invalid name! Enter BOTH first and last name, letters only.")
    name = name.title()

    while True:
        while True:
            contact = input("Enter Contact Number (11 digits starting with 09, or 'none'): ").strip().lower()
            if contact == "back":
                return False
            if contact == "none":
                break
            if contact.isdecimal() and len(contact) == 11 and contact.startswith("09"):
                break
            print("Invalid contact! Must be 11 digits and start with '09'.")

        while True:
            email = input("Enter Email Address (or 'none'): ").strip().lower()
            if email == "back":
                return False
            if email == "none":
                break
            if is_valid_email(email):
                break
            print("Invalid email! Must end with @gmail.com, @yahoo.com, @outlook.com, @icloud.com, or @hotmail.com.")

        if contact == "none" and email == "none":
            print("\n[Error] Provide AT LEAST a contact number OR an email.\n")
        else:
            break

    free_rooms = get_free_rooms(room_type, check_in, check_out, "")
    new_bookings = []
    count = 0

    while count < rooms_needed:
        room = free_rooms[count]
        guests_here = guests // rooms_needed
        if count < guests % rooms_needed:
            guests_here += 1
        count += 1

        new_bookings.append({
            "id": "M2-" + str(len(reservations) + count).zfill(4),
            "name": name,
            "contact": contact,
            "email": email,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "guests": guests_here,
            "room": room["number"],
            "total": room["price"] * nights,
            "status": "CONFIRMED",
            "payment_status": "UNPAID",
            "paid": 0,
            "pay_method": "none",
            "pay_ref": "none",
            "refund_to": "none",
            "group": "none",
        })

    print("\n--- RESERVATION SUMMARY ---")
    grand_total = 0
    for booking in new_bookings:
        show_booking(booking)
        grand_total += booking["total"]
        print("-" * 30)
    if len(new_bookings) > 1:
        print(f"{len(new_bookings)} rooms booked for {guests} guests. Each room has its own Booking ID.")
    print(f"Total to pay: ₱{grand_total}")

    print("\n1. Proceed to Payment")
    print("2. Cancel")
    if ask_number("Enter choice (1-2): ", 1, 2) == 2:
        print("\nReservation cancelled. No payment was made.")
        input("\nPress Enter to return to menu...")
        return False

    payment = take_payment(grand_total)
    if len(payment) == 0:
        print("\nPayment cancelled. Your booking was not saved.")
        input("\nPress Enter to return to menu...")
        return False

    for booking in new_bookings:
        others = []
        for other in new_bookings:
            if other["id"] != booking["id"]:
                others.append(other["id"])
        if len(others) > 0:
            booking["group"] = ", ".join(others)
        booking["pay_method"] = payment[0]
        booking["pay_ref"] = payment[1]
        booking["refund_to"] = payment[0]
        booking["paid"] = booking["total"]
        booking["payment_status"] = "PAID"
        reservations.append(booking)

    if len(new_bookings) == 1:
        print(f"\nReservation Confirmed! Your booking ID is {new_bookings[0]['id']}.")
    else:
        print("\nReservation Confirmed! Your booking IDs are:")
        for booking in new_bookings:
            print(f"  {booking['id']} - Room {booking['room']} ({booking['guests']} guest(s))")
    print("Please keep your booking ID(s). You need them (and your contact/email) to manage your booking.")

    print("\n--- WHAT WOULD YOU LIKE TO DO NEXT? ---")
    print("1. Back to Main Menu")
    print("2. Exit")
    choice = ask_number("Enter choice (1-2): ", 1, 2)
    if choice == 2:
        print("\nThank you for visiting Celinó Hotel.")
        print("Hope to see you again!")
        sys.exit()
    return True


def ask_booking_id():
    while True:
        search_id = input("Enter Booking ID (e.g., M2-0001): ").strip().upper()
        if search_id == "BACK":
            return "back"
        booking = find_booking(search_id)
        if booking is not None:
            return booking
        print("\nBooking ID not found. Please try again.\n")


def find_my_booking():
    booking = ask_booking_id()
    if booking == "back":
        return "back"

    for attempt in range(3):
        proof = input("Enter the contact number or email used for this booking: ").strip().lower()
        if proof == "back":
            return "back"
        if proof != "none" and (proof == booking["contact"] or proof == booking["email"]):
            return booking
        print(f"\nDetails do not match this booking. Attempts left: {2 - attempt}\n")

    print("Verification failed. Too many wrong tries.")
    return None


def pay_or_refund(booking, new_total):
    difference = new_total - booking["paid"]

    if difference > 0:
        print(f"\nThe new total is ₱{new_total}. You need to pay an extra ₱{difference}.")
        print("1. Pay Extra Amount")
        print("2. Keep My Original Booking")
        if ask_number("Enter choice (1-2): ", 1, 2) == 2:
            return False

        payment = take_payment(difference)
        if len(payment) == 0:
            print("\nPayment cancelled.")
            return False
        booking["pay_method"] = payment[0]
        booking["pay_ref"] = payment[1]
        booking["paid"] = new_total
    elif difference < 0:
        print(f"\nThe new total is ₱{new_total}. ₱{-difference} will be refunded to {booking['refund_to']}.")
        booking["paid"] = new_total

    return True


def cancel_booking(booking):
    if booking["status"] != "CONFIRMED":
        print(f"\nCannot cancel. This booking is {booking['status']}.")
        return

    days_left = (booking["check_in"] - date.today()).days
    print("\nCancellation policy: full refund if you cancel 3 or more days before check-in.")
    print("If you cancel later than that, there is NO refund.")

    if days_left >= 3:
        print(f"Your check-in is {days_left} days away, so you get a full refund of ₱{booking['paid']}.")
    else:
        print(f"Your check-in is too close, so ₱{booking['paid']} will NOT be refunded.")

    if input("\nType 'yes' to cancel this booking: ").strip().lower() != "yes":
        print("\nCancellation stopped. Your booking is still active.")
        return

    booking["status"] = "CANCELLED"
    print("\nReservation CANCELLED. The room is now available again.")
    if days_left >= 3:
        print(f"Full refund of ₱{booking['paid']} will be sent to {booking['refund_to']}.")
        booking["payment_status"] = "REFUNDED"
        booking["paid"] = 0
    else:
        print(f"No refund. ₱{booking['paid']} is non-refundable.")
        booking["payment_status"] = "NON-REFUNDABLE"


def change_booking(booking):
    if booking["status"] == "CHECKED-IN":
        print("\nYou cannot change a booking after check-in.")
        return
    if booking["status"] != "CONFIRMED":
        print(f"\nCannot change this booking. Its status is {booking['status']}.")
        return

    days_left = (booking["check_in"] - date.today()).days
    if days_left < 3:
        print("\nChanges are only allowed 3 or more days before check-in.")
        print("Your check-in is too close to change this booking.")
        return

    print("\n1. Change Dates")
    print("2. Change Room Type")
    print("3. Go Back")
    choice = ask_number("Enter choice (1-3): ", 1, 3)

    old_room = find_room(booking["room"])

    if choice == 1:
        print("\n(You can type 'back' on any question to cancel the change.)")
        while True:
            dates = get_dates()
            if dates is None:
                print("\nNothing was changed.")
                return
            if (dates[0] - date.today()).days >= 3:
                break
            print("\nThe new check-in date must be at least 3 days from today. Please choose another date.")
        check_in = dates[0]
        check_out = dates[1]
        nights = dates[2]

        free_rooms = get_free_rooms(old_room["type"], check_in, check_out, booking["id"])
        if len(free_rooms) == 0:
            print("\nSorry, no room of your type is available for those dates. Nothing was changed.")
            return

        new_room = free_rooms[0]
        if old_room in free_rooms:
            new_room = old_room

        new_total = new_room["price"] * nights

        if not pay_or_refund(booking, new_total):
            print("\nNothing was changed.")
            return

        booking["room"] = new_room["number"]
        booking["check_in"] = check_in
        booking["check_out"] = check_out
        booking["nights"] = nights
        booking["total"] = new_total

        print("\nDates updated!")
        show_booking(booking)

    elif choice == 2:
        room_type = choose_room_type(booking["check_in"], booking["check_out"], booking["guests"], 1, booking["id"])
        if room_type is None:
            print("Nothing was changed.")
            return

        free_rooms = get_free_rooms(room_type, booking["check_in"], booking["check_out"], booking["id"])
        new_room = free_rooms[0]
        if old_room in free_rooms:
            new_room = old_room

        if new_room["number"] == old_room["number"]:
            print(f"\nYou are already booked in a {old_room['type']} room. Nothing was changed.")
            return

        new_total = new_room["price"] * booking["nights"]

        if not pay_or_refund(booking, new_total):
            print("\nNothing was changed.")
            return

        booking["room"] = new_room["number"]
        booking["total"] = new_total

        print("\nRoom updated!")
        show_booking(booking)


def view_all_reservations():
    print("\n--- ALL RESERVATIONS ---")
    if len(reservations) == 0:
        print("No reservations yet.")
    else:
        income = 0
        for res in reservations:
            show_booking(res)
            print("-" * 30)
            income += res["paid"]
        print(f"Total reservations: {len(reservations)}")
        print(f"Total income (payments received): ₱{income}")
    input("\nPress Enter to continue...")


def staff_manage_reservation():
    while True:
        print("\n--- STAFF: MANAGE A RESERVATION ---")
        booking = ask_booking_id()
        if booking == "back":
            return

        print("\n--- RESERVATION DETAILS ---")
        show_booking(booking)

        print("\n1. Change Dates or Room")
        print("2. Cancel Reservation")
        print("3. Go Back")
        manage_choice = ask_number("Enter choice (1-3): ", 1, 3)
        if manage_choice == 1:
            change_booking(booking)
            input("\nPress Enter to continue...")
        elif manage_choice == 2:
            cancel_booking(booking)
            input("\nPress Enter to continue...")


def check_in_guest():
    print("\n--- CHECK-IN ---")
    booking = ask_booking_id()
    if booking == "back":
        return

    if booking["status"] != "CONFIRMED":
        print(f"\nCannot check in. This booking is {booking['status']}.")
    elif date.today() >= booking["check_out"]:
        print("\nThis booking has already ended.")
    elif date.today() < booking["check_in"]:
        print(f"\nToo early. Check-in date is {format_date(booking['check_in'])}.")
    else:
        room = find_room(booking["room"])
        if room["status"] != "AVAILABLE":
            print(f"\nRoom {room['number']} is not ready yet (status: {room['status']}).")
            for other in rooms:
                if other["type"] == room["type"] and other["status"] == "AVAILABLE" and is_room_free(other["number"], booking["check_in"], booking["check_out"], booking["id"]):
                    print(f"Moving the guest to Room {other['number']} (same type) instead.")
                    booking["room"] = other["number"]
                    room = other
                    break

        if room["status"] != "AVAILABLE":
            print("No other ready room of the same type. Please try again later.")
        else:
            booking["status"] = "CHECKED-IN"
            room["status"] = "OCCUPIED"
            print(f"\n{booking['name']} is now CHECKED-IN to Room {room['number']}.")
    input("\nPress Enter to continue...")


def check_out_guest():
    print("\n--- CHECK-OUT ---")
    booking = ask_booking_id()
    if booking == "back":
        return

    if booking["status"] != "CHECKED-IN":
        print(f"\nCannot check out. This booking is {booking['status']}.")
    else:
        room = find_room(booking["room"])
        booking["status"] = "CHECKED-OUT"
        room["status"] = "CLEANING"
        print(f"\n{booking['name']} is now CHECKED-OUT.")
        print(f"Room {room['number']} needs CLEANING.")
    input("\nPress Enter to continue...")


def mark_no_show():
    print("\n--- MARK AS NO-SHOW ---")
    booking = ask_booking_id()
    if booking == "back":
        return

    if booking["status"] != "CONFIRMED":
        print(f"\nCannot mark as no-show. This booking is {booking['status']}.")
    elif date.today() <= booking["check_in"]:
        print(f"\nToo early. The guest can still arrive until the end of {format_date(booking['check_in'])}.")
    else:
        booking["status"] = "NO-SHOW"
        booking["payment_status"] = "NON-REFUNDABLE"
        print(f"\n{booking['name']} is marked as NO-SHOW.")
        print(f"The room is free again. ₱{booking['paid']} is kept (non-refundable).")
    input("\nPress Enter to continue...")


def view_room_status():
    print("\n--- ROOM STATUS ---")
    for room in rooms:
        line = f"Room {room['number']} ({room['type']}): {room['status']}"
        for res in reservations:
            if res["room"] == room["number"] and res["status"] == "CHECKED-IN":
                line += f" - {res['name']} ({res['id']})"
        print(line)
    input("\nPress Enter to continue...")


def mark_room_clean():
    cleaning = []
    for room in rooms:
        if room["status"] == "CLEANING":
            cleaning.append(room)

    if len(cleaning) == 0:
        print("\nNo rooms need cleaning.")
    else:
        print("\n--- ROOMS NEEDING CLEANING ---")
        number = 1
        for room in cleaning:
            print(f"{number}. Room {room['number']} ({room['type']})")
            number += 1

        clean_choice = ask_number(f"Select a room (1-{len(cleaning)}): ", 1, len(cleaning))
        chosen = cleaning[clean_choice - 1]
        chosen["status"] = "AVAILABLE"
        print(f"\nRoom {chosen['number']} is now AVAILABLE.")
    input("\nPress Enter to continue...")


def main():
    while True:
        print("\n==============================")
        print("   WELCOME TO CELINÓ HOTEL    ")
        print("==============================")
        print("1. View Rooms / Make Reservation")
        print("2. Manage My Reservation")
        print("3. Hotel Information")
        print("4. Staff Area")
        print("5. Exit")

        choice = ask_number("Enter choice (1-5): ", 1, 5)

        if choice == 1:
            while True:
                print("\n--- ROOMS AND RESERVATION ---")
                print("1. View Standard Rooms")
                print("2. View Deluxe Rooms")
                print("3. View Suite Rooms")
                print("4. Make a Reservation")
                print("5. Back to Main Menu")

                room_choice = ask_number("Enter choice (1-5): ", 1, 5)
                if room_choice == 1:
                    show_rooms("Standard")
                elif room_choice == 2:
                    show_rooms("Deluxe")
                elif room_choice == 3:
                    show_rooms("Suite")
                elif room_choice == 4:
                    if make_reservation():
                        break
                else:
                    break

        elif choice == 2:
            print("\n(You can type 'back' on any question to return to the Manage menu.)")
            while True:
                print("\n--- MANAGE MY RESERVATION ---")
                print("1. Search Reservation by Booking ID")
                print("2. Change Dates or Room")
                print("3. Cancel Reservation")
                print("4. Back to Main Menu")

                manage_choice = ask_number("Enter choice (1-4): ", 1, 4)
                if manage_choice == 4:
                    break

                booking = find_my_booking()
                if booking == "back":
                    continue
                if booking is not None:
                    print("\n--- RESERVATION DETAILS ---")
                    show_booking(booking)

                    if manage_choice == 2:
                        change_booking(booking)
                    elif manage_choice == 3:
                        cancel_booking(booking)

                input("\nPress Enter to return to Manage Menu...")

        elif choice == 3:
            print("\n--- HOTEL INFORMATION ---")
            print("Hotel Name: Celinó Hotel")
            print("Address: km.30 National Road, Tunasan, Muntinlupa")
            print("Contact Number: 09123456789")
            print("Email: celinohotel@gmail.com")
            input("\nPress Enter to go back to Main Menu...")

        elif choice == 4:
            print("\n--- STAFF LOGIN ---")
            print("(You can type 'back' to return to the Main Menu.)")
            logged_in = False
            went_back = False
            for attempt in range(3):
                password = input("Enter staff password: ")
                if password.strip().lower() == "back":
                    went_back = True
                    break
                if password == STAFF_PASSWORD:
                    logged_in = True
                    break
                print(f"Wrong password. Attempts left: {2 - attempt}")

            if went_back:
                print("\nGoing back to the Main Menu.")
            elif not logged_in:
                input("\nAccess denied. Press Enter to return...")
            else:
                print("\n(You can type 'back' on any Booking ID question to return to the Staff Menu.)")
                while True:
                    print("\n--- STAFF MENU ---")
                    print("1. View All Reservations")
                    print("2. Manage a Reservation")
                    print("3. Check-in a Guest")
                    print("4. Check-out a Guest")
                    print("5. Mark a No-Show")
                    print("6. View Room Status")
                    print("7. Mark Room as Clean")
                    print("8. Back to Main Menu")

                    staff_choice = ask_number("Enter choice (1-8): ", 1, 8)

                    if staff_choice == 1:
                        view_all_reservations()

                    elif staff_choice == 2:
                        staff_manage_reservation()

                    elif staff_choice == 3:
                        check_in_guest()

                    elif staff_choice == 4:
                        check_out_guest()

                    elif staff_choice == 5:
                        mark_no_show()

                    elif staff_choice == 6:
                        view_room_status()

                    elif staff_choice == 7:
                        mark_room_clean()

                    else:
                        break

        else:
            break


try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\n\nProgram stopped.")

print("\nThank you for visiting Celinó Hotel.")
print("Hope to see you again!")
