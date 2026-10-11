import os
import re
import sys
import textwrap
from datetime import date, timedelta

# ======================================================================
#  DESIGN SETTINGS  (change these to restyle the whole program)
# ======================================================================
WIDTH = 66             # total width of every box
MARGIN = "  "          # empty space on the left of everything
CLEAR_SCREEN = True    # clear the screen whenever a new screen opens

os.system("")          # lets Windows terminals display colors

RESET = "\033[0m"
GOLD = "\033[38;5;178m"
BRIGHT_GOLD = "\033[1;38;5;220m"
CREAM = "\033[38;5;230m"
GREY = "\033[38;5;243m"
GREEN = "\033[38;5;114m"
RED = "\033[38;5;167m"
BLUE = "\033[38;5;110m"
ORANGE = "\033[38;5;215m"

STATUS_COLORS = {
    "CONFIRMED": GREEN, "CHECKED-IN": BLUE, "CHECKED-OUT": GREY,
    "CANCELLED": RED, "NO-SHOW": ORANGE,
    "PAID": GREEN, "UNPAID": ORANGE, "REFUNDED": BLUE, "NON-REFUNDABLE": RED,
    "AVAILABLE": GREEN, "OCCUPIED": RED, "CLEANING": ORANGE,
}

INNER = WIDTH - 4      # usable space inside a box
ANSI = re.compile(r"\033\[[0-9;]*m")

# ======================================================================
#  HOTEL DATA  (same as before)
# ======================================================================
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


# ======================================================================
#  DESIGN TOOLS  (everything that draws on the screen lives here)
# ======================================================================
def visible_len(text):
    """Length of the text as seen on screen (color codes take no space)."""
    return len(ANSI.sub("", text))


def pad(text, width, align="left"):
    gap = max(0, width - visible_len(text))
    if align == "center":
        left = gap // 2
        return " " * left + text + " " * (gap - left)
    if align == "right":
        return " " * gap + text
    return text + " " * gap


def out(text=""):
    print(MARGIN + text)


def blank():
    print()


def clear_screen():
    if CLEAR_SCREEN and sys.stdout.isatty():
        print("\033[2J\033[H", end="")


def money(amount):
    return f"₱{amount:,}"


def badge(status):
    color = STATUS_COLORS.get(status, CREAM)
    return f"{color}● {status}{RESET}"


# ---------- messages ----------
def _message(color, icon, text):
    lines = textwrap.wrap(text, WIDTH - 4) or [""]
    out(f"{color}{icon} {lines[0]}{RESET}")
    for extra in lines[1:]:
        out(f"{color}  {extra}{RESET}")


def ok(text):
    _message(GREEN, "✔", text)


def error(text):
    _message(RED, "✖", text)


def warn(text):
    _message(ORANGE, "▲", text)


def info(text):
    _message(BLUE, "◆", text)


def tip(text):
    _message(GREY, "✧", f"({text})")


# ---------- boxes ----------
def box_top(title=""):
    if title == "":
        out(f"{GOLD}╔{'═' * (WIDTH - 2)}╗{RESET}")
        return
    label = f" {title} "
    rest = WIDTH - 5 - len(label)
    out(f"{GOLD}╔═══{BRIGHT_GOLD}{label}{GOLD}{'═' * rest}╗{RESET}")


def box_bottom():
    out(f"{GOLD}╚{'═' * (WIDTH - 2)}╝{RESET}")


def box_divider():
    out(f"{GOLD}╠{'═' * (WIDTH - 2)}╣{RESET}")


def box_thin():
    out(f"{GOLD}║ {GREY}{'─' * INNER}{GOLD} ║{RESET}")


def box_row(text="", align="left"):
    out(f"{GOLD}║{RESET} {pad(text, INNER, align)} {GOLD}║{RESET}")


def box_text(text, color=CREAM):
    for piece in textwrap.wrap(text, INNER):
        box_row(f"{color}{piece}{RESET}")


def kv_row(label, value, value_color=CREAM):
    """A row like:  Guest Name ........ Juan Dela Cruz"""
    value = str(value)
    plain = "\033" not in value
    if plain:
        room = INNER - len(label) - 4
        if len(value) > room:
            value = value[:room - 1] + "…"
        shown = f"{value_color}{value}{RESET}"
    else:
        shown = value
    dots = max(1, INNER - len(label) - visible_len(shown) - 2)
    box_row(f"{GREY}{label} {'·' * dots}{RESET} {shown}")


