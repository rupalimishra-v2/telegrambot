from telethon import TelegramClient
import traceback
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import SessionPasswordNeededError, FloodWaitError, ChatWriteForbiddenError, ChatAdminRequiredError
import time
import datetime
from report.csv_report import csv_file_generator
from report.csv_to_pdf import csv_to_pdf
from utils import constants
from utils.ds_operations import generate_group_data, convert_list_into_list_of_lists

""" https://docs.telethon.dev/en/stable/modules/client.html
    https://www.programcreek.com/python/example/123216/telethon.tl.types.User
    https://my.telegram.org/apps """


def message(api_id, api_hash, phone_number, shilling_text, shilling_partner, shilling_user):

    client = TelegramClient(shilling_partner, api_id, api_hash)

    # Client authorization not required everytime, until session expires.
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        try:
            client.sign_in(phone_number, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    group_links = constants.group_links

    async def main():
        counter = 0
        csv_report_data = []
        lists = convert_list_into_list_of_lists(group_links=group_links, number_of_items=15)
        if lists:
            for groups in lists:
                counter += 1
                print("Running for loop", counter)
                current_date = datetime.date.today().strftime("%d %B, %Y")
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                if groups:
                    for group_link in groups:
                        try:
                            await client.get_entity(group_link)
                        except ValueError:
                            group_link = None
                        if group_link is not None:
                            try:
                                await client.send_message(group_link, message=shilling_text)
                                csv_report_data.append(generate_group_data(group_link=group_link,
                                                                           current_date=current_date,
                                                                           current_time=current_time,
                                                                           text=shilling_text))
                            except ChatWriteForbiddenError:
                                print(group_link)
                                pass
                                # await client(JoinChannelRequest(group_link))
                                # await client.send_message(group_link, message=text)
                                # csv_report_data.append(generate_group_data(group_link=group_link,
                                #                                            current_date=current_date,
                                #                                            current_time=current_time,
                                #                                            text=text))
                                # time.sleep(30)
                            except ChatAdminRequiredError:
                                print(group_link)
                                pass
                            except FloodWaitError as ex:
                                print("Getting Flood Error from telegram. Script is stopping now."
                                      " Please try again after some time for {} seconds.".format(ex.seconds))
                                time.sleep(ex.seconds)
                                pass
                    time.sleep(60)
            print("Loop ending counter {}".format(counter))

        file_name = constants.generated_reports_path + shilling_partner + datetime.date.today().strftime("%d %B, %Y")
        csv_file_generator(data=csv_report_data, file_name=file_name)
        time.sleep(10)
        csv_to_pdf(file_name=file_name, report_by=shilling_user, shilling_partner=shilling_partner)

    with client:
        client.loop.run_until_complete(main())


if __name__ == '__main__':
    try:
        message(0, '', '', constants.elitheum_shilling_text,
                constants.elitheum_shilling_partner, constants.shilling_cj_user)
        print('Success')
    except Exception:
        print("Unexpected Error")
        print(traceback.print_exc())
        pass
