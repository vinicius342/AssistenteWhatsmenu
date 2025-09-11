import datetime
import os
import shutil
import time

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from log import LogFileMixin
from utils import PROFILE_WHATSAPP_PATH


class Whatsapp(LogFileMixin):
    def __init__(self, msg_title: str, automatic_msg: str, headless: bool,
                 check_messages: bool = True):
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
        self.check_messages = check_messages

    def start(self):
        try:
            # Selenium irá buscar o chromedriver automaticamente no PATH
            self.driver = webdriver.Chrome(options=self.options)
        except WebDriverException as e:
            print('webdriver', e.__class__.__name__)
            if os.path.exists(PROFILE_WHATSAPP_PATH):
                shutil.rmtree(PROFILE_WHATSAPP_PATH)
            raise e
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
                    By.XPATH, '//*[@aria-label="Nova conversa"]'
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
                    '//*[@aria-label="Pesquisar nome ou número"]'
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

        # Se a checagem de mensagens estiver desabilitada, envia direto
        if not self.check_messages:
            self.log_success(f'{phone_number} message check disabled')
            self.send_msg()
            self.log_success(f'{phone_number} message sent without check')
            return

        # Verifica se já existe mensagem com código do pedido
        has_order_code = self._has_order_code_message()
        self.log_success(f'{phone_number} order code result: {has_order_code}')

        if has_order_code:
            self.log_success(f'{phone_number} order code already found')
            print('encontrou codigo do pedido')
            return

        # Se não encontrou código do pedido, envia mensagem
        self.log_success(f'{phone_number} no order code found - sending msg')
        print(f'Sending message to {phone_number}')
        self.send_msg()
        self.log_success(f'{phone_number} message sent')

    def _has_order_code_message(self) -> bool:
        """
        Verifica se já existe uma mensagem com código do pedido no chat HOJE.
        Busca por mensagens que contenham 'Código do pedido' junto com
        'www.whatsmenu.com.br' ou o título da mensagem configurado,
        mas apenas nas mensagens de hoje.
        """
        try:
            # Busca todas as mensagens no chat usando a classe copyable-area
            messages = self.wait.until(lambda x: x.find_elements(
                By.CLASS_NAME, 'copyable-area'
            ))

            self.log_success(f'Found {len(messages)} messages to check')
            print(f'Debug: Found {len(messages)} messages')

            # Verifica cada mensagem
            for i, message in enumerate(messages):
                message_text = message.text.strip()
                print(f'Debug: Message {i+1}: {message_text[:100]}...')

                # Verifica se a mensagem é de hoje
                if 'HOJE' in message_text:
                    print(f'Debug: Message {i+1} contains HOJE')
                    # Pega apenas o texto a partir de "HOJE"
                    hoje_index = message_text.find('HOJE')
                    today_message = message_text[hoje_index:]

                    # Verifica se contém código do pedido
                    if 'Código do pedido' in today_message:
                        print(f'Debug: Found order code in message {i+1}')
                        # Verifica se é do whatsmenu ou do título configurado
                        if ('www.whatsmenu.com.br' in today_message or
                                self.msg_title in today_message):
                            self.log_success('Order code message found today')
                            print('Debug: Order code from expected source')
                            return True

            self.log_success('No order code message found today')
            return False

        except TimeoutException:
            self.log_error('Timeout waiting for messages')
            return False
        except Exception as e:
            self.log_error(f'Error checking messages: {e.__class__.__name__}')
            return False

    def send_msg(self):
        print("Debug: Starting send_msg")
        try:
            for i, msg in enumerate(self.automatic_msg):
                print(f"Debug: Sending message {i+1}: {msg}")
                # Tenta encontrar a caixa de texto de mensagem
                try:
                    # Tenta diferentes seletores para a caixa de mensagem
                    msg_box = None

                    # Opção 1: div contenteditable
                    try:
                        msg_box = self.wait.until(lambda x: x.find_element(
                            By.XPATH,
                            '//div[@contenteditable="true"][@data-tab="10"]'
                        ))
                        print("Debug: Found message box using contenteditable")
                    except TimeoutException:
                        pass

                    # Opção 2: div com role textbox
                    if not msg_box:
                        try:
                            msg_box = self.wait.until(lambda x: x.find_element(
                                By.XPATH,
                                '//div[@role="textbox"]'
                            ))
                            print("Debug: Found box using role=textbox")
                        except TimeoutException:
                            pass

                    # Opção 3: qualquer elemento contenteditable
                    if not msg_box:
                        msg_box = self.wait.until(lambda x: x.find_element(
                            By.XPATH,
                            '//*[@contenteditable="true"]'
                        ))
                        print("Debug: Found box using contenteditable=true")

                except TimeoutException:
                    print("Debug: Could not find message box")
                    self.log_error('Could not find message input box')
                    return

                # Limpa e envia a mensagem
                print(f"Debug: Clicking message box and sending: {msg}")
                msg_box.click()
                msg_box.clear()
                msg_box.send_keys(msg)
                msg_box.send_keys(Keys.ENTER)
                time.sleep(1)  # Pausa entre mensagens
                print(f"Debug: Message {i+1} sent successfully")

        except AttributeError as e:
            self.log_error(f'msg AttributeError: {e.__class__.__name__}')
            print(f"Debug: AttributeError: {e}")
            return
        except TimeoutException:
            self.log_error('msg TimeoutException: Could not find message box')
            return
        except Exception as e:
            self.log_error(f'msg Exception: {e.__class__.__name__}')
            return
        else:
            time.sleep(1)
            self.log_success('msg sent successfully')
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
                    'Recebemos o seu pedido.', True, True)
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
