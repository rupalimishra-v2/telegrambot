from telethon import TelegramClient
import traceback
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError, ChatAdminRequiredError
import time
from utils import constants


def join(api_id, api_hash):
    client = TelegramClient(None, api_id, api_hash)

    group_links = constants.group_links

    async def main():
        counter = 0
        lists = convert_list_into_list_of_lists(group_links=group_links, number_of_items=5)
        if lists:
            for groups in lists:
                if groups is not None:
                    for group_link in groups:
                        counter += 1
                        print("Running for loop", counter)
                        try:
                            await client.get_entity(group_link)
                        except ValueError:
                            group_link = None
                        if group_link is not None:
                            try:
                                await client(JoinChannelRequest(group_link))
                            except ChatAdminRequiredError:
                                print(group_link)
                                pass
                            except FloodWaitError as ex:
                                print("Getting Flood Error from telegram. Script is stopping now."
                                      " Please try again after some time.", ex.seconds)
                                time.sleep(ex.seconds)
                    time.sleep(50)
            print(counter)

    with client:
        client.loop.run_until_complete(main())


def convert_list_into_list_of_lists(group_links, number_of_items):
    result = []
    for idx in range(0, number_of_items):
        result.append(group_links[idx::number_of_items])
    return result


if __name__ == '__main__':
    try:
        join(0, '')
    except Exception:
        print("Unexpected Error")
        print(traceback.print_exc())
        # pass
