from telegram.direct_msg import message
from telegram.join_group import join
import sys
import os
import traceback

if __name__ == '__main__':
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone_number = os.getenv('PHONE_NUMBER')
    shilling_text = os.getenv('SHILLING_TEXT')
    shilling_partner = os.getenv('SHILLING_PARTNER')
    shilling_user = os.getenv('SHILLING_USER')

    if len(sys.argv) != 1:
        raise BaseException('Invalid arguments passed.')
    if str(sys.argv) == 'RUN_MESSAGE':
        try:
            message(api_id=api_id, api_hash=api_hash, phone_number=phone_number, shilling_text=shilling_text,
                    shilling_partner=shilling_partner, shilling_user=shilling_user)
            print('Success')
        except Exception:
            print("Unexpected Error")
            print(traceback.print_exc())
            pass
    elif str(sys.argv) == 'JOIN_GROUPS':
        try:
            join(api_id=api_id, api_hash=api_hash)
            print('Success')
        except Exception:
            print("Unexpected Error")
            print(traceback.print_exc())
            pass

