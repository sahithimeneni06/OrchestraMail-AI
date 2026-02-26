from .email_flows import send_new_flow, reply_using_email_flow, reply_from_inbox_flow
def mail_agent():

    print("\n====== AI MAIL AGENT ======\n")
    print("1️⃣ Send NEW email")
    print("2️⃣ Reply using recipient email")
    print("3️⃣ Reply from inbox list")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        send_new_flow()

    elif choice == "2":
        reply_using_email_flow()

    elif choice == "3":
        reply_from_inbox_flow()

    else:
        return