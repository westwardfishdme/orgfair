

def main():
    first_name = input("what is your first name?: ")
    last_name = input("what is your last name?: ")
    email = input("what is your student email?: ")

    csv = f"{first_name},{last_name},{email}\n"
    with open("7968.csv", "a") as file:
        file.write(csv)


if __name__ == "__main__":
    try:
        while True:
            main()
    except Exception:
        print("file written maybe idk finch wrote this on his phone")