# ---------- screens and menus ----------
def banner():
    clear_screen()
    blank()
    box_top()
    box_row()
    box_row(f"{GOLD}✦   ✦   ✦   ✦   ✦", "center")
    box_row()
    box_row(f"{BRIGHT_GOLD}C E L I N Ó     H O T E L", "center")
    box_row(f"{GOLD}──────────  ★ ★ ★ ★ ★  ──────────", "center")
    box_row()
    box_row(f"{GREY}km.30 National Road  ·  Tunasan  ·  Muntinlupa", "center")
    box_row()
    box_bottom()


def screen(title):
    """Opens a new screen with a gold title bar."""
    clear_screen()
    blank()
    out(f"{GOLD}✦ CELINÓ HOTEL  {GREY}│  {BRIGHT_GOLD}{title}{RESET}")
    out(f"{GOLD}{'━' * WIDTH}{RESET}")
    blank()


def section(title, step=""):
    """A smaller heading inside a screen."""
    blank()
    extra = f"   {GREY}{step}{RESET}" if step else ""
    out(f"{BRIGHT_GOLD}✦ {title}{RESET}{extra}")
    out(f"{GREY}{'─' * WIDTH}{RESET}")


def show_menu(title, options):
    box_top(title)
    box_row()
    for number, text in enumerate(options, start=1):
        box_row(f"{BRIGHT_GOLD}{number}{RESET}   {GOLD}◆{RESET}   {CREAM}{text}{RESET}")
    box_row()
    box_bottom()


def option_line(number, text):
    out(f"{BRIGHT_GOLD}{number}{RESET}  {GOLD}◆{RESET}  {CREAM}{text}{RESET}")


def ask(question):
    answer = input(f"{MARGIN}{GOLD}❯ {CREAM}{question}{BRIGHT_GOLD}")
    print(RESET, end="")
    return answer


def pause(message="Press Enter to continue..."):
    blank()
    input(f"{MARGIN}{GREY}{message}{RESET}")


def goodbye():
    blank()
    box_top()
    box_row()
    box_row(f"{GOLD}✦   ✦   ✦", "center")
    box_row(f"{BRIGHT_GOLD}Thank you for visiting Celinó Hotel.", "center")
    box_row(f"{CREAM}Hope to see you again!", "center")
    box_row(f"{GOLD}✦   ✦   ✦", "center")
    box_row()
    box_bottom()
    blank()


# ======================================================================
#  INPUT AND SMALL HELPERS
# ======================================================================
def ask_number(question, low, high, allow_back=False):
    while True:
        text = ask(question).strip()
        if allow_back and text.lower() == "back":
            return None
        if not text.isdecimal():
            error("Invalid input! Please enter numbers only.")
        else:
            number = int(text)
            if number >= low and number <= high:
                return number
            error(f"Please enter a number between {low} and {high}.")


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


def get_free_rooms(room_type, start, end, skip_id):
    free = []
    for room in rooms:
        if room["type"] == room_type and is_room_free(room["number"], start, end, skip_id):
            free.append(room)
    return free


# ======================================================================
#  SHOWING BOOKINGS, DATES AND ROOMS
# ======================================================================
def show_booking(res):
    room = find_room(res["room"])
    box_top("BOOKING DETAILS")
    box_row()
    kv_row("Booking ID", res["id"], BRIGHT_GOLD)
    kv_row("Guest Name", res["name"])
    kv_row("Contact Number", res["contact"])
    kv_row("Email Address", res["email"])
    box_thin()
    kv_row("Check-in Date", format_date(res["check_in"]))
    kv_row("Check-out Date", format_date(res["check_out"]))
    kv_row("Guests", res["guests"])
    kv_row("Room", f"{res['room']} ({room['type']})")
    box_thin()
    kv_row("Cost", f"{res['nights']} night(s) x {money(room['price'])} = {money(res['total'])}")
    kv_row("Payment Status", badge(res["payment_status"]))
    kv_row("Amount Paid", money(res["paid"]))
    kv_row("Paid Via", res["pay_method"])
    kv_row("Reference", res["pay_ref"])
    box_thin()
    kv_row("Booking Status", badge(res["status"]))
    if res["group"] != "none":
        kv_row("Same Reservation As", res["group"])
    box_row()
    box_bottom()


