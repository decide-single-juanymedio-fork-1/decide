from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TestBoothview():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_boothview(self):
    #Logearse y realizar votación con ayuda de la notificación
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.set_window_size(910, 1016)
    self.driver.find_element(By.NAME, "username").click()
    self.driver.find_element(By.NAME, "username").send_keys("usuario1")
    self.driver.find_element(By.NAME, "password").click()
    self.driver.find_element(By.NAME, "password").send_keys("practica1")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.LINK_TEXT, "aquí").click()
    self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon").click()
    self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .btn").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("usuario1")
    self.driver.find_element(By.ID, "password").send_keys("practica1")
    self.driver.find_element(By.ID, "registerModal").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .btn")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .btn").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(3) > .form-group").click()
    self.driver.find_element(By.ID, "q1").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    assert self.driver.switch_to.alert.text == "¿Está seguro de su elección?"
    self.driver.switch_to.alert.accept()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()

  def test_boothview2(self):
    #Crear usuario, modificarlo y luego cerrar cesion
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.set_window_size(910, 1016)
    self.driver.find_element(By.NAME, "username").click()
    self.driver.find_element(By.LINK_TEXT, "Regístrese").click()
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("usuario4")
    self.driver.find_element(By.ID, "id_email").click()
    self.driver.find_element(By.ID, "id_email").send_keys("usuario4@us.es")
    self.driver.find_element(By.ID, "id_password1").click()
    self.driver.find_element(By.ID, "id_password1").send_keys("practica4")
    self.driver.find_element(By.ID, "id_password2").send_keys("practica4")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.LINK_TEXT, "Página principal").click()
    self.driver.find_element(By.LINK_TEXT, "Cambiar perfil").click()
    self.driver.find_element(By.ID, "id_email").click()
    self.driver.find_element(By.ID, "id_email").send_keys("usuario422@us.es")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.LINK_TEXT, "Cerrar sesión").click()
