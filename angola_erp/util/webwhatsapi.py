import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message

driver = WhatsAPIDriver()
print ("Waiting for QR")
driver.wait_for_login()

print("BOT STARTED")

while True:
	time.sleep(3)
	print('Checking for messages...')
	for contact in driver.get_unread():
		for message in contact.messages:
			if isinstance(message, Message):
				contact.chat.send_message(message.safe_content)