def get_dates(step=""):
    section("CHECK-IN & CHECK-OUT DATES", step)
    today = date.today()
    while True:
        month = ask_number("Enter Check-in Month (1-12): ", 1, 12, True)
        if month is None:
            return None
        day = ask_number("Enter Check-in Day (1-31): ", 1, 31, True)
        if day is None:
            return None

        if day > days_in_month(today.year, month):
            error("Invalid calendar date! Please try again.")
            continue

        check_in = date(today.year, month, day)

        if check_in < today:
            blank()
            warn(f"{format_date(check_in)} has already passed.")
            option_line(1, "Book for next year instead")
            option_line(2, "Enter a different date")
            if ask_number("Enter choice (1-2): ", 1, 2) == 2:
                continue
            if day > days_in_month(today.year + 1, month):
                error("That date does not exist next year. Please try again.")
                continue
            check_in = date(today.year + 1, month, day)

        break

    nights = ask_number("How many nights will you stay? ", 1, 30, True)
    if nights is None:
        return None
    check_out = check_in + timedelta(days=nights)

    blank()
    box_top("YOUR STAY")
    kv_row("Check-in", format_date(check_in))
    kv_row("Check-out", format_date(check_out))
    kv_row("Nights", nights)
    box_bottom()
    return check_in, check_out, nights


def show_rooms(room_type):
    screen(f"{room_type.upper()} ROOMS")

    total_rooms = 0
    sample = None
    for room in rooms:
        if room["type"] == room_type:
            total_rooms += 1
            sample = room

    today = date.today()
    free_tonight = len(get_free_rooms(room_type, today, today + timedelta(days=1), ""))

    box_top(f"{room_type.upper()} ROOM")
    box_row()
    kv_row("Price per night", money(sample["price"]), BRIGHT_GOLD)
    kv_row("Max guests per room", sample["max_guests"])
    kv_row("Total rooms", total_rooms)
    meter = f"{GOLD}{'■' * free_tonight}{GREY}{'□' * (total_rooms - free_tonight)}{RESET}"
    kv_row("Available tonight", f"{CREAM}{free_tonight} of {total_rooms}{RESET}  {meter}")

    booked = []
    for res in reservations:
        res_room = find_room(res["room"])
        if res_room["type"] == room_type and (res["status"] == "CONFIRMED" or res["status"] == "CHECKED-IN") and res["check_out"] > today:
            booked.append(f"{format_date(res['check_in'])}  →  {format_date(res['check_out'])}")

    if len(booked) > 0:
        box_thin()
        box_row(f"{GOLD}Upcoming booked dates (1 room each){RESET}")
        for text in booked:
            box_row(f"{GREY}◆{RESET} {CREAM}{text}{RESET}")

    box_row()
    box_bottom()
    pause("Press Enter to go back...")


def choose_room_type(check_in, check_out, guests_per_room, rooms_needed, skip_id):
    available = []

    blank()
    box_top("ROOM AVAILABILITY")
    box_row(f"{CREAM}{format_date(check_in)}  →  {format_date(check_out)}{RESET}", "center")
    box_divider()
    box_row(f"{GOLD}{pad('ROOM', 10)}{pad('RATE / NIGHT', 14)}{pad('MAX', 6)}STATUS{RESET}")
    box_thin()

    for room_type in ROOM_TYPES:
        sample = None
        for room in rooms:
            if room["type"] == room_type:
                sample = room
                break

        left = len(get_free_rooms(room_type, check_in, check_out, skip_id))
        if sample["max_guests"] < guests_per_room:
            status = f"{RED}✖ Too small · max {sample['max_guests']} guests{RESET}"
        elif left == 0:
            status = f"{RED}✖ Fully booked{RESET}"
        elif left < rooms_needed:
            status = f"{ORANGE}▲ Not enough · only {left} left{RESET}"
        else:
            status = f"{GREEN}● Available · {left} left{RESET}"
            available.append(room_type)

        rate = money(sample["price"]) + "/night"
        box_row(f"{BRIGHT_GOLD}{pad(room_type, 10)}{CREAM}{pad(rate, 14)}{pad(str(sample['max_guests']), 6)}{RESET}{status}")

    box_bottom()

    if len(available) == 0:
        blank()
        error("Sorry! No room is available for your dates, guests, and rooms.")
        return None

    blank()
    options = []
    for room_type in available:
        sample = None
        for room in rooms:
            if room["type"] == room_type:
                sample = room
                break
        options.append(f"{room_type} Room   {GREY}· {money(sample['price'])}/night")
    options.append("Go Back")
    show_menu("SELECT A ROOM TYPE", options)

    number = len(available) + 1
    choice = ask_number(f"Select a room type (1-{number}): ", 1, number)
    if choice == number:
        blank()
        info("Going back. No room was selected.")
        return None
    return available[choice - 1]


