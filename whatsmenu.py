import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from utils import PROFILE_WHATSMENU_PATH
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from whatsapp import Whatsapp


class Whatsmenu:
    def __init__(self, whatsapp: 'Whatsapp', headless: bool, wait_time: str):
        self.headless = headless
        self.whatsapp = whatsapp
        self.wait_time = wait_time
        self.window_signal = False
        self.today = datetime.datetime.today().strftime('%d/%m/%Y')
        self.driver = None
        self.logged_in = False
        try:
            with open('list_checked.txt', 'r', encoding='utf8') as file:
                self.list_of_checked = file.readlines()
                self.list_of_checked = [
                    n.replace('\n', '') for n in self.list_of_checked]
        except Exception:
            print('nao leu list_checked.txt')
            with open('list_checked.txt', 'w', encoding='utf8') as file:
                file.write(f'{self.today}\n')
                self.list_of_checked = [self.today]
        else:
            if self.today != self.list_of_checked[0]:
                self.list_of_checked = [self.today]
                with open('list_checked.txt', 'w', encoding='utf8') as file:
                    file.write(f'{self.today}\n')
            print(self.list_of_checked)

    def start(self):
        self.options = Options()
        self.options.add_argument(f'user-data-dir={PROFILE_WHATSMENU_PATH}')
        self.options.add_argument(r'--disable-print-preview')
        if not self.headless:
            self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(
            'https://next.whatsmenu.com.br/auth/login?callbackUrl=https%3A'
            '%2F%2Fnext.whatsmenu.com.br%2Fdashboard%2Frequest')
        self.driver.maximize_window()

        self.wait = WebDriverWait(self.driver, 6)
        self.browser_window = True

        # Methods
        self._login_()
        self.window_signal = False
        if self.logged_in:
            self.wait_element()

    def _login_(self) -> None:
        while not self.logged_in:
            if not self.browser_window:
                break
            try:
                self.wait.until(lambda x: x.find_element(  # E-mail box
                    By.XPATH,
                    '/html/body/main/div/div[2]/div/div/div/form/div[1]/input'
                ))
                self.wait.until(lambda x: x.find_element(  # Password box
                    By.XPATH,
                    '/html/body/main/div/div[2]/div/div/div/form/div[2]/input'
                ))
            except TimeoutException as e:
                print('E-mail and password', e.__class__.__name__)
            except Exception as e:
                print('E-mail and password', e.__class__.__name__)
                break
            else:
                for _ in range(15):
                    time.sleep(1)

            try:
                self.wait.until(lambda x: x.find_elements(
                    By.CSS_SELECTOR,
                    '#main > section > div'
                ))
            except TimeoutException as e:
                print('E-mail and password', e.__class__.__name__)
            except Exception as e:
                print('E-mail and password', e.__class__.__name__)
                break
            else:
                self.logged_in = True
                print('Logged in')

    def wait_element(self):
        while not self.window_signal:

            try:
                time.sleep(1)
                elements_list = self.wait.until(lambda x: x.find_elements(
                    By.CSS_SELECTOR,
                    '#main > section > div'
                ))

                print(self.list_of_checked)

                # Capturing the number
                for n in elements_list:
                    print(n.text.split('\n'))
                    for n2 in n.text.split('\n'):
                        if '(' in n2 and ')' in n2:
                            init = n2.index('(')
                            end = init + 15
                            phone_number = n2[init:end]
                            phone_number_clean = ''.join(
                                [i for i in phone_number if i.isdecimal()])
                            if phone_number_clean in self.list_of_checked:
                                # print(phone_number_clean)
                                continue
                            else:
                                for _ in range(int(self.wait_time)):
                                    time.sleep(1)
                                try:
                                    self.whatsapp.check_number(
                                        phone_number_clean)
                                except Exception as e:
                                    print(f'Erro ao verificar número: {e}')
                                finally:
                                    self.list_of_checked.append(
                                        phone_number_clean)
                                    with open('list_checked.txt', 'a',
                                              encoding='utf8') as file:
                                        file.write(f'{phone_number_clean}\n')
            except Exception as e:
                print('wait_element', e.__class__.__name__)
                return

    def close(self):
        self.driver.quit()
        self.browser_window = False
        print('Processo finalizado com sucesso.')


if __name__ == '__main__':
    from whatsapp import Whatsapp

    whats = Whatsapp('...', '...', False)
    whatsmenu = Whatsmenu(whats, True, '10')
    whatsmenu.start()
    whatsmenu.wait_element()
