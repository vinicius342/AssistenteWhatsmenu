import datetime
import time
from typing import TYPE_CHECKING

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils import PROFILE_WHATSMENU_PATH

if TYPE_CHECKING:
    from whatsapp import Whatsapp


class Whatsmenu:
    def __init__(self, whatsapp: 'Whatsapp', force_visible: bool,
                 wait_time: str):
        self.force_visible = force_visible
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
        # Sempre começa em headless, exceto se forçado a ser visível
        self.options = Options()
        self.options.add_argument(f'user-data-dir={PROFILE_WHATSMENU_PATH}')
        self.options.add_argument(r'--disable-print-preview')
        if not self.force_visible:
            self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(
            'https://next.whatsmenu.com.br/auth/login?callbackUrl=https%3A'
            '%2F%2Fnext.whatsmenu.com.br%2Fdashboard%2Frequest')
        self.driver.maximize_window()

        self.wait = WebDriverWait(self.driver, 6)
        self.browser_window = True

        # Tenta login automático primeiro
        login_success = self._check_login_status()

        if not login_success and not self.force_visible:
            # Se precisa de login e estava em headless, reinicia visível
            self._show_login_message("Whatsmenu")
            self._restart_with_visible_browser()
            return

        if not login_success:
            # Se está em modo visível, faz login normal
            self._login_()

        self.window_signal = False
        if self.logged_in:
            self.wait_element()

    def _check_login_status(self) -> bool:
        """
        Verifica rapidamente se já está logado no Whatsmenu
        """
        try:
            # Espera um pouco para a página carregar
            time.sleep(3)

            # Se encontrar o dashboard, está logado
            wait_short = WebDriverWait(self.driver, 5)
            wait_short.until(lambda x: x.find_elements(
                By.CSS_SELECTOR, '#main > section > div'
            ))
            self.logged_in = True
            print('Whatsmenu já está logado')
            return True
        except TimeoutException:
            # Se não encontrou dashboard, verifica se está na tela de login
            try:
                login_form = self.driver.find_elements(
                    By.XPATH, '//form[@class]'
                )
                if login_form:
                    print('Whatsmenu precisa de login')
                    return False
            except Exception:
                pass
            return False
        except Exception as e:
            print(f'Erro verificando login Whatsmenu: {e.__class__.__name__}')
            return False

    def _show_login_message(self, service_name: str):
        """
        Mostra mensagem informativa antes de abrir navegador para login
        """
        print("=" * 60)
        print(f"🔐 LOGIN NECESSÁRIO - {service_name.upper()}")
        print("=" * 60)
        print("O navegador será aberto para você fazer login.")
        print("IMPORTANTE:")
        print("1. Faça o login normalmente")
        print("2. Após o login, FECHE O APLICATIVO COMPLETAMENTE")
        print("3. Reinicie o aplicativo")
        print("4. Na próxima vez funcionará automaticamente")
        print("=" * 60)
        print("Abrindo navegador em 3 segundos...")
        time.sleep(3)

    def _verify_interface_active(self) -> bool:
        """
        Verifica se a interface do sistema ainda está ativa
        """
        try:
            # Verifica se o whatsapp ainda está ativo
            whatsapp_active = (hasattr(self.whatsapp, 'window_signal') and
                               self.whatsapp.window_signal)
            if whatsapp_active:
                print("Sistema sendo encerrado - parando Whatsmenu")
                return False

            # Verifica se o próprio whatsmenu foi sinalizado para parar
            if self.window_signal:
                print("Whatsmenu sinalizado para parar")
                return False

            return True
        except Exception:
            return False

    def _restart_with_visible_browser(self):
        """
        Reinicia o driver em modo visível para permitir login
        """
        try:
            if self.driver:
                self.driver.quit()
        except Exception:
            pass

        # Remove o headless e reinicia
        self.options = Options()
        self.options.add_argument(f'user-data-dir={PROFILE_WHATSMENU_PATH}')
        self.options.add_argument(r'--disable-print-preview')

        try:
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.get(
                'https://next.whatsmenu.com.br/auth/login?callbackUrl=https%3A'
                '%2F%2Fnext.whatsmenu.com.br%2Fdashboard%2Frequest')
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 6)

            # Agora faz o login com navegador visível
            self._login_()

        except Exception as e:
            print(f'Erro reiniciando Whatsmenu: {e.__class__.__name__}')
            raise e

    def _login_(self) -> None:
        while not self.logged_in:
            if not self.browser_window:
                break
            try:
                # Tenta diferentes seletores para os campos de login
                email_selectors = [
                    '/html/body/main/div/div[2]/div/div/div/form/div[1]/input',
                    '//input[@type="email"]',
                    '//input[@name="email"]',
                    '//input[@placeholder*="email" or @placeholder*="Email"]'
                ]

                password_selectors = [
                    '/html/body/main/div/div[2]/div/div/div/form/div[2]/input',
                    '//input[@type="password"]',
                    '//input[@name="password"]',
                    '//input[@placeholder*="senha"]'
                ]

                email_found = False
                password_found = False

                # Tenta encontrar campo de email
                for selector in email_selectors:
                    try:
                        element = self.wait.until(
                            lambda x: x.find_element(By.XPATH, selector)
                        )
                        email_found = True
                        break
                    except TimeoutException:
                        continue

                # Tenta encontrar campo de senha
                for selector in password_selectors:
                    try:
                        element = self.wait.until(
                            lambda x: x.find_element(By.XPATH, selector)
                        )
                        password_found = True
                        break
                    except TimeoutException:
                        continue

                if not email_found or not password_found:
                    raise TimeoutException("Login fields not found")

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
            # Verifica se a interface ainda está ativa antes de continuar
            if not self._verify_interface_active():
                print("Interface não está mais ativa - encerrando Whatsmenu")
                break

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