# ======================================================================
#  PAYMENT
# ======================================================================
def ask_card():
    while True:
        cardholder = ask("Enter Name on Card: ").strip()
        if cardholder.lower() == "back":
            return None
        letters = cardholder.replace(" ", "").replace(".", "").replace("'", "").replace("-", "")
        if len(cardholder) >= 2 and letters.isalpha():
            break
        error("Invalid name! Use letters only.")

    while True:
        number = ask("Enter 16-digit Card Number: ").replace(" ", "")
        if number.lower() == "back":
            return None
        if number.isdecimal() and len(number) == 16:
            break
        error("Invalid card number! It must be 16 digits.")

    while True:
        cvv = ask("Enter 3-digit CVV: ").strip()
        if cvv.lower() == "back":
            return None
        if cvv.isdecimal() and len(cvv) == 3:
            break
        error("Invalid CVV! It must be 3 digits.")

    return [cardholder.upper(), number]


def ask_wallet(method):
    while True:
        number = ask(f"Enter your {method} Number (11 digits starting with 09): ").strip()
        if number.lower() == "back":
            return None
        if number.isdecimal() and len(number) == 11 and number.startswith("09"):
            return number
        error("Invalid number! Must be 11 digits and start with '09'.")


def take_payment(amount):
    section("PAYMENT")
    box_top("AMOUNT DUE")
    box_row()
    box_row(f"{BRIGHT_GOLD}{money(amount)}", "center")
    box_row()
    box_bottom()
    tip("You can type 'back' on any question to return to the payment methods.")

    while True:
        blank()
        show_menu("PAYMENT METHOD", ["Debit/Credit Card", "GCash/Maya", "Cancel Payment"])
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

    blank()
    box_top("PAYMENT RECEIPT")
    box_row()
    kv_row("Reference", reference, BRIGHT_GOLD)
    kv_row("Method", pay_method)
    if cardholder != "":
        kv_row("Cardholder", cardholder)
    kv_row("Amount Paid", money(amount), BRIGHT_GOLD)
    box_row()
    box_row(f"{GREEN}✔ Payment successful!", "center")
    box_row()
    box_bottom()

    return [pay_method, reference]


