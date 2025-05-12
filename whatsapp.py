import shutil
import time
import os

from utils import PROFILE_WHATSAPP_PATH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (TimeoutException,
                                        ElementClickInterceptedException,
                                        WebDriverException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from log import LogFileMixin


class Whatsapp(LogFileMixin):
    def __init__(self, msg_title: str, automatic_msg: str, headless: bool):
        self.options = Options()
        self.options.add_argument(
            r'user-data-dir={}'.format(PROFILE_WHATSAPP_PATH))
        if not headless:
            self.options.add_argument(r'--headless')
        self.msg_title = msg_title  # Tenho que no app
        # Tenho que colocar no app
        self.automatic_msg = automatic_msg.split('\n')
        self.window_signal = False
        self.log = LogFileMixin()
        self.driver = None
        self.active_start = False

    def start(self):
        try:
            self.driver = webdriver.Chrome(
                options=self.options)
        except WebDriverException as e:
            print('webdriver', e.__class__.__name__)
            if os.path.exists(PROFILE_WHATSAPP_PATH):
                shutil.rmtree(PROFILE_WHATSAPP_PATH)
        self.driver.get('https://web.whatsapp.com/')
        self.driver.maximize_window()

        self.current_datetime = datetime.datetime.now().strftime('%d/%m/%Y')
        self.browser_window = True
        self.list_of_checked = []
        self.wait = WebDriverWait(self.driver, 10)
        self.automatic_msg = [n.replace('\n', '') for n in self.automatic_msg]
        self.action = ActionChains(self.driver)

        self._login_()
        self.active_start = True

    def check_number(self, phone_number: str) -> None:

        formatted_phone_number = self.number_phone_formatting(phone_number)

        try:
            new_chat = self.wait.until(
                lambda x: x.find_element(
                    By.XPATH, '//button[@aria-label="Nova conversa"]'
                )
            )
            new_chat.click()
            self.log_success(f'{phone_number} new_chat clicked')
        except Exception as e:
            self.log_error(f'new_chat {e.__class__.__name__}')
            print('new_chat', e.__class__.__name__)

        try:
            search_bar = self.wait.until(
                lambda x: x.find_element(
                    By.XPATH,
                    '//div[@aria-label="Pesquisar nome ou número"]'
                )
            )
            search_bar.send_keys(phone_number)
            self.log_success(f'{phone_number} search_bar send_keys')
        except Exception as e:
            print('search_bar', e.__class__.__name__)
            self.log_error(f'search_bar {e.__class__.__name__}')

        try:
            chat = self.wait.until(
                lambda x: x.find_element(
                    By.XPATH,
                    f'//span[@title="{formatted_phone_number}"]'
                )
            )
            time.sleep(1)
            chat.click()
            self.log_success(f'{phone_number} chat clicked')
            print('chat')
        except ElementClickInterceptedException as e:
            try:
                chat = self.wait.until(
                    lambda x: x.find_element(
                        By.XPATH,
                        f'//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div[3]/div[2]/div[1]/div/span'
                    )
                )
                time.sleep(1)
                chat.click()
                self.log_success(f'{phone_number} chat clicked')
            except Exception as e:
                try:
                    back_button = self.wait.until(
                        lambda x: x.find_element(
                            By.XPATH,
                            f'//div[@aria-label="Voltar"]'
                        )
                    )
                    back_button.click()
                except Exception as e:
                    self.log_error(f'Back_button {e.__class__.__name__}')
                    self.driver.get('https://web.whatsapp.com/')
                    while True:
                        try:
                            print('Logged in', e.__class__.__name__)
                            self.wait.until(
                                lambda x: x.find_element(
                                    By.XPATH, '//*[@id="app"]')
                            )
                        except Exception as e:
                            print('Logged in', e.__class__.__name__)
                            break
                        else:
                            self.log.log_success('Logged in successfully.')
                            break
                    return print(e.__class__.__name__, 'aria-label="voltar"')
                else:
                    return
        except TimeoutException as e:
            try:
                back_button = self.wait.until(
                    lambda x: x.find_element(
                        By.XPATH,
                        f'//div[@aria-label="Voltar"]'
                    )
                )
                back_button.click()
            except Exception as e:
                self.driver.get('https://web.whatsapp.com/')
                self.log_error(f'Back_button {e.__class__.__name__}')
                while True:
                    try:
                        print('Logged in', e.__class__.__name__)
                        self.wait.until(
                            lambda x: x.find_element(
                                By.XPATH, '//*[@id="app"]')
                        )
                    except Exception as e:
                        print('Logged in', e.__class__.__name__)
                        break
                    else:
                        self.log.log_success('Logged in successfully.')
                        break
                return print(e.__class__.__name__, 'aria-label="voltar"')
            else:
                return
        except Exception as e:
            self.driver.refresh()
            self.log_error(f'chat {e.__class__.__name__}')
            while True:
                try:
                    print('new chat', e.__class__.__name__)
                    self.wait.until(
                        lambda x: x.find_element(
                            By.ID, 'side')
                    )
                except Exception:
                    ...
                else:
                    self.log.log_success('Logged in successfully.')
                    break
            return print(e, 'aria-label="voltar"')

        time.sleep(1)

        try:
            days = self.wait.until(lambda x: x.find_elements(
                By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]'
            ))
        except TimeoutException as e:
            self.log_success(f'{e.__class__.__name__} {phone_number}'
                             ' before send msg')
            self.send_msg()
            self.log_success(f'{e.__class__.__name__} {phone_number}'
                             ' later send msg')
            return
        except Exception as e:
            self.log_error(f'days {e.__class__.__name__}')
            print(e.__class__.__name__)
            return
        else:
            self.log_success(f'{phone_number} days')
            for day in days:
                word_index = day.text.find('HOJE')
                if word_index != -1:
                    formated_word = day.text[word_index:]
                    if 'www.whatsmenu.com.br' in formated_word and\
                            'Código do pedido' in formated_word:
                        self.log_success(f'{phone_number} whatsmenu'
                                         'codigo do pedido')
                        print('encontrou codigo do pedido')
                        return
                    elif self.msg_title in formated_word and\
                            'Código do pedido' in formated_word:
                        self.log_success(f'{phone_number} msg_title'
                                         'codigo do pedido')
                        print('encontrou codigo do pedido')
                        return
                    else:
                        self.log_success(f'{phone_number} before send msg')
                        self.send_msg()
                        self.log_success(f'{phone_number} later send msg')
                        return
                else:
                    self.log_success(f'{phone_number} before send msg')
                    self.send_msg()
                    self.log_success(f'{phone_number} later send msg')
                    return

    def send_msg(self):
        try:
            for msg in self.automatic_msg:
                msg_box = self.wait.until(lambda x: x.find_element(
                    By.XPATH,
                    '//div[@aria-label="Digite uma mensagem"]'
                ))
                msg_box.send_keys(msg)
                msg_box.send_keys(Keys.ENTER)
        except AttributeError as e:
            self.log_error(f'msg {e.__class__.__name__}')
            return
        except Exception as e:
            self.log_error(f'msg {e.__class__.__name__}')
            return
        else:
            time.sleep(1)
            self.log_success('msg')
            self.action.send_keys(Keys.CANCEL)
            return

    def _login_(self):
        logged_in = False
        while not logged_in and not self.window_signal:

            if not self.browser_window:
                break
            try:
                self.wait.until(
                    lambda x: x.find_element(
                        By.XPATH, '//*[@id="app"]/div/div[3]/div/div[3]/header'
                        '/header/div/span/div/div[1]/button')
                )
            except NoSuchElementException as e:
                try:
                    print('new chat', e.__class__.__name__)
                    self.wait.until(
                        lambda x: x.find_element(
                            By.ID, 'side')
                    )
                except Exception:
                    ...
                else:
                    print('logged in')
                    logged_in = True
            except TimeoutException as e:
                try:
                    print('new chat', e.__class__.__name__)
                    self.wait.until(
                        lambda x: x.find_element(
                            By.ID, 'side')
                    )
                except Exception:
                    ...
                else:
                    print('logged in')
                    logged_in = True
            except Exception as e:
                try:
                    print('new_chat', e.__class__.__name__)
                    self.wait.until(
                        lambda x: x.find_element(
                            By.ID, 'side')
                    )
                except Exception:
                    ...
                else:
                    print('logged in')
                    logged_in = True
            else:
                print('logged in')
                logged_in = True

    def number_phone_formatting(self, phone_number: str):

        phone_number_list = ['+', '55', ' ']
        for i in range(len(phone_number)):
            if i == 7:
                phone_number_list.append('-')
            elif i == 2:
                phone_number_list.append(' ')
                continue

            phone_number_list.append(phone_number[i])

        formatted_phone_number = ''
        for n in phone_number_list:
            formatted_phone_number = formatted_phone_number + n

        return formatted_phone_number

    def close(self):
        self.driver.quit()
        self.browser_window = False
        print('Whatsapp Processo finalizado com sucesso.')


if __name__ == '__main__':
    chat = Whatsapp('Beruchy Hamburgueria Delivery',
                    'Recebemos o seu pedido.', True)
    chat.start()
    chat.check_number('99999999999')
    for _ in range(20):
        time.sleep(1)
    chat.check_number('85981647142')
    for _ in range(20):
        time.sleep(1)
    chat.check_number('85981647142')
    for _ in range(20):
        time.sleep(1)
