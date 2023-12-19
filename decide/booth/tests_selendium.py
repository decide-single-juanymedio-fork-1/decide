import time
from base.tests import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

#PARA QUE ESTAS PRUEBAS FUNCIONEN CORRECTAMENTE, ES NECESARIO REALIZAR EL ./manage.py flush y luego ./manage.py loaddata populate.json, y finalmente
#.manage.py runserver
class TestBoothview(StaticLiveServerTestCase):

  def setUp(self):
    self.base = BaseTestCase()
    self.base.setUp()

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    self.driver = webdriver.Chrome(options=options)

    super().setUp()

  def tearDown(self):
    super().tearDown()
    self.driver.quit()

    self.base.tearDown()

  def test_boothview(self):
    #Logearse y realizar votación con ayuda de la notificación
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.find_element(By.NAME, "username").click()
    self.driver.find_element(By.NAME, "username").send_keys("usuario1")
    self.driver.find_element(By.NAME, "password").click()
    self.driver.find_element(By.NAME, "password").send_keys("practica1")
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(5)
    self.driver.find_element(By.LINK_TEXT, "aquí").click()
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .btn").click()
    time.sleep(5)
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("usuario1")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("practica1")
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    time.sleep(5)
    self.driver.find_element(By.ID, "q2").click()
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    time.sleep(5)
    assert self.driver.switch_to.alert.text == "¿Está seguro de su elección?"
    self.driver.switch_to.alert.accept()
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
    self.driver.close()


  def test_boothview2(self):
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.find_element(By.LINK_TEXT, "Regístrese").click()
    time.sleep(5)
    self.driver.find_element(By.ID, "id_username").send_keys("usuario4")
    self.driver.find_element(By.ID, "id_email").click()
    self.driver.find_element(By.ID, "id_email").send_keys("usuario4@us.es")
    self.driver.find_element(By.ID, "id_password1").click()
    self.driver.find_element(By.ID, "id_password1").send_keys("practica4")
    self.driver.find_element(By.ID, "id_password2").click()
    self.driver.find_element(By.ID, "id_password2").send_keys("practica4")
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(5)
    self.driver.find_element(By.LINK_TEXT, "Página principal").click()
    time.sleep(5)
    self.driver.find_element(By.LINK_TEXT, "Cambiar perfil").click()
    time.sleep(5)
    self.driver.find_element(By.ID, "id_email").click()
    self.driver.find_element(By.ID, "id_email").send_keys("usuario422@us.es")
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(5)
    self.driver.find_element(By.LINK_TEXT, "Página principal").click()
    time.sleep(5)
    self.driver.find_element(By.LINK_TEXT, "Cerrar sesión").click()
    self.driver.close()