# ======================================================================
#  MAKING A RESERVATION
# ======================================================================
def make_reservation():
    screen("MAKE A RESERVATION")
    tip("You can type 'back' on any question to return to the menu.")

    dates = get_dates("STEP 1 OF 4")
    if dates is None:
        return False
    check_in = dates[0]
    check_out = dates[1]
    nights = dates[2]

    section("GUESTS & ROOMS", "STEP 2 OF 4")
    guests = ask_number("Number of Guests: ", 1, MAX_TOTAL_GUESTS, True)
    if guests is None:
        return False

    while True:
        rooms_needed = ask_number("Number of Rooms: ", 1, MAX_ROOMS, True)
        if rooms_needed is None:
            return False
        if rooms_needed <= guests:
            break
        error("You cannot book more rooms than guests.")

    guests_per_room = guests // rooms_needed
    if guests % rooms_needed != 0:
        guests_per_room += 1

    room_type = choose_room_type(check_in, check_out, guests_per_room, rooms_needed, "")
    if room_type is None:
        pause("Press Enter to return to menu...")
        return False

    section("GUEST DETAILS", "STEP 3 OF 4")

    while True:
        name = ask("Enter Guest Name (First and Last Name): ").strip()
        if name.lower() == "back":
            return False
        letters = name.replace(" ", "").replace(".", "").replace("'", "").replace("-", "")
        if " " in name and letters.isalpha():
            break
        error("Invalid name! Enter BOTH first and last name, letters only.")
    name = name.title()

    while True:
        while True:
            contact = ask("Enter Contact Number (11 digits starting with 09, or 'none'): ").strip().lower()
            if contact == "back":
                return False
            if contact == "none":
                break
            if contact.isdecimal() and len(contact) == 11 and contact.startswith("09"):
                break
            error("Invalid contact! Must be 11 digits and start with '09'.")

        while True:
            email = ask("Enter Email Address (or 'none'): ").strip().lower()
            if email == "back":
                return False
            if email == "none":
                break
            if is_valid_email(email):
                break
            error("Invalid email! Must end with @gmail.com, @yahoo.com, @outlook.com, @icloud.com, or @hotmail.com.")

        if contact == "none" and email == "none":
            blank()
            error("Provide AT LEAST a contact number OR an email.")
            blank()
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

    section("RESERVATION SUMMARY", "STEP 4 OF 4")
    grand_total = 0
    for booking in new_bookings:
        show_booking(booking)
        grand_total += booking["total"]
    if len(new_bookings) > 1:
        blank()
        info(f"{len(new_bookings)} rooms booked for {guests} guests. Each room has its own Booking ID.")

    blank()
    box_top("TOTAL")
    box_row()
    kv_row("Total to pay", money(grand_total), BRIGHT_GOLD)
    box_row()
    box_bottom()

    blank()
    show_menu("CONFIRM", ["Proceed to Payment", "Cancel"])
    if ask_number("Enter choice (1-2): ", 1, 2) == 2:
        blank()
        warn("Reservation cancelled. No payment was made.")
        pause("Press Enter to return to menu...")
        return False

    payment = take_payment(grand_total)
    if len(payment) == 0:
        blank()
        warn("Payment cancelled. Your booking was not saved.")
        pause("Press Enter to return to menu...")
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

    blank()
    box_top("RESERVATION CONFIRMED")
    box_row()
    box_row(f"{BRIGHT_GOLD}✦   Thank you for choosing Celinó Hotel   ✦", "center")
    box_row()
    if len(new_bookings) == 1:
        kv_row("Your booking ID", new_bookings[0]["id"], BRIGHT_GOLD)
    else:
        box_row(f"{GOLD}Your booking IDs:{RESET}")
        for booking in new_bookings:
            box_row(f"{BRIGHT_GOLD}{booking['id']}{RESET}  {GREY}·{RESET}  {CREAM}Room {booking['room']} ({booking['guests']} guest(s)){RESET}")
    box_row()
    box_bottom()
    blank()
    info("Please keep your booking ID(s). You need them (and your contact/email) to manage your booking.")

    blank()
    show_menu("WHAT NEXT?", ["Back to Main Menu", "Exit"])
    choice = ask_number("Enter choice (1-2): ", 1, 2)
    if choice == 2:
        goodbye()
        sys.exit()
    return True


# ======================================================================
#  FINDING AND CHANGING BOOKINGS
# ======================================================================
def ask_booking_id():
    while True:
        search_id = ask("Enter Booking ID (e.g., M2-0001): ").strip().upper()
        if search_id == "BACK":
            return "back"
        booking = find_booking(search_id)
        if booking is not None:
            return booking
        blank()
        error("Booking ID not found. Please try again.")
        blank()


def find_my_booking():
    booking = ask_booking_id()
    if booking == "back":
        return "back"

    for attempt in range(3):
        proof = ask("Enter the contact number or email used for this booking: ").strip().lower()
        if proof == "back":
            return "back"
        if proof != "none" and (proof == booking["contact"] or proof == booking["email"]):
            return booking
        blank()
        error(f"Details do not match this booking. Attempts left: {2 - attempt}")
        blank()

    error("Verification failed. Too many wrong tries.")
    return None


def pay_or_refund(booking, new_total):
    difference = new_total - booking["paid"]

    if difference > 0:
        blank()
        info(f"The new total is {money(new_total)}. You need to pay an extra {money(difference)}.")
        option_line(1, "Pay Extra Amount")
        option_line(2, "Keep My Original Booking")
        if ask_number("Enter choice (1-2): ", 1, 2) == 2:
            return False

        payment = take_payment(difference)
        if len(payment) == 0:
            blank()
            warn("Payment cancelled.")
            return False
        booking["pay_ref"] = booking["pay_ref"] + ", " + payment[1]
        booking["paid"] = new_total
    elif difference < 0:
        blank()
        info(f"The new total is {money(new_total)}. {money(-difference)} will be refunded to {booking['refund_to']}.")
        booking["paid"] = new_total

    return True


def cancel_booking(booking):
    if booking["status"] != "CONFIRMED":
        blank()
        error(f"Cannot cancel. This booking is {booking['status']}.")
        return

    days_left = (booking["check_in"] - date.today()).days

    blank()
    box_top("CANCELLATION POLICY")
    box_row()
    box_text("Full refund if you cancel 3 or more days before check-in.")
    box_text("If you cancel later than that, there is NO refund.", ORANGE)
    box_row()
    box_bottom()
    blank()

    if days_left >= 3:
        ok(f"Your check-in is {days_left} days away, so you get a full refund of {money(booking['paid'])}.")
    else:
        warn(f"Your check-in is too close, so {money(booking['paid'])} will NOT be refunded.")

    blank()
    if ask("Type 'yes' to cancel this booking: ").strip().lower() != "yes":
        blank()
        info("Cancellation stopped. Your booking is still active.")
        return

    booking["status"] = "CANCELLED"
    blank()
    ok("Reservation CANCELLED. The room is now available again.")
    if days_left >= 3:
        info(f"Full refund of {money(booking['paid'])} will be sent to {booking['refund_to']}.")
        booking["payment_status"] = "REFUNDED"
        booking["paid"] = 0
    else:
        warn(f"No refund. {money(booking['paid'])} is non-refundable.")
        booking["payment_status"] = "NON-REFUNDABLE"


def change_booking(booking):
    if booking["status"] == "CHECKED-IN":
        blank()
        error("You cannot change a booking after check-in.")
        return
    if booking["status"] != "CONFIRMED":
        blank()
        error(f"Cannot change this booking. Its status is {booking['status']}.")
        return

    days_left = (booking["check_in"] - date.today()).days
    if days_left < 3:
        blank()
        warn("Changes are only allowed 3 or more days before check-in.")
        warn("Your check-in is too close to change this booking.")
        return

    blank()
    show_menu("CHANGE BOOKING", ["Change Dates", "Change Room Type", "Go Back"])
    choice = ask_number("Enter choice (1-3): ", 1, 3)

    old_room = find_room(booking["room"])

    if choice == 1:
        blank()
        tip("You can type 'back' on any question to cancel the change.")
        while True:
            dates = get_dates()
            if dates is None:
                blank()
                info("Nothing was changed.")
                return
            if (dates[0] - date.today()).days >= 3:
                break
            blank()
            warn("The new check-in date must be at least 3 days from today. Please choose another date.")
        check_in = dates[0]
        check_out = dates[1]
        nights = dates[2]

        free_rooms = get_free_rooms(old_room["type"], check_in, check_out, booking["id"])
        if len(free_rooms) == 0:
            blank()
            error("Sorry, no room of your type is available for those dates. Nothing was changed.")
            return

        new_room = free_rooms[0]
        if old_room in free_rooms:
            new_room = old_room

        new_total = new_room["price"] * nights

        if not pay_or_refund(booking, new_total):
            blank()
            info("Nothing was changed.")
            return

        booking["room"] = new_room["number"]
        booking["check_in"] = check_in
        booking["check_out"] = check_out
        booking["nights"] = nights
        booking["total"] = new_total

        blank()
        ok("Dates updated!")
        show_booking(booking)

    elif choice == 2:
        room_type = choose_room_type(booking["check_in"], booking["check_out"], booking["guests"], 1, booking["id"])
        if room_type is None:
            info("Nothing was changed.")
            return

        free_rooms = get_free_rooms(room_type, booking["check_in"], booking["check_out"], booking["id"])
        new_room = free_rooms[0]
        if old_room in free_rooms:
            new_room = old_room

        if new_room["number"] == old_room["number"]:
            blank()
            info(f"You are already booked in a {old_room['type']} room. Nothing was changed.")
            return

        new_total = new_room["price"] * booking["nights"]

        if not pay_or_refund(booking, new_total):
            blank()
            info("Nothing was changed.")
            return

        booking["room"] = new_room["number"]
        booking["total"] = new_total

        blank()
        ok("Room updated!")
        show_booking(booking)


# ======================================================================
#  STAFF FUNCTIONS
# ======================================================================
def view_all_reservations():
    screen("ALL RESERVATIONS")
    if len(reservations) == 0:
        info("No reservations yet.")
    else:
        income = 0
        for res in reservations:
            show_booking(res)
            blank()
            income += res["paid"]
        box_top("SUMMARY")
        box_row()
        kv_row("Total reservations", len(reservations))
        kv_row("Total income (payments received)", money(income), BRIGHT_GOLD)
        box_row()
        box_bottom()
    pause()


def staff_manage_reservation():
    while True:
        screen("STAFF  ·  MANAGE A RESERVATION")
        tip("Type 'back' on the Booking ID question to return.")
        booking = ask_booking_id()
        if booking == "back":
            return

        section("RESERVATION DETAILS")
        show_booking(booking)

        blank()
        show_menu("ACTIONS", ["Change Dates or Room", "Cancel Reservation", "Go Back"])
        manage_choice = ask_number("Enter choice (1-3): ", 1, 3)
        if manage_choice == 1:
            change_booking(booking)
            pause()
        elif manage_choice == 2:
            cancel_booking(booking)
            pause()


def check_in_guest():
    screen("CHECK-IN")
    tip("Type 'back' on the Booking ID question to return.")
    booking = ask_booking_id()
    if booking == "back":
        return

    blank()
    if booking["status"] != "CONFIRMED":
        error(f"Cannot check in. This booking is {booking['status']}.")
    elif date.today() >= booking["check_out"]:
        error("This booking has already ended.")
    elif date.today() < booking["check_in"]:
        warn(f"Too early. Check-in date is {format_date(booking['check_in'])}.")
    else:
        room = find_room(booking["room"])
        if room["status"] != "AVAILABLE":
            warn(f"Room {room['number']} is not ready yet (status: {room['status']}).")
            for other in rooms:
                if other["type"] == room["type"] and other["status"] == "AVAILABLE" and is_room_free(other["number"], booking["check_in"], booking["check_out"], booking["id"]):
                    info(f"Moving the guest to Room {other['number']} (same type) instead.")
                    booking["room"] = other["number"]
                    room = other
                    break

        if room["status"] != "AVAILABLE":
            error("No other ready room of the same type. Please try again later.")
        else:
            booking["status"] = "CHECKED-IN"
            room["status"] = "OCCUPIED"
            ok(f"{booking['name']} is now CHECKED-IN to Room {room['number']}.")
    pause()


def check_out_guest():
    screen("CHECK-OUT")
    tip("Type 'back' on the Booking ID question to return.")
    booking = ask_booking_id()
    if booking == "back":
        return

    blank()
    if booking["status"] != "CHECKED-IN":
        error(f"Cannot check out. This booking is {booking['status']}.")
    else:
        room = find_room(booking["room"])
        booking["status"] = "CHECKED-OUT"
        room["status"] = "CLEANING"
        ok(f"{booking['name']} is now CHECKED-OUT.")
        warn(f"Room {room['number']} needs CLEANING.")
    pause()


def mark_no_show():
    screen("MARK AS NO-SHOW")
    tip("Type 'back' on the Booking ID question to return.")
    booking = ask_booking_id()
    if booking == "back":
        return

    blank()
    if booking["status"] != "CONFIRMED":
        error(f"Cannot mark as no-show. This booking is {booking['status']}.")
    elif date.today() <= booking["check_in"]:
        warn(f"Too early. The guest can still arrive until the end of {format_date(booking['check_in'])}.")
    else:
        booking["status"] = "NO-SHOW"
        booking["payment_status"] = "NON-REFUNDABLE"
        ok(f"{booking['name']} is marked as NO-SHOW.")
        info(f"The room is free again. {money(booking['paid'])} is kept (non-refundable).")
    pause()


def view_room_status():
    screen("ROOM STATUS")
    box_top("ALL ROOMS")
    box_row(f"{GOLD}{pad('ROOM', 7)}{pad('TYPE', 11)}{pad('STATUS', 14)}GUEST{RESET}")
    box_thin()

    last_type = ""
    counts = {"AVAILABLE": 0, "OCCUPIED": 0, "CLEANING": 0}
    for room in rooms:
        if last_type != "" and room["type"] != last_type:
            box_thin()
        last_type = room["type"]
        counts[room["status"]] = counts.get(room["status"], 0) + 1

        guest = ""
        for res in reservations:
            if res["room"] == room["number"] and res["status"] == "CHECKED-IN":
                guest += f"{res['name']} ({res['id']})"
        if len(guest) > 30:
            guest = guest[:29] + "…"

        box_row(f"{BRIGHT_GOLD}{pad(str(room['number']), 7)}{CREAM}{pad(room['type'], 11)}{RESET}{pad(badge(room['status']), 14)}{GREY}{guest}{RESET}")

    box_divider()
    box_row(f"{GREEN}● Available {counts['AVAILABLE']}{RESET}   {RED}● Occupied {counts['OCCUPIED']}{RESET}   {ORANGE}● Cleaning {counts['CLEANING']}{RESET}", "center")
    box_bottom()
    pause()


def mark_room_clean():
    screen("MARK ROOM AS CLEAN")
    cleaning = []
    for room in rooms:
        if room["status"] == "CLEANING":
            cleaning.append(room)

    if len(cleaning) == 0:
        info("No rooms need cleaning.")
    else:
        options = []
        for room in cleaning:
            options.append(f"Room {room['number']} ({room['type']})")
        show_menu("ROOMS NEEDING CLEANING", options)

        clean_choice = ask_number(f"Select a room (1-{len(cleaning)}): ", 1, len(cleaning))
        chosen = cleaning[clean_choice - 1]
        chosen["status"] = "AVAILABLE"
        blank()
        ok(f"Room {chosen['number']} is now AVAILABLE.")
    pause()


# ======================================================================
#  MAIN PROGRAM
# ======================================================================
def main():
    while True:
        banner()
        blank()
        show_menu("MAIN MENU", [
            "View Rooms / Make Reservation",
            "Manage My Reservation",
            "Hotel Information",
            "Staff Area",
            "Exit",
        ])

        choice = ask_number("Enter choice (1-5): ", 1, 5)

        if choice == 1:
            while True:
                screen("ROOMS & RESERVATION")
                show_menu("ROOMS AND RESERVATION", [
                    "View Standard Rooms",
                    "View Deluxe Rooms",
                    "View Suite Rooms",
                    "Make a Reservation",
                    "Back to Main Menu",
                ])

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
            while True:
                screen("MANAGE MY RESERVATION")
                show_menu("MANAGE MY RESERVATION", [
                    "Search Reservation by Booking ID",
                    "Change Dates or Room",
                    "Cancel Reservation",
                    "Back to Main Menu",
                ])

                manage_choice = ask_number("Enter choice (1-4): ", 1, 4)
                if manage_choice == 4:
                    break

                blank()
                tip("You can type 'back' on any question to return to the Manage menu.")
                booking = find_my_booking()
                if booking == "back":
                    continue
                if booking is not None:
                    section("RESERVATION DETAILS")
                    show_booking(booking)

                    if manage_choice == 2:
                        change_booking(booking)
                    elif manage_choice == 3:
                        cancel_booking(booking)

                pause("Press Enter to return to Manage Menu...")

        elif choice == 3:
            screen("HOTEL INFORMATION")
            box_top("CELINÓ HOTEL")
            box_row()
            box_row(f"{GOLD}✦   ★ ★ ★ ★ ★   ✦", "center")
            box_row()
            kv_row("Hotel Name", "Celinó Hotel", BRIGHT_GOLD)
            kv_row("Address", "km.30 National Road, Tunasan, Muntinlupa")
            kv_row("Contact Number", "09123456789")
            kv_row("Email", "celinohotel@gmail.com")
            box_row()
            box_bottom()
            pause("Press Enter to go back to Main Menu...")

        elif choice == 4:
            screen("STAFF LOGIN")
            tip("You can type 'back' to return to the Main Menu.")
            logged_in = False
            went_back = False
            for attempt in range(3):
                password = ask("Enter staff password: ")
                if password.strip().lower() == "back":
                    went_back = True
                    break
                if password == STAFF_PASSWORD:
                    logged_in = True
                    break
                error(f"Wrong password. Attempts left: {2 - attempt}")

            if went_back:
                blank()
                info("Going back to the Main Menu.")
            elif not logged_in:
                blank()
                error("Access denied.")
                pause("Press Enter to return...")
            else:
                while True:
                    screen("STAFF AREA")
                    show_menu("STAFF MENU", [
                        "View All Reservations",
                        "Manage a Reservation",
                        "Check-in a Guest",
                        "Check-out a Guest",
                        "Mark a No-Show",
                        "View Room Status",
                        "Mark Room as Clean",
                        "Back to Main Menu",
                    ])
                    tip("You can type 'back' on any Booking ID question to return to the Staff Menu.")

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
    print(RESET)
    blank()
    warn("Program stopped.")

goodbye()
